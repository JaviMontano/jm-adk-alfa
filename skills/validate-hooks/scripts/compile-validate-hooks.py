#!/usr/bin/env python3
"""Compile a deterministic offline hooks audit from structured JSON."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
PAYLOAD_FIELDS = {"command", "url", "prompt", "agent"}


@dataclass(frozen=True)
class Finding:
    severity: str
    event: str
    hook_type: str
    rule: str
    finding: str
    remediation: str


@dataclass(frozen=True)
class HookEntry:
    event: str
    hook_type: str
    index: int
    payload: dict[str, Any]
    source: str


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_object(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def require_fields(data: dict[str, Any], required: list[str], label: str) -> None:
    missing = [field for field in required if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def build_data_from_hooks_file(path: Path, plugin_root: Path) -> dict[str, Any]:
    hooks_json = load_json(path)
    return {
        "repo_name": plugin_root.name,
        "plugin_root": str(plugin_root),
        "hooks_path": str(path),
        "hooks_json": hooks_json,
        "expected_placement_guard": True,
        "evidence": {
            "source": str(path),
            "read_mode": "offline-read-only",
            "mutation_policy": "no hooks executed and no config mutated",
        },
    }


def validate_input(data: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(data, schema["required_root_fields"], "root")
    if not isinstance(data["hooks_json"], dict):
        raise ValueError("hooks_json must be an object containing the hooks key")
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("evidence must be an object")
    require_fields(evidence, schema["required_evidence_fields"], "evidence")


def all_events(matrix: dict[str, Any]) -> set[str]:
    return set(matrix["tool_use_context_events"]) | set(matrix["non_tool_use_context_events"])


def did_you_mean(event: str, matrix: dict[str, Any]) -> str:
    explicit = matrix.get("common_event_misspellings", {}).get(event)
    if explicit:
        return explicit
    candidates = all_events(matrix)
    lowered = event.lower()
    for candidate in candidates:
        if candidate.lower() == lowered:
            return candidate
    return ""


def detect_shape(hooks_json: dict[str, Any]) -> str:
    if "hooks" not in hooks_json:
        return "missing-hooks-key"
    hooks_value = hooks_json["hooks"]
    if isinstance(hooks_value, dict):
        return "event-keyed-object"
    if isinstance(hooks_value, list):
        return "flat-event-array"
    return type(hooks_value).__name__


def collect_entries(
    hooks_json: dict[str, Any],
    matrix: dict[str, Any],
) -> tuple[str, list[HookEntry], list[Finding]]:
    findings: list[Finding] = []
    entries: list[HookEntry] = []
    shape = detect_shape(hooks_json)
    events = all_events(matrix)

    if shape == "missing-hooks-key":
        findings.append(
            Finding(
                "CRITICAL",
                "(root)",
                "(none)",
                "hooks-key",
                "hooks.json is missing the top-level hooks key.",
                "Add a top-level hooks object keyed by event name.",
            )
        )
        return shape, entries, findings

    hooks_value = hooks_json["hooks"]
    if shape == "event-keyed-object":
        if not hooks_value:
            findings.append(
                Finding(
                    "INFO",
                    "(root)",
                    "(none)",
                    "empty-hooks",
                    "hooks is an empty object.",
                    "No remediation required unless hooks are expected.",
                )
            )
            return shape, entries, findings
        for event, value in hooks_value.items():
            event_name = str(event)
            if event_name not in events:
                suggestion = did_you_mean(event_name, matrix)
                remediation = f"Rename event to {suggestion}." if suggestion else "Use one of the 22 recognized event names."
                findings.append(
                    Finding(
                        "WARNING",
                        event_name,
                        "(event)",
                        "event-name",
                        "Unrecognized hook event name.",
                        remediation,
                    )
                )
            if not isinstance(value, list):
                findings.append(
                    Finding(
                        "CRITICAL",
                        event_name,
                        "(event)",
                        "event-array",
                        "Event value must be an array of hook entry objects.",
                        "Replace the event value with an array, even for one hook.",
                    )
                )
                continue
            if not value:
                findings.append(
                    Finding(
                        "WARNING",
                        event_name,
                        "(none)",
                        "empty-event-array",
                        "Event contains an empty hooks array.",
                        "Remove the event key or add at least one hook entry.",
                    )
                )
                continue
            for index, hook in enumerate(value):
                if not isinstance(hook, dict):
                    findings.append(
                        Finding(
                            "CRITICAL",
                            event_name,
                            "(entry)",
                            "hook-entry-object",
                            "Hook entry must be an object.",
                            "Replace the entry with an object containing type and payload fields.",
                        )
                    )
                    continue
                hook_type = str(hook.get("type", ""))
                entries.append(HookEntry(event_name, hook_type, index, hook, "event-keyed-object"))
        return shape, entries, findings

    if shape == "flat-event-array":
        findings.append(
            Finding(
                "CRITICAL",
                "(root)",
                "(structure)",
                "hooks-shape",
                "hooks key is an array; canonical hooks.json requires an event-keyed object.",
                "Convert to {\"hooks\": {\"PreToolUse\": [{\"type\": \"command\", ...}]}}.",
            )
        )
        for index, hook in enumerate(hooks_value):
            if not isinstance(hook, dict):
                findings.append(
                    Finding(
                        "CRITICAL",
                        "(unknown)",
                        "(entry)",
                        "hook-entry-object",
                        "Flat hooks entry must be an object.",
                        "Replace the entry with an event-keyed hook object.",
                    )
                )
                continue
            event_name = str(hook.get("event") or hook.get("hookEventName") or hook.get("type") or "(missing)")
            hook_type = str(hook.get("hook_type") or hook.get("kind") or ("command" if "command" in hook else ""))
            if event_name not in events:
                suggestion = did_you_mean(event_name, matrix)
                remediation = f"Rename event to {suggestion}." if suggestion else "Use one of the 22 recognized event names."
                findings.append(
                    Finding(
                        "WARNING",
                        event_name,
                        hook_type or "(missing)",
                        "event-name",
                        "Flat hook entry uses an unrecognized event name.",
                        remediation,
                    )
                )
            entries.append(HookEntry(event_name, hook_type, index, hook, "flat-event-array"))
        return shape, entries, findings

    findings.append(
        Finding(
            "CRITICAL",
            "(root)",
            "(structure)",
            "hooks-shape",
            f"hooks key has unsupported type {shape}.",
            "Use an object keyed by event name.",
        )
    )
    return shape, entries, findings


def validate_entry_contract(entry: HookEntry, matrix: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    hook_types = matrix["hook_types"]
    hook_type = entry.hook_type
    event = entry.event
    payload = entry.payload

    if not hook_type:
        findings.append(
            Finding(
                "CRITICAL",
                event,
                "(missing)",
                "hook-type",
                "Hook entry is missing the type field.",
                "Set type to one of command, http, prompt, or agent.",
            )
        )
        return findings

    if hook_type not in hook_types:
        if hook_type in all_events(matrix):
            message = "Hook type field appears to contain an event name, not a hook type."
        else:
            message = "Hook entry has an unrecognized hook type."
        findings.append(
            Finding(
                "CRITICAL",
                event,
                hook_type,
                "hook-type",
                message,
                "Use one of command, http, prompt, or agent.",
            )
        )
        return findings

    required_field = hook_types[hook_type]["requires_field"]
    if not isinstance(payload.get(required_field), str) or not str(payload.get(required_field)).strip():
        findings.append(
            Finding(
                "CRITICAL",
                event,
                hook_type,
                "required-field",
                f"type {hook_type} requires a non-empty {required_field} string.",
                f"Add {required_field} or change the hook type.",
            )
        )

    populated_payloads = [field for field in PAYLOAD_FIELDS if isinstance(payload.get(field), str) and payload.get(field)]
    if len(populated_payloads) > 1:
        findings.append(
            Finding(
                "CRITICAL",
                event,
                hook_type,
                "ambiguous-payload",
                f"Hook entry mixes multiple payload fields: {', '.join(sorted(populated_payloads))}.",
                "Keep only the payload field that matches the hook type.",
            )
        )

    if hook_types[hook_type]["requires_tool_use_context"] and event not in matrix["tool_use_context_events"]:
        findings.append(
            Finding(
                "CRITICAL",
                event,
                hook_type,
                "tool-use-context",
                f"Hook type {hook_type} on event {event} will fail because {event} does not provide ToolUseContext.",
                "Change type to command or move to PreToolUse, PermissionRequest, or PostToolUse.",
            )
        )

    matcher = payload.get("matcher")
    if matcher is None:
        findings.append(
            Finding(
                "INFO",
                event,
                hook_type,
                "broad-matcher",
                "Matcher is omitted, so the hook fires for every instance of the event.",
                "Add a matcher when the hook should be scoped.",
            )
        )
    elif not isinstance(matcher, str):
        findings.append(
            Finding(
                "WARNING",
                event,
                hook_type,
                "matcher-type",
                "Matcher must be a string.",
                "Convert matcher to a string or remove it.",
            )
        )
    elif looks_like_regex(matcher):
        findings.append(
            Finding(
                "WARNING",
                event,
                hook_type,
                "matcher-regex",
                "Matcher looks like a regex; many hook contexts expect plain strings.",
                "Use a plain tool name or documented session-start matcher.",
            )
        )

    return findings


def looks_like_regex(value: str) -> bool:
    return any(token in value for token in [".*", "^", "$", "[", "]", "(", ")", "+", "?"])


def command_findings(entry: HookEntry, policy: dict[str, Any], plugin_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if entry.hook_type != "command":
        return findings
    command = entry.payload.get("command")
    if not isinstance(command, str) or not command.strip():
        return findings

    for check in policy["checks"]:
        if re.search(check["pattern"], command):
            findings.append(
                Finding(
                    check["severity"],
                    entry.event,
                    "command",
                    check["id"],
                    check["finding"],
                    check["remediation"],
                )
            )

    for script_ref in script_references(command):
        findings.extend(validate_script_reference(entry, script_ref, plugin_root))
    return findings


def script_references(command: str) -> list[str]:
    try:
        parts = shlex.split(command)
    except ValueError:
        return []
    refs: list[str] = []
    for part in parts:
        if part.startswith("-"):
            continue
        cleaned = part.strip()
        if cleaned.endswith((".sh", ".py")) or cleaned.startswith(("./scripts/", "scripts/")):
            refs.append(cleaned[2:] if cleaned.startswith("./") else cleaned)
    return refs


def validate_script_reference(entry: HookEntry, script_ref: str, plugin_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if os.path.isabs(script_ref):
        findings.append(
            Finding(
                "CRITICAL",
                entry.event,
                "command",
                "script-portability",
                f"Command references absolute script path {script_ref}.",
                "Use a project-relative script path.",
            )
        )
        return findings
    if script_ref.startswith("../"):
        findings.append(
            Finding(
                "CRITICAL",
                entry.event,
                "command",
                "script-portability",
                f"Command references script outside plugin root: {script_ref}.",
                "Move the script under the plugin root or use a documented local command.",
            )
        )
        return findings
    script_path = plugin_root / script_ref
    if not script_path.exists():
        findings.append(
            Finding(
                "CRITICAL",
                entry.event,
                "command",
                "script-exists",
                f"Referenced script does not exist: {script_ref}.",
                "Create the script or update hooks.json to the correct relative path.",
            )
        )
        return findings
    if script_path.suffix == ".sh":
        mode = script_path.stat().st_mode
        if not (mode & stat.S_IXUSR):
            findings.append(
                Finding(
                    "WARNING",
                    entry.event,
                    "command",
                    "script-executable",
                    f"Referenced shell script is not executable: {script_ref}.",
                    f"Run chmod +x {script_ref} or invoke it explicitly with bash.",
                )
            )
    return findings


def placement_guard_findings(
    entries: list[HookEntry],
    expectations: dict[str, Any],
    expected_enabled: bool,
) -> list[Finding]:
    if not expected_enabled or not expectations.get("enabled", False):
        return []
    event = expectations["event"]
    fragments = expectations["command_fragments"]
    guard_entries: list[HookEntry] = []
    misplaced_entries: list[HookEntry] = []
    for entry in entries:
        command = str(entry.payload.get("command", ""))
        description = str(entry.payload.get("description", ""))
        haystack = f"{command} {description}"
        if any(fragment in haystack for fragment in fragments):
            if entry.event == event and entry.hook_type == "command":
                guard_entries.append(entry)
            else:
                misplaced_entries.append(entry)

    findings: list[Finding] = []
    if misplaced_entries:
        for entry in misplaced_entries:
            findings.append(
                Finding(
                    "CRITICAL",
                    entry.event,
                    entry.hook_type or "(missing)",
                    "placement-guard-event",
                    "Placement guard is registered outside the required PreToolUse command hook.",
                    expectations["remediation"],
                )
            )
    if not guard_entries:
        findings.append(
            Finding(
                "WARNING",
                event,
                "command",
                "placement-guard-missing",
                "No PreToolUse command hook references the placement guard.",
                expectations["remediation"],
            )
        )
    return findings


def count_by_severity(findings: list[Finding]) -> dict[str, int]:
    return {
        "CRITICAL": sum(1 for finding in findings if finding.severity == "CRITICAL"),
        "WARNING": sum(1 for finding in findings if finding.severity == "WARNING"),
        "INFO": sum(1 for finding in findings if finding.severity == "INFO"),
    }


def safe_count(entries: list[HookEntry], matrix: dict[str, Any]) -> int:
    safe = 0
    for entry in entries:
        hook_type = entry.hook_type
        if hook_type not in matrix["hook_types"]:
            continue
        if matrix["hook_types"][hook_type]["requires_tool_use_context"] and entry.event not in matrix["tool_use_context_events"]:
            continue
        required = matrix["hook_types"][hook_type]["requires_field"]
        if not isinstance(entry.payload.get(required), str) or not entry.payload.get(required):
            continue
        safe += 1
    return safe


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def findings_table(findings: list[Finding]) -> str:
    if not findings:
        return "- [CODE] No findings."
    rows = [
        "| Severity | Event | Hook Type | Rule | Finding | Remediation |",
        "|---|---|---|---|---|---|",
    ]
    for finding in sorted(findings, key=lambda item: (SEVERITY_ORDER[item.severity], item.event, item.rule)):
        rows.append(
            "| {severity} | {event} | {hook_type} | {rule} | {finding} | {remediation} |".format(
                severity=finding.severity,
                event=finding.event,
                hook_type=finding.hook_type,
                rule=finding.rule,
                finding=finding.finding,
                remediation=finding.remediation,
            )
        )
    return "\n".join(rows)


def critical_findings(findings: list[Finding]) -> str:
    critical = [finding for finding in findings if finding.severity == "CRITICAL"]
    if not critical:
        return "- [CODE] No critical findings."
    return "\n".join(
        f"- [CODE] {finding.event} / {finding.hook_type}: {finding.finding} Remediation: {finding.remediation}"
        for finding in critical
    )


def event_coverage(entries: list[HookEntry], matrix: dict[str, Any]) -> str:
    if not entries:
        return "- [CODE] No hook entries to classify."
    events = sorted({entry.event for entry in entries})
    tool_events = [event for event in events if event in matrix["tool_use_context_events"]]
    non_tool_events = [event for event in events if event in matrix["non_tool_use_context_events"]]
    unknown_events = [event for event in events if event not in all_events(matrix)]
    return "\n".join(
        [
            f"- [CODE] Events present: {', '.join(events)}.",
            f"- [CODE] ToolUseContext events present: {', '.join(tool_events) if tool_events else 'none'}.",
            f"- [CODE] Non-ToolUseContext events present: {', '.join(non_tool_events) if non_tool_events else 'none'}.",
            f"- [CODE] Unknown events present: {', '.join(unknown_events) if unknown_events else 'none'}.",
        ]
    )


def tool_use_context_lines(entries: list[HookEntry], matrix: dict[str, Any]) -> str:
    lines = [
        "- [CODE] ToolUseContext is available only on PreToolUse, PermissionRequest, and PostToolUse.",
        "- [CODE] command and http hooks are compatible with all 22 recognized events.",
        "- [CODE] prompt and agent hooks are compatible only with ToolUseContext events.",
    ]
    incompatible = [
        entry
        for entry in entries
        if entry.hook_type in {"prompt", "agent"} and entry.event not in matrix["tool_use_context_events"]
    ]
    if incompatible:
        for entry in incompatible:
            lines.append(f"- [CODE] Incompatible: {entry.hook_type} on {entry.event}.")
    else:
        lines.append("- [CODE] No prompt or agent hooks are registered on non-ToolUseContext events.")
    return "\n".join(lines)


def command_safety_lines(entries: list[HookEntry], findings: list[Finding]) -> str:
    command_entries = [entry for entry in entries if entry.hook_type == "command"]
    command_findings = [
        finding
        for finding in findings
        if finding.rule
        in {
            "destructive-root-delete",
            "hard-reset",
            "git-clean-force",
            "sudo",
            "network-pipe-shell",
            "secret-file-read",
            "script-portability",
            "script-exists",
            "script-executable",
        }
    ]
    lines = [f"- [CODE] Command hooks inspected without execution: {len(command_entries)}."]
    if command_findings:
        lines.append(f"- [CODE] Command safety findings: {len(command_findings)}.")
    else:
        lines.append("- [CODE] No command safety findings.")
    return "\n".join(lines)


def placement_guard_lines(entries: list[HookEntry], expectations: dict[str, Any]) -> str:
    fragments = expectations["command_fragments"]
    expected_event = expectations["event"]
    matches = []
    for entry in entries:
        command = str(entry.payload.get("command", ""))
        description = str(entry.payload.get("description", ""))
        if any(fragment in f"{command} {description}" for fragment in fragments):
            matches.append(entry)
    if not matches:
        return "\n".join(
            [
                f"- [CODE] Expected event: {expected_event}.",
                "- [CODE] Placement guard hook not detected.",
                f"- [CODE] Policy reference: {expectations['required_policy_reference']}.",
            ]
        )
    lines = [f"- [CODE] Expected event: {expected_event}."]
    for entry in matches:
        lines.append(f"- [CODE] Detected placement guard reference on {entry.event} as {entry.hook_type}.")
    lines.append(f"- [CODE] Policy reference: {expectations['required_policy_reference']}.")
    return "\n".join(lines)


def remediation_checklist(findings: list[Finding]) -> str:
    actionable = [finding for finding in findings if finding.severity in {"CRITICAL", "WARNING"}]
    if not actionable:
        return "- [CODE] No remediation required."
    seen: set[str] = set()
    lines: list[str] = []
    for finding in sorted(actionable, key=lambda item: (SEVERITY_ORDER[item.severity], item.rule, item.event)):
        item = f"- [CODE] {finding.severity}: {finding.remediation}"
        if item not in seen:
            lines.append(item)
            seen.add(item)
    return "\n".join(lines)


def validation_lines(shape: str, entries: list[HookEntry]) -> str:
    return "\n".join(
        [
            f"- [CODE] hooks.json structure checked: {shape}.",
            "- [CODE] Event names checked against all 22 recognized events.",
            "- [CODE] Hook type compatibility checked against command, http, prompt, and agent.",
            "- [CODE] ToolUseContext availability checked for prompt and agent hooks.",
            "- [CODE] Command safety inspected by string analysis only.",
            "- [CODE] Placement guard expectations checked without mutating config.",
            f"- [CODE] Hook entries analyzed: {len(entries)}.",
        ]
    )


def risk_lines() -> str:
    return "\n".join(
        [
            "- [INFERENCE] Offline checks cannot prove runtime behavior of hook commands.",
            "- [INFERENCE] Command safety checks are pattern-based and may miss project-specific hazards.",
            "- [ASSUMPTION] The supplied hooks_json is the authoritative hooks configuration for the audited plugin root.",
            "- [CODE] This compiler does not execute hook commands and only writes a report when --output is supplied.",
        ]
    )


def render_report(
    data: dict[str, Any],
    shape: str,
    entries: list[HookEntry],
    findings: list[Finding],
    matrix: dict[str, Any],
    expectations: dict[str, Any],
) -> str:
    counts = count_by_severity(findings)
    status = "FAIL" if counts["CRITICAL"] else "PASS"
    template = (skill_dir() / "assets" / "validate-hooks-template.md").read_text(encoding="utf-8")
    replacements = {
        "{{REPO_NAME}}": str(data["repo_name"]),
        "{{HOOKS_PATH}}": str(data["hooks_path"]),
        "{{HOOKS_SHAPE}}": shape,
        "{{TOTAL_HOOKS}}": str(len(entries)),
        "{{SAFE_COUNT}}": str(safe_count(entries, matrix)),
        "{{CRITICAL_COUNT}}": str(counts["CRITICAL"]),
        "{{WARNING_COUNT}}": str(counts["WARNING"]),
        "{{INFO_COUNT}}": str(counts["INFO"]),
        "{{STATUS}}": status,
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{CRITICAL_FINDINGS}}": critical_findings(findings),
        "{{FINDINGS_TABLE}}": findings_table(findings),
        "{{EVENT_COVERAGE}}": event_coverage(entries, matrix),
        "{{TOOL_USE_CONTEXT}}": tool_use_context_lines(entries, matrix),
        "{{COMMAND_SAFETY}}": command_safety_lines(entries, findings),
        "{{PLACEMENT_GUARD}}": placement_guard_lines(entries, expectations),
        "{{REMEDIATION_CHECKLIST}}": remediation_checklist(findings),
        "{{VALIDATION}}": validation_lines(shape, entries),
        "{{RISKS}}": risk_lines(),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def compile_audit(data: dict[str, Any]) -> tuple[str, list[Finding]]:
    base = skill_dir()
    schema = load_object(base / "assets" / "hooks-audit-schema.json")
    matrix = load_object(base / "assets" / "hook-compatibility-matrix.json")
    command_policy = load_object(base / "assets" / "command-safety-policy.json")
    placement_expectations = load_object(base / "assets" / "placement-guard-expectations.json")
    validate_input(data, schema)

    plugin_root = Path(str(data.get("plugin_root") or ".")).resolve()
    shape, entries, findings = collect_entries(data["hooks_json"], matrix)
    for entry in entries:
        findings.extend(validate_entry_contract(entry, matrix))
        findings.extend(command_findings(entry, command_policy, plugin_root))
    findings.extend(
        placement_guard_findings(
            entries,
            placement_expectations,
            bool(data.get("expected_placement_guard", True)),
        )
    )
    return render_report(data, shape, entries, findings, matrix, placement_expectations), findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic offline hooks audit")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="Structured hooks audit JSON")
    source.add_argument("--hooks-json", help="Read an actual hooks.json file without executing hooks")
    parser.add_argument("--plugin-root", default=".", help="Plugin root for script existence checks")
    parser.add_argument("--output", help="Write Markdown report to this path; stdout by default")
    args = parser.parse_args()

    try:
        plugin_root = Path(args.plugin_root).resolve()
        if args.input:
            data = load_object(Path(args.input))
            if "plugin_root" not in data:
                data["plugin_root"] = str(plugin_root)
        else:
            data = build_data_from_hooks_file(Path(args.hooks_json), plugin_root)
        report, findings = compile_audit(data)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)

    if any(finding.severity == "CRITICAL" for finding in findings):
        print("ERROR: critical hooks findings detected", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
