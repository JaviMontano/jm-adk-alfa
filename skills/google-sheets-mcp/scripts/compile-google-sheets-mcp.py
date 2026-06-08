#!/usr/bin/env python3
"""Compile a deterministic Google Sheets MCP operation plan from JSON.

This script is intentionally offline. It reads local assets and fixtures only;
it never calls Google Sheets, OAuth, HTTP, network, or MCP tools.
"""

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


def require_fields(data: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


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


def scope_profiles(scope_policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    profiles = scope_policy.get("profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("scope-policy profiles must be a list")
    return {str(profile["id"]): profile for profile in profiles if isinstance(profile, dict)}


def mcp_tools(mcp_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tools = mcp_contract.get("tools", [])
    if not isinstance(tools, list):
        raise ValueError("mcp-tool-contract tools must be a list")
    return {str(tool["name"]): tool for tool in tools if isinstance(tool, dict)}


def validate_scope_binding(operation: dict[str, Any], scope_policy: dict[str, Any]) -> None:
    required = str(scope_policy["official_note"]["required_binding"])
    actual = str(operation["scope_binding"])
    if actual != required:
        raise ValueError(f"scope_binding must be {required}; Sheets scopes do not bind to sheet tabs")


def validate_scope_for_action(
    operation: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
) -> None:
    profile_id = str(operation["scope_profile"])
    if profile_id not in profiles:
        raise ValueError(f"unknown scope_profile for {operation['id']}: {profile_id}")
    allowed = profiles[profile_id].get("allowed_actions", [])
    if operation["action"] not in allowed:
        raise ValueError(f"scope_profile {profile_id} cannot perform {operation['action']}")


def validate_tool_for_action(operation: dict[str, Any], tools: dict[str, dict[str, Any]]) -> None:
    tool_name = str(operation["mcp_tool"])
    if tool_name not in tools:
        raise ValueError(f"unknown mcp_tool for {operation['id']}: {tool_name}")
    allowed = tools[tool_name].get("rest_methods", [])
    if operation["action"] not in allowed:
        raise ValueError(f"mcp_tool {tool_name} cannot perform {operation['action']}")


def validate_read_only_first(
    data: dict[str, Any],
    schema: dict[str, Any],
    safety: dict[str, Any],
) -> None:
    ro = require_object(data, "read_only_first")
    required = safety["read_only_first"]["required_fields"]
    require_fields(ro, required, "read_only_first")
    for field in required:
        if ro[field] is not True:
            raise ValueError(f"read_only_first.{field} must be true")

    operations = data["operations"]
    mutating = [op for op in operations if op["action"] in schema["mutating_actions"]]
    if not mutating:
        return
    first_action = str(operations[0]["action"])
    if first_action not in safety["read_only_first"]["first_action_types"]:
        raise ValueError("mutating Sheets workflows must start with read-only discovery")


def validate_confirmation(
    data: dict[str, Any],
    schema: dict[str, Any],
    safety: dict[str, Any],
) -> None:
    mutating = [op for op in data["operations"] if op["action"] in schema["mutating_actions"]]
    confirmation = require_object(data, "human_confirmation")
    require_fields(confirmation, ["status", "confirmed_by", "confirmation_text", "mutation_count"], "human_confirmation")
    if not mutating:
        return

    required_status = str(safety["human_confirmation"]["required_status"])
    if confirmation["status"] != required_status:
        raise ValueError(f"mutating Sheets operation requires human_confirmation.status={required_status}")
    prefix = str(safety["human_confirmation"]["confirmation_phrase_prefix"])
    text = str(confirmation["confirmation_text"])
    if not text.startswith(prefix):
        raise ValueError(f"human_confirmation.confirmation_text must start with {prefix}")
    if confirmation["mutation_count"] != len(mutating):
        raise ValueError("human_confirmation.mutation_count must equal planned mutating operation count")

    for operation in mutating:
        if operation.get("requires_human_confirmation") is not True:
            raise ValueError(f"{operation['id']} requires requires_human_confirmation=true")
        if operation.get("confirmation_key") != text:
            raise ValueError(f"{operation['id']} confirmation_key must match human_confirmation.confirmation_text")


def validate_a1(value: str, label: str) -> None:
    if "!" not in value or not value.split("!", 1)[0] or not value.split("!", 1)[1]:
        raise ValueError(f"{label} must use SheetName!A1 notation")


def validate_values(values: Any, label: str) -> None:
    if not isinstance(values, list) or not values:
        raise ValueError(f"{label}.values must be a non-empty list")
    for row in values:
        if not isinstance(row, list):
            raise ValueError(f"{label}.values rows must be lists")
        for cell in row:
            if cell is not None and not isinstance(cell, (bool, int, float, str)):
                raise ValueError(f"{label}.values cells must be bool, number, string, or null")


def validate_value_range(
    value_range: dict[str, Any],
    schema: dict[str, Any],
    label: str,
) -> None:
    require_fields(value_range, ["range", "majorDimension", "values"], label)
    validate_a1(str(value_range["range"]), f"{label}.range")
    if value_range["majorDimension"] not in schema["allowed_major_dimensions"]:
        raise ValueError(f"{label}.majorDimension is unsupported: {value_range['majorDimension']}")
    validate_values(value_range["values"], label)


def validate_spreadsheets_get(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(operation, schema["required_spreadsheet_get_fields"], operation["id"])
    if not str(operation["spreadsheet_id"]).strip():
        raise ValueError(f"{operation['id']} spreadsheet_id must be non-empty")
    if not str(operation["fields"]).strip():
        raise ValueError(f"{operation['id']} fields must be non-empty")
    if not isinstance(operation["include_grid_data"], bool):
        raise ValueError(f"{operation['id']} include_grid_data must be boolean")
    for range_value in operation.get("ranges", []):
        validate_a1(str(range_value), f"{operation['id']}.ranges[]")


def validate_spreadsheets_create(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(operation, schema["required_spreadsheet_create_fields"], operation["id"])
    body = require_object(operation, "spreadsheet_body")
    properties = require_object(body, "properties")
    if not str(properties.get("title", "")).strip():
        raise ValueError(f"{operation['id']} spreadsheet_body.properties.title must be non-empty")


def validate_batch_update(
    operation: dict[str, Any],
    schema: dict[str, Any],
    batch_policy: dict[str, Any],
) -> None:
    require_fields(operation, schema["required_batch_update_fields"], operation["id"])
    if not str(operation["spreadsheet_id"]).strip():
        raise ValueError(f"{operation['id']} spreadsheet_id must be non-empty")
    batch = require_object(operation, "batch_update")
    requests = require_list(batch, "requests")
    allowed = set(batch_policy["allowed_request_types"])
    for request in requests:
        if not isinstance(request, dict) or len(request) != 1:
            raise ValueError(f"{operation['id']} batchUpdate request must have exactly one request type")
        request_type = next(iter(request))
        if request_type not in allowed:
            raise ValueError(f"{operation['id']} unsupported batchUpdate request type: {request_type}")
    if not isinstance(batch.get("includeSpreadsheetInResponse", False), bool):
        raise ValueError(f"{operation['id']} includeSpreadsheetInResponse must be boolean")


def validate_values_get(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(operation, schema["required_values_get_fields"], operation["id"])
    if not str(operation["spreadsheet_id"]).strip():
        raise ValueError(f"{operation['id']} spreadsheet_id must be non-empty")
    validate_a1(str(operation["range_a1"]), f"{operation['id']}.range_a1")
    if operation["major_dimension"] not in schema["allowed_major_dimensions"]:
        raise ValueError(f"{operation['id']} major_dimension is unsupported")
    if operation["value_render_option"] not in schema["allowed_value_render_options"]:
        raise ValueError(f"{operation['id']} value_render_option is unsupported")
    if operation["date_time_render_option"] not in schema["allowed_date_time_render_options"]:
        raise ValueError(f"{operation['id']} date_time_render_option is unsupported")


def validate_values_write(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    required = (
        schema["required_values_append_fields"]
        if operation["action"] == "spreadsheets.values.append"
        else schema["required_values_write_fields"]
    )
    require_fields(operation, required, operation["id"])
    if not str(operation["spreadsheet_id"]).strip():
        raise ValueError(f"{operation['id']} spreadsheet_id must be non-empty")
    if operation["value_input_option"] not in schema["allowed_value_input_options"]:
        raise ValueError(f"{operation['id']} value_input_option is unsupported")
    if operation["action"] == "spreadsheets.values.append" and operation["insert_data_option"] not in schema["allowed_insert_data_options"]:
        raise ValueError(f"{operation['id']} insert_data_option is unsupported")
    validate_value_range(require_object(operation, "value_range"), schema, f"{operation['id']}.value_range")


def validate_values_batch_update(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(operation, schema["required_values_batch_update_fields"], operation["id"])
    if not str(operation["spreadsheet_id"]).strip():
        raise ValueError(f"{operation['id']} spreadsheet_id must be non-empty")
    batch = require_object(operation, "batch_values")
    if batch.get("valueInputOption") not in schema["allowed_value_input_options"]:
        raise ValueError(f"{operation['id']} batch_values.valueInputOption is unsupported")
    data = require_list(batch, "data")
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{operation['id']} batch_values.data[{index}] must be an object")
        validate_value_range(item, schema, f"{operation['id']}.batch_values.data[{index}]")


def validate_operation_payload(
    operation: dict[str, Any],
    schema: dict[str, Any],
    batch_policy: dict[str, Any],
) -> None:
    action = operation["action"]
    if action == "spreadsheets.get":
        validate_spreadsheets_get(operation, schema)
    elif action == "spreadsheets.create":
        validate_spreadsheets_create(operation, schema)
    elif action == "spreadsheets.batchUpdate":
        validate_batch_update(operation, schema, batch_policy)
    elif action == "spreadsheets.values.get":
        validate_values_get(operation, schema)
    elif action in {"spreadsheets.values.update", "spreadsheets.values.append"}:
        validate_values_write(operation, schema)
    elif action == "spreadsheets.values.batchUpdate":
        validate_values_batch_update(operation, schema)


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> None:
    schema = assets["schema"]
    require_fields(data, schema["required_root_fields"], "root")
    if data["mcp_server"] not in schema["allowed_mcp_servers"]:
        raise ValueError(f"unsupported mcp_server: {data['mcp_server']}")
    if data["operation_mode"] not in schema["allowed_operation_modes"]:
        raise ValueError(f"unsupported operation_mode: {data['operation_mode']}")

    operations = require_list(data, "operations")
    operation_ids: set[str] = set()
    profiles = scope_profiles(assets["scope_policy"])
    tools = mcp_tools(assets["mcp_contract"])
    for operation in operations:
        if not isinstance(operation, dict):
            raise ValueError("each operation must be an object")
        require_fields(operation, schema["required_operation_fields"], "operation")
        if operation["id"] in operation_ids:
            raise ValueError(f"duplicate operation id: {operation['id']}")
        operation_ids.add(str(operation["id"]))
        if operation["action"] not in schema["allowed_actions"]:
            raise ValueError(f"unsupported action for {operation['id']}: {operation['action']}")
        validate_scope_binding(operation, assets["scope_policy"])
        validate_scope_for_action(operation, profiles)
        validate_tool_for_action(operation, tools)
        validate_operation_payload(operation, schema, assets["batch_policy"])

    validate_read_only_first(data, schema, assets["safety"])
    validate_confirmation(data, schema, assets["safety"])
    evidence = require_object(data, "evidence")
    require_fields(evidence, schema["required_evidence_fields"], "evidence")


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [DOC] {key}: {value}" for key, value in sorted(evidence.items()))


def mcp_preflight_lines(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> str:
    requirements = assets["mcp_contract"]["mcp_tools_spec_requirements"]
    return "\n".join(
        [
            f"- [CODE] MCP server: `{data['mcp_server']}`.",
            "- [CODE] Compiler mode: offline plan/checklist only; no Google, OAuth, network, or MCP calls are performed.",
            "- [DOC] Local setup docs: `docs/google-workspace-mcp-setup.md` and `docs/mcp-integration.md`.",
            f"- [DOC] MCP tool definitions require name/description/inputSchema; inputSchema note: {requirements['inputSchema']}",
        ]
    )


def scope_note_lines(data: dict[str, Any], scope_policy: dict[str, Any]) -> str:
    profiles = scope_profiles(scope_policy)
    official = scope_policy["official_note"]
    lines = [
        f"- [DOC] Official scope note: {official['statement']}",
        f"- [DOC] Required local scope binding: `{official['required_binding']}`.",
        f"- [DOC] Sheet-level edit protection alternative: {official['protected_range_alternative']}",
    ]
    for operation in data["operations"]:
        profile = profiles[str(operation["scope_profile"])]
        lines.append(
            f"- [DOC] `{operation['id']}` uses `{profile['scope']}` for `{operation['action']}`; rationale: {profile['rationale']}"
        )
    return "\n".join(lines)


def operation_table(data: dict[str, Any]) -> str:
    lines = [
        "| Step | REST method | MCP tool | Scope profile | Gate | Description |",
        "|---|---|---|---|---|---|",
    ]
    mutating = set(load_json(skill_dir() / "assets" / "google-sheets-mcp-schema.json")["mutating_actions"])
    for index, operation in enumerate(data["operations"], start=1):
        gate = "human confirmation" if operation["action"] in mutating else "read-only"
        lines.append(
            f"| {index} | `{operation['action']}` | `{operation['mcp_tool']}` | `{operation['scope_profile']}` | {gate} | {operation['description']} |"
        )
    return "\n".join(lines)


def value_contract_lines(data: dict[str, Any], value_policy: dict[str, Any]) -> str:
    lines = [
        f"- [DOC] ValueRange required fields: {', '.join(value_policy['value_range']['required_fields'])}.",
        f"- [DOC] Supported input value types: {', '.join(value_policy['value_range']['supported_input_value_types'])}.",
        f"- [DOC] Null policy: {value_policy['value_range']['null_policy']}",
        f"- [DOC] Append table detection: {value_policy['append']['table_detection']}",
    ]
    value_ops = [
        operation
        for operation in data["operations"]
        if operation["action"].startswith("spreadsheets.values.")
    ]
    for operation in value_ops:
        if operation["action"] == "spreadsheets.values.get":
            lines.append(f"- [CODE] `{operation['id']}` reads `{operation['range_a1']}` as `{operation['major_dimension']}`.")
        elif operation["action"] == "spreadsheets.values.batchUpdate":
            ranges = [item["range"] for item in operation["batch_values"]["data"]]
            lines.append(f"- [CODE] `{operation['id']}` writes batch ranges: {', '.join(ranges)}.")
        else:
            lines.append(f"- [CODE] `{operation['id']}` writes `{operation['value_range']['range']}` with `{operation['value_input_option']}`.")
    return "\n".join(lines)


def batch_update_lines(data: dict[str, Any], batch_policy: dict[str, Any]) -> str:
    reqs = batch_policy["requirements"]
    lines = [
        f"- [DOC] Structural method: `{batch_policy['method']}`.",
        f"- [DOC] batchUpdate requests are atomic: {reqs['atomicity']}",
        f"- [DOC] Request order: {reqs['request_order']}",
        f"- [INFERENCE] Collaboration limit: {reqs['collaboration_limit']}",
    ]
    for operation in data["operations"]:
        if operation["action"] == "spreadsheets.batchUpdate":
            request_types = [next(iter(request)) for request in operation["batch_update"]["requests"]]
            lines.append(f"- [CODE] `{operation['id']}` structural request types: {', '.join(request_types)}.")
    return "\n".join(lines)


def confirmation_lines(data: dict[str, Any], schema: dict[str, Any]) -> str:
    confirmation = data["human_confirmation"]
    mutating = [operation for operation in data["operations"] if operation["action"] in schema["mutating_actions"]]
    lines = [
        f"- [CODE] human confirmation: {confirmation['status']}.",
        f"- [CODE] Confirmed by: `{confirmation['confirmed_by']}`.",
        f"- [CODE] Confirmation text: {confirmation['confirmation_text']}",
        f"- [CODE] Planned mutating operations: {len(mutating)}.",
    ]
    for operation in mutating:
        lines.append(f"- [CODE] `{operation['id']}` mutation gate is confirmed.")
    return "\n".join(lines)


def validation_lines(data: dict[str, Any]) -> str:
    read_only = data["read_only_first"]
    return "\n".join(
        [
            "- [CODE] Structured schema validation passed.",
            f"- [CODE] Read-only-first enabled: {read_only['enabled']}.",
            f"- [CODE] Metadata checked: {read_only['metadata_checked']}.",
            f"- [CODE] Ranges checked: {read_only['ranges_checked']}.",
            f"- [CODE] Formula impact checked: {read_only['formula_impact_checked']}.",
            f"- [CODE] Protected ranges reviewed: {read_only['protected_ranges_reviewed']}.",
            "- [CODE] Scope bindings validated as spreadsheet_file.",
        ]
    )


def risk_lines(data: dict[str, Any]) -> str:
    risks = [
        "- [INFERENCE] This plan must be reviewed before live MCP execution because the compiler intentionally does not inspect real spreadsheet permissions.",
        "- [INFERENCE] The compiler cannot verify formulas, protected ranges, named ranges, filters, charts, or collaborator activity in the live spreadsheet.",
    ]
    if any(operation["action"] == "spreadsheets.batchUpdate" for operation in data["operations"]):
        risks.append("- [INFERENCE] Structural batch updates can affect formulas, formatting, protected ranges, and downstream dashboards.")
    if any(operation["action"] == "spreadsheets.values.append" for operation in data["operations"]):
        risks.append("- [INFERENCE] Append table detection depends on the live sheet's current contiguous data region.")
    return "\n".join(risks)


def load_assets() -> dict[str, dict[str, Any]]:
    base = skill_dir() / "assets"
    return {
        "schema": load_json(base / "google-sheets-mcp-schema.json"),
        "scope_policy": load_json(base / "scope-policy.json"),
        "mcp_contract": load_json(base / "mcp-tool-contract.json"),
        "safety": load_json(base / "operation-safety-policy.json"),
        "value_policy": load_json(base / "value-range-policy.json"),
        "batch_policy": load_json(base / "batch-update-policy.json")
    }


def render_report(data: dict[str, Any]) -> str:
    assets = load_assets()
    validate_input(data, assets)
    template = (skill_dir() / "assets" / "google-sheets-mcp-template.md").read_text(encoding="utf-8")
    summary = "\n".join(
        [
            f"- [CODE] Request ID: `{data['request_id']}`.",
            f"- [CODE] Operation mode: `{data['operation_mode']}`.",
            f"- [CODE] Planned operations: {len(data['operations'])}.",
            f"- [CODE] Output is an offline Google Sheets MCP plan/checklist for: {data['request_title']}.",
        ]
    )
    replacements = {
        "{request_title}": str(data["request_title"]),
        "{summary}": summary,
        "{evidence}": evidence_lines(data["evidence"]),
        "{mcp_preflight}": mcp_preflight_lines(data, assets),
        "{scope_note}": scope_note_lines(data, assets["scope_policy"]),
        "{operation_plan}": operation_table(data),
        "{value_contract}": value_contract_lines(data, assets["value_policy"]),
        "{batch_update_contract}": batch_update_lines(data, assets["batch_policy"]),
        "{confirmation_gate}": confirmation_lines(data, assets["schema"]),
        "{validation}": validation_lines(data),
        "{risks}": risk_lines(data),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic Google Sheets MCP plan")
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output", help="Optional output Markdown path")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.input))
        report = render_report(data)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
        else:
            print(report)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
