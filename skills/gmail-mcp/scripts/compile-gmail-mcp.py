#!/usr/bin/env python3
"""Compile a deterministic offline Gmail MCP operation plan from JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def validate_required(data: dict[str, Any], required: list[str], label: str) -> None:
    missing = [field for field in required if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def confirmation_present(action: dict[str, Any], prefix: str) -> bool:
    value = str(action.get("human_confirmation", ""))
    return value.startswith(prefix)


def action_scope(action_type: str, scope_matrix: dict[str, Any]) -> str:
    return str(scope_matrix["operation_to_scope"].get(action_type, "manual_scope_review"))


def is_bulk_label(action: dict[str, Any], threshold: int) -> bool:
    if action.get("type") != "modify_message_labels":
        return False
    message_ids = action.get("message_ids", [])
    if not isinstance(message_ids, list):
        return False
    return bool(action.get("bulk")) or len(message_ids) > threshold


def validate_input(
    data: dict[str, Any],
    schema: dict[str, Any],
    safety: dict[str, Any],
    search_policy: dict[str, Any],
    send_policy: dict[str, Any],
) -> None:
    validate_required(data, schema["required_root_fields"], "root")
    if data["operation"] not in schema["allowed_operations"]:
        raise ValueError(f"unsupported operation: {data['operation']}")
    if data["read_only_first"] is not True:
        raise ValueError("read_only_first must be true")

    search = require_object(data, "search")
    validate_required(search, schema["required_search_fields"], "search")
    if not str(search["query"]).strip():
        raise ValueError("search.query must be non-empty")
    if not isinstance(search["label_ids"], list):
        raise ValueError("search.label_ids must be a list")
    if not isinstance(search["max_results"], int):
        raise ValueError("search.max_results must be an integer")
    hard_limit = int(search_policy["query_contract"]["max_results_hard_limit"])
    if search["max_results"] < 1 or search["max_results"] > hard_limit:
        raise ValueError(f"search.max_results must be between 1 and {hard_limit}")
    if not isinstance(search["needs_body_access"], bool):
        raise ValueError("search.needs_body_access must be boolean")

    actions = require_list(data, "planned_actions")
    first_action_type = str(actions[0].get("type", ""))
    if first_action_type not in safety["read_only_first"]["first_action_types"]:
        raise ValueError("first planned action must be read-only")

    allowed_actions = set(schema["allowed_action_types"])
    allowed_tools = set(schema["allowed_tools"])
    prefix = str(send_policy["confirmation_phrase_prefix"])
    confirmation_required = set(safety["human_confirmation_required_for"])
    bulk_threshold = int(safety["bulk_label_message_threshold"])

    for action in actions:
        if not isinstance(action, dict):
            raise ValueError("each planned action must be an object")
        validate_required(action, schema["required_action_fields"], "planned_action")
        action_type = str(action["type"])
        if action_type not in allowed_actions:
            raise ValueError(f"unsupported action type: {action_type}")
        if action["tool"] not in allowed_tools:
            raise ValueError(f"unsupported MCP tool: {action['tool']}")

        needs_confirmation = action_type in confirmation_required
        if is_bulk_label(action, bulk_threshold):
            needs_confirmation = True
            action["confirmation_reason"] = "bulk_label_modify"
        if action_type == "modify_message_labels":
            add_labels = action.get("add_label_names", [])
            remove_labels = action.get("remove_label_names", [])
            if not isinstance(add_labels, list) or not isinstance(remove_labels, list):
                raise ValueError("modify_message_labels add/remove labels must be lists")
            if "TRASH" in add_labels or "INBOX" in remove_labels:
                needs_confirmation = True
                action["confirmation_reason"] = "label_operation_changes_visibility"
        if needs_confirmation and not confirmation_present(action, prefix):
            raise ValueError(f"{action_type} requires human confirmation starting with {prefix}")

    privacy = require_object(data, "privacy")
    validate_required(privacy, schema["required_privacy_fields"], "privacy")
    for key in schema["required_privacy_fields"]:
        if not isinstance(privacy[key], bool):
            raise ValueError(f"privacy.{key} must be boolean")
    if privacy["store_email_bodies"]:
        raise ValueError("privacy.store_email_bodies must be false")
    if privacy["store_attachments"]:
        raise ValueError("privacy.store_attachments must be false")
    if not privacy["redact_pii"]:
        raise ValueError("privacy.redact_pii must be true")
    if not privacy["redact_credentials"]:
        raise ValueError("privacy.redact_credentials must be true")

    evidence = require_object(data, "evidence")
    validate_required(evidence, schema["required_evidence_fields"], "evidence")
    if evidence["compiler_mode"] != safety["compiler_mode"]:
        raise ValueError("evidence.compiler_mode must be offline_only")


def evidence_lines(data: dict[str, Any], safety: dict[str, Any]) -> str:
    evidence = data["evidence"]
    lines = [
        f"- [CODE] request_id: `{data['request_id']}`.",
        f"- [CODE] operation: `{data['operation']}`.",
        f"- [CODE] compiler_mode: `{safety['compiler_mode']}`.",
        f"- [DOC] documentation_snapshot: {evidence['documentation_snapshot']}.",
        f"- [CODE] input_source: {evidence['source']}.",
    ]
    return "\n".join(lines)


def scope_table(data: dict[str, Any], scope_matrix: dict[str, Any]) -> str:
    lines = ["| Action | Tool | Minimum scope review |", "|---|---|---|"]
    for action in data["planned_actions"]:
        scope = action_scope(str(action["type"]), scope_matrix)
        lines.append(f"| `{action['id']}` | `{action['tool']}` | `{scope}` |")
    return "\n".join(lines)


def safety_gate_lines(data: dict[str, Any], safety: dict[str, Any]) -> str:
    gates = [
        "- [CODE] Read-only-first: enabled and first planned action is read-only.",
        "- [CODE] Script mode: offline plan/checklist only; no Gmail, OAuth, network, or MCP call is performed.",
        f"- [CODE] Direct send default: {safety['direct_send_default']}.",
    ]
    for action in data["planned_actions"]:
        if action.get("human_confirmation"):
            gates.append(f"- [CODE] `{action['id']}` has human confirmation captured.")
    return "\n".join(gates)


def tool_sequence(data: dict[str, Any], scope_matrix: dict[str, Any]) -> str:
    lines: list[str] = []
    for index, action in enumerate(data["planned_actions"], start=1):
        scope = action_scope(str(action["type"]), scope_matrix)
        lines.append(
            f"{index}. [CODE] `{action['tool']}` for `{action['type']}`; "
            f"scope review `{scope}`; {action['description']}"
        )
    return "\n".join(lines)


def confirmation_checklist(data: dict[str, Any], safety: dict[str, Any]) -> str:
    lines: list[str] = []
    bulk_threshold = int(safety["bulk_label_message_threshold"])
    for action in data["planned_actions"]:
        needs_confirmation = str(action["type"]) in safety["human_confirmation_required_for"]
        if is_bulk_label(action, bulk_threshold):
            needs_confirmation = True
        if str(action["type"]) == "modify_message_labels":
            add_labels = action.get("add_label_names", [])
            remove_labels = action.get("remove_label_names", [])
            if "TRASH" in add_labels or "INBOX" in remove_labels:
                needs_confirmation = True
        if needs_confirmation:
            status = "present" if action.get("human_confirmation") else "missing"
            lines.append(f"- [CODE] `{action['id']}` confirmation: {status}.")
    if not lines:
        lines.append("- [CODE] No destructive, send, filter, or bulk-label action is planned.")
    return "\n".join(lines)


def privacy_controls(data: dict[str, Any], privacy_policy: dict[str, Any]) -> str:
    privacy = data["privacy"]
    lines = [
        f"- [CODE] Store email bodies: {privacy['store_email_bodies']}.",
        f"- [CODE] Store attachments: {privacy['store_attachments']}.",
        f"- [CODE] Redact PII: {privacy['redact_pii']}.",
        f"- [CODE] Redact credentials: {privacy['redact_credentials']}.",
        f"- [CODE] Attachment policy: {privacy_policy['attachment_policy']['default']}.",
    ]
    return "\n".join(lines)


def risk_lines(data: dict[str, Any], search_policy: dict[str, Any]) -> str:
    risks = [
        "- [INFERENCE] This plan must be reviewed before live MCP execution because the script intentionally does not inspect the real mailbox.",
        "- [INFERENCE] Gmail API search can differ from Gmail UI search for alias expansion and thread-wide behavior.",
    ]
    if data["search"]["needs_body_access"]:
        risks.append("- [INFERENCE] Body access increases privacy exposure; fetch only selected message or thread IDs.")
    if data["search"]["max_results"] == search_policy["query_contract"]["max_results_hard_limit"]:
        risks.append("- [INFERENCE] The search uses the hard result limit; narrow the query before live execution if possible.")
    return "\n".join(risks)


def render_report(data: dict[str, Any]) -> str:
    base = skill_dir()
    assets_dir = base / "assets"
    schema = load_json(assets_dir / "gmail-mcp-schema.json")
    safety = load_json(assets_dir / "operation-safety-policy.json")
    scope_matrix = load_json(assets_dir / "scope-matrix.json")
    search_policy = load_json(assets_dir / "search-query-patterns.json")
    send_policy = load_json(assets_dir / "send-draft-policy.json")
    privacy_policy = load_json(assets_dir / "privacy-redaction-policy.json")
    template = (assets_dir / "gmail-mcp-template.md").read_text(encoding="utf-8")

    validate_input(data, schema, safety, search_policy, send_policy)

    summary = (
        f"[CODE] Plan `{data['request_id']}` compiles a `{data['operation']}` Gmail MCP workflow "
        f"for: {data['objective']}"
    )
    replacements = {
        "{summary}": summary,
        "{evidence}": evidence_lines(data, safety),
        "{scope_review}": scope_table(data, scope_matrix),
        "{safety_gates}": safety_gate_lines(data, safety),
        "{tool_sequence}": tool_sequence(data, scope_matrix),
        "{confirmation_checklist}": confirmation_checklist(data, safety),
        "{privacy_controls}": privacy_controls(data, privacy_policy),
        "{risks}": risk_lines(data, search_policy),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an offline Gmail MCP operation plan")
    parser.add_argument("--input", required=True, help="Path to structured Gmail MCP input JSON")
    parser.add_argument("--output", help="Path to write Markdown output; stdout when omitted")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.input))
        report = render_report(data)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
