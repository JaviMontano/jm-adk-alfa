#!/usr/bin/env python3
"""Compile a deterministic offline Google Slides MCP operation plan from JSON."""

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


def require_fields(data: dict[str, Any], required: list[str], label: str) -> None:
    missing = [field for field in required if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def mcp_tools(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tools = contract.get("tools", [])
    if not isinstance(tools, list):
        raise ValueError("mcp-tool-contract tools must be a list")
    return {str(tool["name"]): tool for tool in tools if isinstance(tool, dict)}


def scope_profiles(scope_policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    profiles = scope_policy.get("profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("scope-policy profiles must be a list")
    return {str(profile["id"]): profile for profile in profiles if isinstance(profile, dict)}


def validate_confirmation(
    operation: dict[str, Any],
    action_payload: dict[str, Any],
    schema: dict[str, Any],
    policy: dict[str, Any],
) -> None:
    action = str(operation["action"])
    if action not in set(policy["mutating_actions"]):
        return
    confirmation = require_object(action_payload, "human_confirmation")
    require_fields(confirmation, schema["required_confirmation_fields"], f"human_confirmation for {operation['id']}")
    if confirmation["status"] != policy["required_status"]:
        raise ValueError(f"{action} requires human_confirmation.status={policy['required_status']}")
    prefix = str(policy["confirmation_phrase_prefix"])
    if not str(confirmation["confirmation_text"]).startswith(prefix):
        raise ValueError(f"{action} requires confirmation text starting with {prefix}")
    if not str(confirmation["confirmed_by"]).strip():
        raise ValueError(f"{action} requires human_confirmation.confirmed_by")


def validate_scope(
    operation: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
) -> None:
    profile_id = str(operation["scope_profile"])
    if profile_id not in profiles:
        raise ValueError(f"unknown scope_profile for {operation['id']}: {profile_id}")
    profile = profiles[profile_id]
    action = str(operation["action"])
    if action not in profile.get("allowed_actions", []):
        raise ValueError(f"scope_profile {profile_id} cannot perform {action}")
    if action.startswith("presentations.") and action in {"presentations.create", "presentations.batchUpdate"}:
        if profile.get("mutation_allowed") is not True:
            raise ValueError(f"scope_profile {profile_id} cannot mutate Slides presentations")
    if profile.get("minimum_by_default") is not True:
        exception = operation.get("scope_exception")
        if not isinstance(exception, dict) or not str(exception.get("reason", "")).strip():
            raise ValueError(f"scope_profile {profile_id} requires scope_exception.reason")


def validate_tool(
    operation: dict[str, Any],
    tools: dict[str, dict[str, Any]],
) -> None:
    tool_name = str(operation["mcp_tool"])
    if tool_name not in tools:
        raise ValueError(f"unknown MCP tool for {operation['id']}: {tool_name}")
    expected_action = str(tools[tool_name]["action"])
    if operation["action"] != expected_action:
        raise ValueError(f"MCP tool {tool_name} maps to {expected_action}, not {operation['action']}")


def validate_read_only_first(data: dict[str, Any], schema: dict[str, Any]) -> None:
    ro = require_object(data, "read_only_first")
    require_fields(ro, schema["required_read_only_first_fields"], "read_only_first")
    if ro["status"] not in schema["allowed_read_only_first_statuses"]:
        raise ValueError(f"unsupported read_only_first.status: {ro['status']}")
    checks = ro["checks"]
    if not isinstance(checks, list):
        raise ValueError("read_only_first.checks must be a list")
    missing = [check for check in schema["minimum_read_only_first_checks"] if check not in checks]
    if missing:
        raise ValueError(f"read_only_first.checks missing: {missing}")
    actions = [operation["action"] for operation in data["operations"]]
    if any(action in schema["mutating_actions"] for action in actions) and ro["status"] != "complete":
        raise ValueError("mutating plan requires read_only_first.status=complete")


def validate_create(
    operation: dict[str, Any],
    schema: dict[str, Any],
    confirmation_policy: dict[str, Any],
) -> str | None:
    create = require_object(operation, "create")
    require_fields(create, schema["required_create_fields"], f"create for {operation['id']}")
    if not str(create["title"]).strip():
        raise ValueError(f"create.title must be non-empty for {operation['id']}")
    body = create.get("body", {"title": create["title"]})
    if not isinstance(body, dict):
        raise ValueError(f"create.body must be an object for {operation['id']}")
    disallowed = sorted(set(body) - set(schema["allowed_create_body_fields"]))
    if disallowed:
        raise ValueError(f"presentations.create body includes ignored or unsupported fields: {disallowed}")
    if str(body.get("title", create["title"])) != str(create["title"]):
        raise ValueError(f"create.body.title must match create.title for {operation['id']}")
    validate_confirmation(operation, create, schema, confirmation_policy)
    return str(create.get("presentation_id") or body.get("presentationId") or "").strip() or None


def validate_get(operation: dict[str, Any], schema: dict[str, Any]) -> str:
    get = require_object(operation, "get")
    require_fields(get, schema["required_get_fields"], f"get for {operation['id']}")
    presentation_id = str(get["presentation_id"]).strip()
    if not presentation_id:
        raise ValueError(f"get.presentation_id must be non-empty for {operation['id']}")
    return presentation_id


def validate_page_get(operation: dict[str, Any], schema: dict[str, Any], known_ids: set[str]) -> None:
    page_get = require_object(operation, "page_get")
    require_fields(page_get, schema["required_page_get_fields"], f"page_get for {operation['id']}")
    presentation_id = str(page_get["presentation_id"]).strip()
    if not presentation_id or not str(page_get["page_object_id"]).strip():
        raise ValueError(f"page_get presentation_id and page_object_id are required for {operation['id']}")
    if presentation_id not in known_ids:
        raise ValueError(f"presentations.pages.get requires prior presentations.get or create for {presentation_id}")


def validate_thumbnail(
    operation: dict[str, Any],
    schema: dict[str, Any],
    thumbnail_policy: dict[str, Any],
    known_ids: set[str],
) -> None:
    thumbnail = require_object(operation, "thumbnail")
    require_fields(thumbnail, schema["required_thumbnail_fields"], f"thumbnail for {operation['id']}")
    presentation_id = str(thumbnail["presentation_id"]).strip()
    if not presentation_id or not str(thumbnail["page_object_id"]).strip():
        raise ValueError(f"thumbnail presentation_id and page_object_id are required for {operation['id']}")
    if presentation_id not in known_ids:
        raise ValueError(f"presentations.pages.getThumbnail requires prior presentations.get or create for {presentation_id}")
    mime_type = str(thumbnail.get("mime_type", thumbnail_policy["default_mime_type"]))
    if mime_type not in thumbnail_policy["allowed_mime_types"]:
        raise ValueError(f"unsupported thumbnail mime_type for {operation['id']}: {mime_type}")
    if thumbnail["thumbnail_size"] not in thumbnail_policy["allowed_thumbnail_sizes"]:
        raise ValueError(f"unsupported thumbnail_size for {operation['id']}: {thumbnail['thumbnail_size']}")
    if thumbnail["content_url_handling"] not in thumbnail_policy["allowed_content_url_handling"]:
        raise ValueError(f"unsupported content_url_handling for {operation['id']}: {thumbnail['content_url_handling']}")


def request_key(request: dict[str, Any], operation_id: str) -> str:
    if not isinstance(request, dict):
        raise ValueError(f"batchUpdate request must be an object for {operation_id}")
    keys = list(request.keys())
    if len(keys) != 1:
        raise ValueError(f"batchUpdate request must contain exactly one request key for {operation_id}")
    return keys[0]


def validate_batch_update(
    operation: dict[str, Any],
    schema: dict[str, Any],
    confirmation_policy: dict[str, Any],
    batch_policy: dict[str, Any],
    known_ids: set[str],
) -> None:
    batch = require_object(operation, "batch_update")
    require_fields(batch, schema["required_batch_update_fields"], f"batch_update for {operation['id']}")
    presentation_id = str(batch["presentation_id"]).strip()
    if not presentation_id:
        raise ValueError(f"batch_update.presentation_id must be non-empty for {operation['id']}")
    if presentation_id not in known_ids:
        raise ValueError(f"presentations.batchUpdate requires prior presentations.get or same-plan presentations.create for {presentation_id}")
    requests = require_list(batch, "requests")
    allowed = set(batch_policy["allowed_request_keys"])
    for request in requests:
        key = request_key(request, str(operation["id"]))
        if key not in allowed:
            raise ValueError(f"unsupported batchUpdate request key for {operation['id']}: {key}")
    write_control = batch.get("write_control")
    if write_control is not None:
        if not isinstance(write_control, dict):
            raise ValueError(f"batch_update.write_control must be an object for {operation['id']}")
        revision = str(write_control.get("requiredRevisionId", "")).strip()
        if not revision:
            raise ValueError(f"write_control.requiredRevisionId must be non-empty for {operation['id']}")
    validate_confirmation(operation, batch, schema, confirmation_policy)


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> None:
    schema = assets["schema"]
    require_fields(data, schema["required_root_fields"], "root")
    if data["mcp_server"] not in schema["allowed_mcp_servers"]:
        raise ValueError(f"unsupported mcp_server: {data['mcp_server']}")
    if data["operation_mode"] not in schema["allowed_operation_modes"]:
        raise ValueError(f"unsupported operation_mode: {data['operation_mode']}")

    operations = require_list(data, "operations")
    tools = mcp_tools(assets["mcp_contract"])
    profiles = scope_profiles(assets["scope_policy"])
    operation_ids: set[str] = set()
    known_presentation_ids: set[str] = set()

    for operation in operations:
        if not isinstance(operation, dict):
            raise ValueError("each operation must be an object")
        require_fields(operation, schema["required_operation_fields"], "operation")
        if operation["id"] in operation_ids:
            raise ValueError(f"duplicate operation id: {operation['id']}")
        operation_ids.add(str(operation["id"]))
        if operation["action"] not in schema["allowed_actions"]:
            raise ValueError(f"unsupported action for {operation['id']}: {operation['action']}")
        validate_tool(operation, tools)
        validate_scope(operation, profiles)

        action = operation["action"]
        if action == "presentations.create":
            created_id = validate_create(operation, schema, assets["confirmation_policy"])
            if created_id:
                known_presentation_ids.add(created_id)
        elif action == "presentations.get":
            known_presentation_ids.add(validate_get(operation, schema))
        elif action == "presentations.pages.get":
            validate_page_get(operation, schema, known_presentation_ids)
        elif action == "presentations.pages.getThumbnail":
            validate_thumbnail(operation, schema, assets["thumbnail_policy"], known_presentation_ids)
        elif action == "presentations.batchUpdate":
            validate_batch_update(
                operation,
                schema,
                assets["confirmation_policy"],
                assets["batch_policy"],
                known_presentation_ids,
            )

    validate_read_only_first(data, schema)
    evidence = require_object(data, "evidence")
    require_fields(evidence, schema["required_evidence_fields"], "evidence")
    if evidence.get("compiler_mode") not in {None, "offline_only"}:
        raise ValueError("evidence.compiler_mode must be offline_only when provided")


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [DOC] {key}: {value}" for key, value in sorted(evidence.items()))


def mcp_preflight_lines(data: dict[str, Any], contract: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"- [CODE] Server expected: `{contract['server']}`.",
            f"- [CODE] Tool tier expected: `{contract['tool_tier']}`.",
            "- [CODE] Check local `.mcp.json` before live execution.",
            "- [CODE] This compiled plan is offline and does not call Slides, OAuth, network, or MCP.",
            f"- [CODE] Requested operation mode: `{data['operation_mode']}`.",
        ]
    )


def operation_table(data: dict[str, Any]) -> str:
    lines = ["| ID | Action | MCP Tool | Scope Profile | Confirmation |", "|---|---|---|---|---|"]
    for operation in data["operations"]:
        action = operation["action"]
        confirmation = "required" if action in {"presentations.create", "presentations.batchUpdate"} else "not-required"
        lines.append(
            f"| {operation['id']} | {action} | `{operation['mcp_tool']}` | "
            f"{operation['scope_profile']} | {confirmation} |"
        )
    return "\n".join(lines)


def scope_review_lines(data: dict[str, Any], scope_policy: dict[str, Any]) -> str:
    profiles = scope_profiles(scope_policy)
    seen: list[str] = []
    for operation in data["operations"]:
        profile_id = str(operation["scope_profile"])
        if profile_id not in seen:
            seen.append(profile_id)
    lines = ["| Scope Profile | OAuth Scope | Usage | Mutates | Use |", "|---|---|---|---|---|"]
    for profile_id in seen:
        profile = profiles[profile_id]
        lines.append(
            f"| {profile_id} | `{profile['scope']}` | {profile['usage']} | "
            f"{profile['mutation_allowed']} | {profile['use_when']} |"
        )
    return "\n".join(lines)


def safety_gate_lines(data: dict[str, Any], confirmation_policy: dict[str, Any]) -> str:
    ro = data["read_only_first"]
    lines = [
        f"- [CODE] Read-only-first status: `{ro['status']}`.",
        f"- [CODE] Read-only-first checks: {', '.join(ro['checks'])}.",
        f"- [CODE] Mutation confirmation prefix: `{confirmation_policy['confirmation_phrase_prefix']}`.",
    ]
    for operation in data["operations"]:
        if operation["action"] == "presentations.create":
            confirmation = operation["create"]["human_confirmation"]
            lines.append(f"- [CODE] `{operation['id']}` confirmation: `{confirmation['status']}` by `{confirmation['confirmed_by']}`.")
        if operation["action"] == "presentations.batchUpdate":
            confirmation = operation["batch_update"]["human_confirmation"]
            lines.append(f"- [CODE] `{operation['id']}` confirmation: `{confirmation['status']}` by `{confirmation['confirmed_by']}`.")
    return "\n".join(lines)


def rest_payload_for_operation(operation: dict[str, Any]) -> dict[str, Any]:
    action = operation["action"]
    if action == "presentations.create":
        create = operation["create"]
        body = dict(create.get("body", {"title": create["title"]}))
        if create.get("presentation_id") and "presentationId" not in body:
            body["presentationId"] = create["presentation_id"]
        return {"method": "POST", "path": "/v1/presentations", "body": body}
    if action == "presentations.get":
        presentation_id = operation["get"]["presentation_id"]
        return {"method": "GET", "path": f"/v1/presentations/{presentation_id}", "body": None}
    if action == "presentations.pages.get":
        item = operation["page_get"]
        return {
            "method": "GET",
            "path": f"/v1/presentations/{item['presentation_id']}/pages/{item['page_object_id']}",
            "body": None,
        }
    if action == "presentations.pages.getThumbnail":
        item = operation["thumbnail"]
        query = {
            "thumbnailProperties.mimeType": item.get("mime_type", "PNG"),
            "thumbnailProperties.thumbnailSize": item["thumbnail_size"],
        }
        return {
            "method": "GET",
            "path": f"/v1/presentations/{item['presentation_id']}/pages/{item['page_object_id']}/thumbnail",
            "query": query,
            "body": None,
        }
    batch = operation["batch_update"]
    body: dict[str, Any] = {"requests": batch["requests"]}
    if "write_control" in batch:
        body["writeControl"] = batch["write_control"]
    return {
        "method": "POST",
        "path": f"/v1/presentations/{batch['presentation_id']}:batchUpdate",
        "body": body,
    }


def payload_preview(data: dict[str, Any]) -> str:
    payloads = {operation["id"]: rest_payload_for_operation(operation) for operation in data["operations"]}
    return "```json\n" + json.dumps(payloads, indent=2, sort_keys=True) + "\n```"


def live_checklist_lines(data: dict[str, Any]) -> str:
    lines = [
        "1. [CODE] Verify `workspace-mcp` is connected and exposes the mapped Slides tools.",
        "2. [CODE] Confirm OAuth grant matches the scope profile in this plan.",
        "3. [CODE] Run read-only operations before mutating calls.",
    ]
    step = 4
    for operation in data["operations"]:
        if operation["action"] in {"presentations.create", "presentations.batchUpdate"}:
            lines.append(f"{step}. [CODE] Re-confirm `{operation['id']}` with the user before live MCP execution.")
            step += 1
    lines.append(f"{step}. [CODE] After live mutation, read back the presentation or page and compare against this plan.")
    return "\n".join(lines)


def validation_lines(data: dict[str, Any], schema: dict[str, Any]) -> str:
    actions = {operation["action"] for operation in data["operations"]}
    mutating = sorted(actions & set(schema["mutating_actions"]))
    return "\n".join(
        [
            "- [CODE] Structured input passed local schema and policy validation.",
            "- [CODE] All operations map to real Slides REST methods and declared MCP tools.",
            f"- [CODE] Actions covered: {', '.join(sorted(actions))}.",
            f"- [CODE] Mutating actions requiring confirmation: {', '.join(mutating) if mutating else 'none'}.",
            "- [CODE] The compiler performed no network, OAuth, Google Slides, or MCP calls.",
        ]
    )


def risk_lines(data: dict[str, Any]) -> str:
    risks = [
        "- [INFERENCE] Live execution can still fail because of OAuth grants, Drive ownership, domain policy, or missing file access.",
        "- [INFERENCE] The offline plan validates request shape and sequence; it does not prove that live presentation IDs exist.",
        "- [ASSUMPTION] IDs, revision IDs, and confirmation text in the input came from a trusted user or a prior read-only discovery step.",
    ]
    if any(operation["action"] == "presentations.pages.getThumbnail" for operation in data["operations"]):
        risks.append("- [DOC] Thumbnail `contentUrl` is temporary and requester-scoped; do not persist it.")
    return "\n".join(risks)


def render(data: dict[str, Any], base: Path, assets: dict[str, dict[str, Any]]) -> str:
    template = (base / "assets" / "google-slides-operation-template.md").read_text(encoding="utf-8")
    replacements = {
        "{{SUMMARY}}": f"- [CODE] Plan `{data['request_id']}` covers `{data['request_title']}`.",
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{MCP_PREFLIGHT}}": mcp_preflight_lines(data, assets["mcp_contract"]),
        "{{OPERATION_TABLE}}": operation_table(data),
        "{{SCOPE_REVIEW}}": scope_review_lines(data, assets["scope_policy"]),
        "{{SAFETY_GATES}}": safety_gate_lines(data, assets["confirmation_policy"]),
        "{{PAYLOAD_PREVIEW}}": payload_preview(data),
        "{{LIVE_CHECKLIST}}": live_checklist_lines(data),
        "{{VALIDATION}}": validation_lines(data, assets["schema"]),
        "{{RISKS}}": risk_lines(data),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def load_assets(base: Path) -> dict[str, dict[str, Any]]:
    return {
        "schema": load_json(base / "assets" / "google-slides-mcp-schema.json"),
        "mcp_contract": load_json(base / "assets" / "mcp-tool-contract.json"),
        "scope_policy": load_json(base / "assets" / "scope-policy.json"),
        "confirmation_policy": load_json(base / "assets" / "human-confirmation-policy.json"),
        "batch_policy": load_json(base / "assets" / "slides-batchupdate-request-policy.json"),
        "thumbnail_policy": load_json(base / "assets" / "thumbnail-policy.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an offline Google Slides MCP plan")
    parser.add_argument("--input", required=True, help="Structured Google Slides MCP JSON")
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
