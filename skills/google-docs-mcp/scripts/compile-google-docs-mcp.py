#!/usr/bin/env python3
"""Compile a deterministic Google Docs MCP operation plan from JSON.

This script is intentionally offline. It reads local assets and fixtures only;
it never calls Google Docs, OAuth, or MCP tools.
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


def tool_contracts(mcp_contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tools = mcp_contract.get("tools", [])
    if not isinstance(tools, list):
        raise ValueError("mcp-tool-contract tools must be a list")
    return {str(tool["name"]): tool for tool in tools if isinstance(tool, dict)}


def mutating_actions(schema: dict[str, Any]) -> set[str]:
    return {str(action) for action in schema["mutating_actions"]}


def validate_root(data: dict[str, Any], schema: dict[str, Any], scope_policy: dict[str, Any]) -> None:
    require_fields(data, schema["required_root_fields"], "root")
    if data["mcp_server"] not in schema["allowed_mcp_servers"]:
        raise ValueError(f"unsupported mcp_server: {data['mcp_server']}")
    if data["operation_mode"] not in schema["allowed_operation_modes"]:
        raise ValueError(f"unsupported operation_mode: {data['operation_mode']}")
    profiles = scope_profiles(scope_policy)
    if data["requested_scope_profile"] not in profiles:
        raise ValueError(f"unknown requested_scope_profile: {data['requested_scope_profile']}")


def validate_confirmation(
    data: dict[str, Any],
    schema: dict[str, Any],
    confirmation_policy: dict[str, Any],
) -> None:
    operations = require_list(data, "operations")
    workflow_mutates = any(operation.get("action") in mutating_actions(schema) for operation in operations if isinstance(operation, dict))
    confirmation = require_object(data, "human_confirmation")
    require_fields(confirmation, schema["required_confirmation_fields"], "human_confirmation")
    if not workflow_mutates:
        return
    if confirmation["status"] != confirmation_policy["required_status"]:
        raise ValueError("mutating operation requires human_confirmation.status=confirmed")
    if not str(confirmation["confirmed_by"]).strip():
        raise ValueError("mutating operation requires human_confirmation.confirmed_by")
    prefix = str(confirmation_policy["confirmation_phrase_prefix"])
    if not str(confirmation["confirmation_text"]).startswith(prefix):
        raise ValueError(f"human_confirmation.confirmation_text must start with {prefix}")


def validate_read_only_first(data: dict[str, Any], schema: dict[str, Any]) -> None:
    ro = require_object(data, "read_only_first")
    require_fields(ro, schema["required_read_only_first_fields"], "read_only_first")
    has_batch_update = any(
        isinstance(operation, dict) and operation.get("action") == "batch_update"
        for operation in require_list(data, "operations")
    )
    if not has_batch_update:
        return
    for key in ["document_resolved", "structure_checked", "revision_id_captured"]:
        if ro[key] is not True:
            raise ValueError(f"documents.batchUpdate requires read_only_first.{key}=true")
    if not str(ro["existing_content_summary"]).strip():
        raise ValueError("documents.batchUpdate requires read_only_first.existing_content_summary")


def validate_scope_for_action(operation: dict[str, Any], scope_policy: dict[str, Any]) -> None:
    profile_id = str(operation["scope_profile"])
    profiles = scope_profiles(scope_policy)
    if profile_id not in profiles:
        raise ValueError(f"unknown scope_profile for {operation['id']}: {profile_id}")
    allowed = profiles[profile_id].get("allowed_actions", [])
    if operation["action"] not in allowed:
        raise ValueError(f"scope_profile {profile_id} cannot perform {operation['action']}")


def validate_tool_for_action(operation: dict[str, Any], mcp_contract: dict[str, Any]) -> None:
    tool_name = str(operation["mcp_tool"])
    tools = tool_contracts(mcp_contract)
    if tool_name not in tools:
        raise ValueError(f"unknown mcp_tool for {operation['id']}: {tool_name}")
    allowed = tools[tool_name].get("actions", [])
    if operation["action"] not in allowed:
        raise ValueError(f"mcp_tool {tool_name} cannot perform {operation['action']}")


def validate_method_for_action(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    action = str(operation["action"])
    expected = schema["method_by_action"].get(action)
    if operation["docs_api_method"] != expected:
        raise ValueError(f"{operation['id']} must use Docs API method {expected}")


def validate_create(operation: dict[str, Any], schema: dict[str, Any]) -> None:
    create = require_object(operation, "create")
    require_fields(create, schema["required_create_fields"], f"create for {operation['id']}")
    blocked = [field for field in schema["blocked_create_fields"] if field in create]
    if blocked:
        raise ValueError("documents.create cannot include body content; use documents.batchUpdate")
    if not str(create["title"]).strip():
        raise ValueError(f"documents.create requires title for {operation['id']}")
    if create["initial_content_strategy"] not in schema["allowed_initial_content_strategies"]:
        raise ValueError(f"unsupported initial_content_strategy for {operation['id']}")
    if create["initial_content_strategy"] == "blank_then_batch_update" and create["follow_up_batch_update_required"] is not True:
        raise ValueError(f"blank_then_batch_update requires follow_up_batch_update_required=true for {operation['id']}")
    if create["document_id_capture"] is not True:
        raise ValueError(f"documents.create requires document_id_capture=true for {operation['id']}")
    if create["requires_human_confirmation"] is not True:
        raise ValueError(f"documents.create requires human confirmation for {operation['id']}")


def validate_get(operation: dict[str, Any], schema: dict[str, Any]) -> str:
    get = require_object(operation, "get")
    require_fields(get, schema["required_get_fields"], f"get for {operation['id']}")
    document_id = str(get["document_id"])
    if not document_id.strip():
        raise ValueError(f"documents.get requires document_id for {operation['id']}")
    if not str(get["fields"]).strip():
        raise ValueError(f"documents.get requires partial fields for {operation['id']}")
    if get["verify_document_id"] is not True:
        raise ValueError(f"documents.get requires verify_document_id=true for {operation['id']}")
    if not isinstance(get["include_tabs_content"], bool):
        raise ValueError(f"documents.get include_tabs_content must be boolean for {operation['id']}")
    if get["suggestions_view_mode"] not in schema["allowed_suggestions_view_modes"]:
        raise ValueError(f"unsupported suggestions_view_mode for {operation['id']}")
    return document_id


def require_range(payload: dict[str, Any], operation_id: str, request_type: str) -> None:
    range_payload = require_object(payload, "range")
    for field in ["startIndex", "endIndex"]:
        value = range_payload.get(field)
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{request_type} requires range.{field} integer for {operation_id}")
    if range_payload["endIndex"] <= range_payload["startIndex"]:
        raise ValueError(f"{request_type} requires range.endIndex after startIndex for {operation_id}")


def validate_request_payload(request: dict[str, Any], operation_id: str) -> None:
    request_type = str(request["type"])
    payload = require_object(request, "payload")
    if request_type == "insertText":
        if not str(payload.get("text", "")).strip():
            raise ValueError(f"insertText requires payload.text for {operation_id}")
        location = require_object(payload, "location")
        if not isinstance(location.get("index"), int) or location["index"] < 1:
            raise ValueError(f"insertText requires payload.location.index integer for {operation_id}")
    elif request_type == "deleteContentRange":
        require_range(payload, operation_id, request_type)
    elif request_type == "replaceAllText":
        contains = require_object(payload, "containsText")
        if not str(contains.get("text", "")).strip():
            raise ValueError(f"replaceAllText requires containsText.text for {operation_id}")
        if "replaceText" not in payload:
            raise ValueError(f"replaceAllText requires replaceText for {operation_id}")
    elif request_type in {"updateTextStyle", "updateParagraphStyle", "createParagraphBullets"}:
        require_range(payload, operation_id, request_type)
        if request_type != "createParagraphBullets" and not str(payload.get("fields", "")).strip():
            raise ValueError(f"{request_type} requires fields for {operation_id}")
        if request_type == "createParagraphBullets" and not str(payload.get("bulletPreset", "")).strip():
            raise ValueError(f"createParagraphBullets requires bulletPreset for {operation_id}")
    elif request_type == "insertTable":
        for field in ["rows", "columns"]:
            if not isinstance(payload.get(field), int) or payload[field] < 1:
                raise ValueError(f"insertTable requires positive {field} for {operation_id}")
        location = require_object(payload, "location")
        if not isinstance(location.get("index"), int) or location["index"] < 1:
            raise ValueError(f"insertTable requires payload.location.index integer for {operation_id}")
    elif request_type == "insertPageBreak":
        location = require_object(payload, "location")
        if not isinstance(location.get("index"), int) or location["index"] < 1:
            raise ValueError(f"insertPageBreak requires payload.location.index integer for {operation_id}")


def validate_batch_update(operation: dict[str, Any], schema: dict[str, Any], prior_get_ids: set[str]) -> None:
    batch = require_object(operation, "batch_update")
    require_fields(batch, schema["required_batch_update_fields"], f"batch_update for {operation['id']}")
    document_id = str(batch["document_id"])
    if not document_id.strip():
        raise ValueError(f"documents.batchUpdate requires document_id for {operation['id']}")
    if document_id not in prior_get_ids:
        raise ValueError("documents.batchUpdate requires a prior documents.get for the same document")
    if batch["requires_human_confirmation"] is not True:
        raise ValueError(f"documents.batchUpdate requires human confirmation for {operation['id']}")
    write_control = require_object(batch, "write_control")
    if not str(write_control.get("required_revision_id", "")).strip():
        raise ValueError(f"documents.batchUpdate requires write_control.required_revision_id for {operation['id']}")
    requests = require_list(batch, "requests")
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError(f"each batchUpdate request must be an object for {operation['id']}")
        require_fields(request, schema["required_batch_request_fields"], f"request for {operation['id']}")
        if request["type"] not in schema["allowed_batch_request_types"]:
            raise ValueError(f"unsupported batchUpdate request type for {operation['id']}: {request['type']}")
        validate_request_payload(request, str(operation["id"]))


def validate_operations(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> None:
    schema = assets["schema"]
    operation_ids: set[str] = set()
    prior_get_ids: set[str] = set()
    operations = require_list(data, "operations")
    for operation in operations:
        if not isinstance(operation, dict):
            raise ValueError("each operation must be an object")
        require_fields(operation, schema["required_operation_fields"], "operation")
        if operation["id"] in operation_ids:
            raise ValueError(f"duplicate operation id: {operation['id']}")
        operation_ids.add(str(operation["id"]))
        if operation["action"] not in schema["allowed_actions"]:
            raise ValueError(f"unsupported action for {operation['id']}: {operation['action']}")
        validate_method_for_action(operation, schema)
        validate_scope_for_action(operation, assets["scope_policy"])
        validate_tool_for_action(operation, assets["mcp_contract"])
        if operation["action"] == "create_document":
            validate_create(operation, schema)
        elif operation["action"] == "get_document":
            prior_get_ids.add(validate_get(operation, schema))
        elif operation["action"] == "batch_update":
            validate_batch_update(operation, schema, prior_get_ids)


def validate_evidence(data: dict[str, Any], schema: dict[str, Any]) -> None:
    evidence = require_object(data, "evidence")
    require_fields(evidence, schema["required_evidence_fields"], "evidence")
    for key in schema["required_evidence_fields"]:
        if not str(evidence[key]).strip():
            raise ValueError(f"evidence.{key} must be non-empty")


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> None:
    validate_root(data, assets["schema"], assets["scope_policy"])
    validate_read_only_first(data, assets["schema"])
    validate_confirmation(data, assets["schema"], assets["confirmation_policy"])
    validate_operations(data, assets)
    validate_evidence(data, assets["schema"])


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [DOC] {key}: {value}" for key, value in sorted(evidence.items()))


def mcp_preflight_lines(data: dict[str, Any], mcp_contract: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"- [CODE] Server expected: `{mcp_contract['server']}`.",
            f"- [CODE] Tool tier expected: `{mcp_contract['tool_tier']}`.",
            "- [CODE] Check local `.mcp.json` before live execution.",
            "- [CODE] This compiled plan is offline and does not call Docs, OAuth, or MCP.",
            f"- [CODE] Operation mode: `{data['operation_mode']}`.",
        ]
    )


def confirmation_state(operation: dict[str, Any]) -> str:
    if operation["action"] == "create_document":
        return "required" if operation["create"]["requires_human_confirmation"] else "missing"
    if operation["action"] == "batch_update":
        return "required" if operation["batch_update"]["requires_human_confirmation"] else "missing"
    return "not-required"


def operation_table(data: dict[str, Any]) -> str:
    lines = ["| ID | Action | Docs API Method | MCP Tool | Scope Profile | Confirmation |", "|---|---|---|---|---|---|"]
    for operation in data["operations"]:
        lines.append(
            f"| {operation['id']} | {operation['action']} | `{operation['docs_api_method']}` | "
            f"`{operation['mcp_tool']}` | {operation['scope_profile']} | {confirmation_state(operation)} |"
        )
    return "\n".join(lines)


def scope_plan_lines(data: dict[str, Any], scope_policy: dict[str, Any]) -> str:
    profiles = scope_profiles(scope_policy)
    seen: list[str] = []
    for operation in data["operations"]:
        profile_id = str(operation["scope_profile"])
        if profile_id not in seen:
            seen.append(profile_id)
    lines = ["| Scope Profile | OAuth Scope | Sensitivity | Mutates | Use |", "|---|---|---|---|---|"]
    for profile_id in seen:
        profile = profiles[profile_id]
        lines.append(
            f"| {profile_id} | `{profile['scope']}` | {profile['sensitivity']} | "
            f"{profile['mutation_allowed']} | {profile['use_when']} |"
        )
    return "\n".join(lines)


def create_plan_lines(data: dict[str, Any]) -> str:
    creates = [operation for operation in data["operations"] if operation["action"] == "create_document"]
    if not creates:
        return "- [CODE] No documents.create operation supplied."
    lines: list[str] = []
    for operation in creates:
        create = operation["create"]
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] Title: `{create['title']}`.",
                f"- [CODE] Initial content strategy: `{create['initial_content_strategy']}`.",
                f"- [CODE] Follow-up batchUpdate required: {create['follow_up_batch_update_required']}.",
                f"- [CODE] Capture created document ID: {create['document_id_capture']}.",
                f"- [CODE] Human confirmation: {create['requires_human_confirmation']}.",
            ]
        )
    return "\n".join(lines)


def get_plan_lines(data: dict[str, Any]) -> str:
    gets = [operation for operation in data["operations"] if operation["action"] == "get_document"]
    if not gets:
        return "- [CODE] No documents.get operation supplied."
    lines: list[str] = []
    for operation in gets:
        get = operation["get"]
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] Document ID: `{get['document_id']}`.",
                f"- [CODE] Fields: `{get['fields']}`.",
                f"- [CODE] Include tabs content: {get['include_tabs_content']}.",
                f"- [CODE] Suggestions view mode: `{get['suggestions_view_mode']}`.",
                f"- [CODE] Verify document ID: {get['verify_document_id']}.",
            ]
        )
    return "\n".join(lines)


def batch_update_plan_lines(data: dict[str, Any]) -> str:
    batches = [operation for operation in data["operations"] if operation["action"] == "batch_update"]
    if not batches:
        return "- [CODE] No documents.batchUpdate operation supplied."
    lines: list[str] = []
    for operation in batches:
        batch = operation["batch_update"]
        request_types = ", ".join(str(request["type"]) for request in batch["requests"])
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] Document ID: `{batch['document_id']}`.",
                f"- [CODE] Request count: {len(batch['requests'])}.",
                f"- [CODE] Request types: {request_types}.",
                f"- [CODE] Required revision ID: `{batch['write_control']['required_revision_id']}`.",
                f"- [CODE] Human confirmation: {batch['requires_human_confirmation']}.",
                "- [INFERENCE] Execute requests only after live structure indexes are rechecked.",
            ]
        )
    return "\n".join(lines)


def confirmation_gate_lines(data: dict[str, Any], confirmation_policy: dict[str, Any]) -> str:
    confirmation = data["human_confirmation"]
    mutating = [operation for operation in data["operations"] if operation["action"] in confirmation_policy["mutating_actions"]]
    lines = [
        f"- [CODE] Required status: `{confirmation_policy['required_status']}`.",
        f"- [CODE] Current status: `{confirmation['status']}`.",
        f"- [CODE] Confirmed by: `{confirmation['confirmed_by']}`.",
        f"- [CODE] Confirmation text: {confirmation['confirmation_text']}",
    ]
    if mutating:
        for operation in mutating:
            lines.append(f"- [CODE] `{operation['id']}` is blocked from live execution until confirmation is retained.")
    else:
        lines.append("- [CODE] No mutating Docs operation is planned.")
    return "\n".join(lines)


def validation_lines(data: dict[str, Any], schema: dict[str, Any]) -> str:
    actions = {operation["action"] for operation in data["operations"]}
    methods = {operation["docs_api_method"] for operation in data["operations"]}
    mutating = sorted(actions & mutating_actions(schema))
    return "\n".join(
        [
            "- [CODE] Structured input passed Google Docs MCP schema and policy validation.",
            f"- [CODE] Operation actions covered: {', '.join(sorted(actions))}.",
            f"- [CODE] Docs API methods covered: {', '.join(sorted(methods))}.",
            f"- [CODE] Mutating actions requiring confirmation: {', '.join(mutating) if mutating else 'none'}.",
            "- [CODE] documents.create is title-only and content insertion is deferred to batchUpdate.",
            "- [CODE] documents.batchUpdate has a prior documents.get for the same document.",
            "- [CODE] The compiler performed no network, OAuth, Docs, or MCP calls.",
        ]
    )


def risk_lines() -> str:
    return "\n".join(
        [
            "- [INFERENCE] Live Docs execution can still fail because of OAuth scope, document ACLs, admin policy, stale revision IDs, or invalid live indexes.",
            "- [INFERENCE] This plan does not prove that a Google Doc exists; it only validates the requested operation contract.",
            "- [ASSUMPTION] Document IDs, revision IDs, and index ranges in the input were supplied by a trusted user or a prior read-only discovery step.",
        ]
    )


def render(data: dict[str, Any], base: Path, assets: dict[str, dict[str, Any]]) -> str:
    template = (base / "assets" / "google-docs-mcp-template.md").read_text(encoding="utf-8")
    workflow_mutates = any(operation["action"] in mutating_actions(assets["schema"]) for operation in data["operations"])
    replacements = {
        "{{OPERATION_ID}}": str(data["operation_id"]),
        "{{REQUEST_TITLE}}": str(data["request_title"]),
        "{{MCP_SERVER}}": str(data["mcp_server"]),
        "{{OPERATION_MODE}}": str(data["operation_mode"]),
        "{{REQUESTED_SCOPE_PROFILE}}": str(data["requested_scope_profile"]),
        "{{MUTATING_WORKFLOW}}": str(workflow_mutates),
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{MCP_PREFLIGHT}}": mcp_preflight_lines(data, assets["mcp_contract"]),
        "{{OPERATION_TABLE}}": operation_table(data),
        "{{SCOPE_PLAN}}": scope_plan_lines(data, assets["scope_policy"]),
        "{{CREATE_PLAN}}": create_plan_lines(data),
        "{{GET_PLAN}}": get_plan_lines(data),
        "{{BATCH_UPDATE_PLAN}}": batch_update_plan_lines(data),
        "{{CONFIRMATION_GATE}}": confirmation_gate_lines(data, assets["confirmation_policy"]),
        "{{VALIDATION}}": validation_lines(data, assets["schema"]),
        "{{RISKS}}": risk_lines(),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def load_assets(base: Path) -> dict[str, dict[str, Any]]:
    return {
        "schema": load_json(base / "assets" / "google-docs-mcp-schema.json"),
        "operation_policy": load_json(base / "assets" / "docs-operation-policy.json"),
        "scope_policy": load_json(base / "assets" / "scope-policy.json"),
        "confirmation_policy": load_json(base / "assets" / "mutation-confirmation-policy.json"),
        "mcp_contract": load_json(base / "assets" / "mcp-tool-contract.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic Google Docs MCP plan")
    parser.add_argument("--input", required=True, help="Structured Google Docs MCP JSON")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        data = load_json(Path(args.input))
        assets = load_assets(base)
        validate_input(data, assets)
        output = render(data, base, assets)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
