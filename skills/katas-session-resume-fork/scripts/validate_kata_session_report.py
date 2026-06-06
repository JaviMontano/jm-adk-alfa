#!/usr/bin/env python3
"""Validate Kata 25 resume/fork/fresh reports against offline contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VALID_DECISIONS = {"resume", "fork", "fresh"}
SUMMARY_FIELDS = {"goal", "findings", "decisions", "current_sources", "next_steps"}


def load_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"invalid JSON: {exc}"]


def bool_at(data: dict, dotted: str) -> object:
    current: object = data
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def require_bool(data: dict, dotted: str, expected: bool) -> list[str]:
    actual = bool_at(data, dotted)
    if actual is not expected:
        return [f"{dotted} must be {expected}"]
    return []


def command_text(command: object) -> str:
    if isinstance(command, str):
        return command
    if isinstance(command, dict):
        values: list[str] = []
        for value in command.values():
            if isinstance(value, str):
                values.append(value)
            elif isinstance(value, list):
                values.extend(str(item) for item in value)
        return "\n".join(values)
    return ""


def validate_common(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    decision = data.get("decision")
    if decision not in VALID_DECISIONS:
        errors.append("decision must be resume, fork, or fresh")
    reason = data.get("reason")
    if not isinstance(reason, str) or len(reason.strip()) < 12:
        errors.append("reason must explain the decision")
    if not isinstance(data.get("signals"), dict):
        errors.append("signals must be an object")
    if not command_text(data.get("command")):
        errors.append("command is required")
    errors.extend(require_bool(data, "signals.raw_transcript_used", False))
    for dotted in [
        "validation.decision_matches_signals",
        "validation.staleness_checked",
        "validation.risk_recorded",
    ]:
        errors.extend(require_bool(data, dotted, True))
    return errors


def validate_resume(data: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(require_bool(data, "signals.context_valid", True))
    errors.extend(require_bool(data, "signals.world_changed", False))
    errors.extend(require_bool(data, "signals.stale_tool_results", False))
    errors.extend(require_bool(data, "signals.parallel_branches", False))
    if "--resume" not in command_text(data.get("command")):
        errors.append("resume command must contain --resume")
    return errors


def validate_fork(data: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(require_bool(data, "signals.parallel_branches", True))
    fork = data.get("fork")
    if not isinstance(fork, dict):
        return errors + ["fork object is required for fork decision"]
    if not isinstance(fork.get("baseline"), str) or not fork["baseline"].strip():
        errors.append("fork.baseline is required")
    branches = fork.get("branches")
    if not isinstance(branches, list) or len([b for b in branches if isinstance(b, str) and b.strip()]) < 2:
        errors.append("fork.branches must contain at least two branch names")
    if fork.get("shared_state") is not False:
        errors.append("fork.shared_state must be false")
    if "--fork" not in command_text(data.get("command")):
        errors.append("fork command must contain --fork")
    return errors


def validate_summary(summary: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(summary, dict):
        return ["summary object is required for fresh decision"]
    if summary.get("source") != "scratchpad":
        errors.append("summary.source must be scratchpad")
    if summary.get("typed") is not True:
        errors.append("summary.typed must be true")
    if summary.get("raw_transcript") is not False:
        errors.append("summary.raw_transcript must be false")
    fields = summary.get("fields")
    if not isinstance(fields, list) or not SUMMARY_FIELDS.issubset(set(fields)):
        errors.append("summary.fields must include goal, findings, decisions, current_sources, next_steps")
    return errors


def validate_fresh(data: dict) -> list[str]:
    errors: list[str] = []
    world_changed = bool_at(data, "signals.world_changed") is True
    stale = bool_at(data, "signals.stale_tool_results") is True
    if not (world_changed or stale):
        errors.append("fresh requires world_changed or stale_tool_results")
    errors.extend(require_bool(data, "signals.context_valid", False))
    errors.extend(require_bool(data, "validation.sources_reloaded", True))
    errors.extend(validate_summary(data.get("summary")))
    text = command_text(data.get("command"))
    if "claude -p" not in text:
        errors.append("fresh command must contain claude -p")
    if "transcript" in text.lower():
        errors.append("fresh command must not inject a raw transcript")
    return errors


def validate_report(path: Path) -> list[str]:
    data, errors = load_json(path)
    if errors:
        return errors
    if not isinstance(data, dict):
        return ["report root must be an object"]
    errors = validate_common(data)
    decision = data.get("decision")
    if decision == "resume":
        errors.extend(validate_resume(data))
    elif decision == "fork":
        errors.extend(validate_fork(data))
    elif decision == "fresh":
        errors.extend(validate_fresh(data))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate katas-session-resume-fork report JSON")
    parser.add_argument("reports", nargs="+", help="Report JSON file(s)")
    args = parser.parse_args()

    failed = False
    for report in args.reports:
        path = Path(report)
        errors = validate_report(path)
        if errors:
            failed = True
            print(f"report={path.name} status=fail errors={len(errors)}")
            for error in errors:
                print(f"ERROR: {error}")
        else:
            print(f"report={path.name} status=pass errors=0")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
