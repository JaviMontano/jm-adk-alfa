#!/usr/bin/env python3
"""Compile a deterministic Google Drive MCP plan from structured JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WORKSPACE_PREFIX = "application/vnd.google-apps."


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


def validate_required(data: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def normalized_query(value: str) -> str:
    return " ".join(value.lower().replace("=", " = ").split())


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


def upload_types(upload_policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    types = upload_policy.get("upload_types", [])
    if not isinstance(types, list):
        raise ValueError("upload-policy upload_types must be a list")
    return {str(item["id"]): item for item in types if isinstance(item, dict)}


def validate_scope_for_action(operation: dict[str, Any], profiles: dict[str, dict[str, Any]]) -> None:
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
    allowed = tools[tool_name].get("actions", [])
    if operation["action"] not in allowed:
        raise ValueError(f"mcp_tool {tool_name} cannot perform {operation['action']}")


def validate_read_only_first(data: dict[str, Any], schema: dict[str, Any]) -> None:
    if data["read_only_first"] is not True:
        raise ValueError("read_only_first must be true")
    actions = [operation["action"] for operation in data["operations"]]
    if any(action in schema["mutating_actions"] for action in actions):
        first_action = actions[0]
        if first_action not in schema["read_only_actions"]:
            raise ValueError("mutating workflows must start with a read-only search/list or download/export operation")


def validate_search(
    operation: dict[str, Any],
    schema: dict[str, Any],
    query_policy: dict[str, Any],
) -> None:
    search = require_object(operation, "search")
    validate_required(search, schema["required_search_fields"], f"search for {operation['id']}")
    q_value = str(search["q"])
    if not q_value.strip():
        raise ValueError(f"search.q must be non-empty for {operation['id']}")
    if "trashed = false" not in normalized_query(q_value):
        raise ValueError(f"search.q must include trashed = false for {operation['id']}")
    fields = str(search["fields"])
    if "files(" not in fields or "id" not in fields or "name" not in fields:
        raise ValueError(f"search.fields must request partial files(id,name,...) fields for {operation['id']}")
    if search["corpora"] not in schema["allowed_corpora"]:
        raise ValueError(f"unsupported corpora for {operation['id']}: {search['corpora']}")
    if search["spaces"] not in schema["allowed_spaces"]:
        raise ValueError(f"unsupported spaces for {operation['id']}: {search['spaces']}")
    if not isinstance(search["page_size"], int) or search["page_size"] < 1:
        raise ValueError(f"search.page_size must be a positive integer for {operation['id']}")
    max_page = int(query_policy["requirements"]["page_size_max"])
    if search["page_size"] > max_page:
        raise ValueError(f"search.page_size exceeds {max_page} for {operation['id']}")
    if search["corpora"] == "allDrives" and not str(search.get("scope_reason", "")).strip():
        raise ValueError(f"corpora=allDrives requires scope_reason for {operation['id']}")


def validate_upload(
    operation: dict[str, Any],
    schema: dict[str, Any],
    upload_policy: dict[str, Any],
) -> None:
    upload = require_object(operation, "upload")
    validate_required(upload, schema["required_upload_fields"], f"upload for {operation['id']}")
    if upload["requires_human_confirmation"] is not True:
        raise ValueError(f"upload requires human confirmation for {operation['id']}")
    local_path = str(upload["local_path"])
    blocked = upload_policy["requirements"]["block_sensitive_local_patterns"]
    for pattern in blocked:
        if pattern in local_path or pattern in str(upload["filename"]):
            raise ValueError(f"upload path matches sensitive pattern {pattern} for {operation['id']}")
    types = upload_types(upload_policy)
    upload_type = str(upload["upload_type"])
    if upload_type not in types:
        raise ValueError(f"unsupported upload_type for {operation['id']}: {upload_type}")
    size_mb = float(upload["size_mb"])
    if size_mb > 5 and upload_type != "resumable":
        raise ValueError(f"files greater than 5 MB require uploadType=resumable for {operation['id']}")
    metadata = require_object(upload, "metadata")
    if metadata and not types[upload_type]["metadata_supported"]:
        raise ValueError(f"uploadType=media cannot include metadata for {operation['id']}")
    for field in ("id", "name", "mimeType"):
        if field not in str(upload["fields"]):
            raise ValueError(f"upload.fields must include {field} for {operation['id']}")


def workspace_export_supported(
    source_mime_type: str,
    export_mime_type: str,
    mime_map: dict[str, Any],
) -> bool:
    workspace = mime_map["workspace_mime_types"].get(source_mime_type)
    if not isinstance(workspace, dict):
        return False
    exports = workspace.get("exports", [])
    return any(item.get("mime_type") == export_mime_type for item in exports if isinstance(item, dict))


def validate_download_export(
    operation: dict[str, Any],
    schema: dict[str, Any],
    mime_map: dict[str, Any],
) -> None:
    download = require_object(operation, "download_export")
    validate_required(download, schema["required_download_export_fields"], f"download_export for {operation['id']}")
    if download["verify_can_download"] is not True:
        raise ValueError(f"download/export must verify canDownload for {operation['id']}")
    source_mime = str(download["source_mime_type"])
    is_workspace = source_mime.startswith(WORKSPACE_PREFIX) and source_mime != mime_map["folder_mime_type"]
    if is_workspace:
        export_mime = str(download.get("export_mime_type", ""))
        if not workspace_export_supported(source_mime, export_mime, mime_map):
            raise ValueError(f"unsupported export_mime_type for {source_mime} in {operation['id']}")
        if download.get("use_alt_media") is True:
            raise ValueError(f"Google Workspace files must use export, not alt=media, for {operation['id']}")
    else:
        if download.get("use_alt_media") is not True:
            raise ValueError(f"blob downloads must use alt=media semantics for {operation['id']}")


def validate_folder(operation: dict[str, Any], schema: dict[str, Any], mime_map: dict[str, Any]) -> None:
    folder = require_object(operation, "folder")
    validate_required(folder, schema["required_folder_fields"], f"folder for {operation['id']}")
    if folder["requires_human_confirmation"] is not True:
        raise ValueError(f"folder mutation requires human confirmation for {operation['id']}")
    if folder["folder_mime_type"] != mime_map["folder_mime_type"]:
        raise ValueError(f"folder_mime_type must be {mime_map['folder_mime_type']} for {operation['id']}")
    if not str(folder["parent_id"]).strip():
        raise ValueError(f"folder.parent_id must be set for {operation['id']}")
    for field in ("id", "name", "mimeType", "parents"):
        if field not in str(folder["fields"]):
            raise ValueError(f"folder.fields must include {field} for {operation['id']}")


def validate_share(
    operation: dict[str, Any],
    schema: dict[str, Any],
    sharing_policy: dict[str, Any],
) -> None:
    share = require_object(operation, "share")
    validate_required(share, schema["required_share_fields"], f"share for {operation['id']}")
    if share["requires_human_confirmation"] is not True:
        raise ValueError(f"sharing permissions require human confirmation for {operation['id']}")
    if share["verify_capability"] != sharing_policy["requirements"]["verify_capability"]:
        raise ValueError(f"share.verify_capability must be canShare for {operation['id']}")
    permission = require_object(share, "permission")
    validate_required(permission, schema["required_permission_fields"], f"permission for {operation['id']}")
    permission_type = str(permission["type"])
    role = str(permission["role"])
    if permission_type not in sharing_policy["permission_types"]:
        raise ValueError(f"unsupported permission.type for {operation['id']}: {permission_type}")
    if role not in sharing_policy["roles"]:
        raise ValueError(f"unsupported permission.role for {operation['id']}: {role}")
    if permission_type in {"user", "group"} and not str(permission.get("emailAddress", "")).strip():
        raise ValueError(f"user/group permission requires emailAddress for {operation['id']}")
    if permission_type == "domain" and not str(permission.get("domain", "")).strip():
        raise ValueError(f"domain permission requires domain for {operation['id']}")
    if permission_type in {"domain", "anyone"} and not str(share.get("reason", "")).strip():
        raise ValueError(f"{permission_type} permission requires explicit reason for {operation['id']}")
    for field in ("id", "type", "role"):
        if field not in str(share["fields"]):
            raise ValueError(f"share.fields must include {field} for {operation['id']}")


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> None:
    schema = assets["schema"]
    validate_required(data, schema["required_root_fields"], "root")
    if data["mcp_server"] not in schema["allowed_mcp_servers"]:
        raise ValueError(f"unsupported mcp_server: {data['mcp_server']}")
    if data["operation_mode"] not in schema["allowed_operation_modes"]:
        raise ValueError(f"unsupported operation_mode: {data['operation_mode']}")

    operations = require_list(data, "operations")
    operation_ids: set[str] = set()
    profiles = scope_profiles(assets["scope_policy"])
    tools = tool_contracts(assets["mcp_contract"])
    for operation in operations:
        if not isinstance(operation, dict):
            raise ValueError("each operation must be an object")
        validate_required(operation, schema["required_operation_fields"], "operation")
        if operation["id"] in operation_ids:
            raise ValueError(f"duplicate operation id: {operation['id']}")
        if operation["action"] not in schema["allowed_actions"]:
            raise ValueError(f"unsupported action for {operation['id']}: {operation['action']}")
        operation_ids.add(str(operation["id"]))
        validate_scope_for_action(operation, profiles)
        validate_tool_for_action(operation, tools)

    validate_read_only_first(data, schema)

    for operation in operations:
        action = operation["action"]
        if action == "search_list":
            validate_search(operation, schema, assets["query_policy"])
        elif action == "upload":
            validate_upload(operation, schema, assets["upload_policy"])
        elif action == "download_export":
            validate_download_export(operation, schema, assets["mime_map"])
        elif action == "organize_folder":
            validate_folder(operation, schema, assets["mime_map"])
        elif action == "share_permission":
            validate_share(operation, schema, assets["sharing_policy"])

    evidence = require_object(data, "evidence")
    validate_required(evidence, schema["required_evidence_fields"], "evidence")


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [DOC] {key}: {value}" for key, value in sorted(evidence.items()))


def mcp_preflight_lines(data: dict[str, Any], mcp_contract: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"- [CODE] Server expected: `{mcp_contract['server']}`.",
            f"- [CODE] Tool tier expected: `{mcp_contract['tool_tier']}`.",
            "- [CODE] Check local `.mcp.json` before live execution.",
            "- [CODE] This compiled plan is offline and does not call Drive, OAuth, or MCP.",
            "- [DOC] Human-in-the-loop confirmation is required before exposed tools perform sensitive operations.",
        ]
    )


def operation_table(data: dict[str, Any]) -> str:
    lines = ["| ID | Action | MCP Tool | Scope Profile | Confirmation |", "|---|---|---|---|---|"]
    for operation in data["operations"]:
        confirmation = confirmation_state(operation)
        lines.append(
            f"| {operation['id']} | {operation['action']} | `{operation['mcp_tool']}` | "
            f"{operation['scope_profile']} | {confirmation} |"
        )
    return "\n".join(lines)


def confirmation_state(operation: dict[str, Any]) -> str:
    for key in ("upload", "folder", "share"):
        if key in operation:
            return "required" if operation[key].get("requires_human_confirmation") else "not-required"
    return "not-required"


def search_contract_lines(data: dict[str, Any]) -> str:
    searches = [operation for operation in data["operations"] if operation["action"] == "search_list"]
    if not searches:
        return "- [CODE] No search/list operation supplied."
    lines: list[str] = []
    for operation in searches:
        search = operation["search"]
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] q: `{search['q']}`.",
                f"- [CODE] fields: `{search['fields']}`.",
                f"- [CODE] corpora: `{search['corpora']}`.",
                f"- [CODE] spaces: `{search['spaces']}`.",
                f"- [CODE] page size: {search['page_size']}.",
            ]
        )
    return "\n".join(lines)


def scope_plan_lines(data: dict[str, Any], scope_policy: dict[str, Any]) -> str:
    profiles = scope_profiles(scope_policy)
    seen = []
    for operation in data["operations"]:
        profile_id = operation["scope_profile"]
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


def upload_plan_lines(data: dict[str, Any]) -> str:
    uploads = [operation for operation in data["operations"] if operation["action"] == "upload"]
    if not uploads:
        return "- [CODE] No upload operation supplied."
    lines: list[str] = []
    for operation in uploads:
        upload = operation["upload"]
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] Local path: `{upload['local_path']}`.",
                f"- [CODE] Destination parent ID: `{upload['destination_parent_id']}`.",
                f"- [CODE] Filename: `{upload['filename']}`.",
                f"- [CODE] MIME type: `{upload['mime_type']}`.",
                f"- [CODE] uploadType={upload['upload_type']}.",
                f"- [CODE] Size MB: {upload['size_mb']}.",
                f"- [CODE] Human confirmation: {upload['requires_human_confirmation']}.",
            ]
        )
    return "\n".join(lines)


def download_export_plan_lines(data: dict[str, Any]) -> str:
    downloads = [operation for operation in data["operations"] if operation["action"] == "download_export"]
    if not downloads:
        return "- [CODE] No download/export operation supplied."
    lines: list[str] = []
    for operation in downloads:
        item = operation["download_export"]
        export = item.get("export_mime_type", "n/a")
        alt_media = item.get("use_alt_media", False)
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] File: `{item['file_name']}` (`{item['file_id']}`).",
                f"- [CODE] Source MIME type: `{item['source_mime_type']}`.",
                f"- [CODE] Export MIME type: `{export}`.",
                f"- [CODE] alt=media semantics: {alt_media}.",
                f"- [CODE] Destination path: `{item['destination_path']}`.",
                f"- [CODE] Verify canDownload: {item['verify_can_download']}.",
            ]
        )
    return "\n".join(lines)


def folder_plan_lines(data: dict[str, Any]) -> str:
    folders = [operation for operation in data["operations"] if operation["action"] == "organize_folder"]
    if not folders:
        return "- [CODE] No folder organization operation supplied."
    lines: list[str] = []
    for operation in folders:
        folder = operation["folder"]
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] Folder path: `{folder['folder_path']}`.",
                f"- [CODE] Parent ID: `{folder['parent_id']}`.",
                f"- [CODE] Folder MIME type: `{folder['folder_mime_type']}`.",
                f"- [CODE] Create missing: {folder['create_missing']}.",
                f"- [CODE] Human confirmation: {folder['requires_human_confirmation']}.",
            ]
        )
    return "\n".join(lines)


def sharing_plan_lines(data: dict[str, Any]) -> str:
    shares = [operation for operation in data["operations"] if operation["action"] == "share_permission"]
    if not shares:
        return "- [CODE] No sharing/permission operation supplied."
    lines: list[str] = []
    for operation in shares:
        share = operation["share"]
        permission = share["permission"]
        target = permission.get("emailAddress") or permission.get("domain") or permission["type"]
        lines.extend(
            [
                f"### {operation['id']}",
                f"- [CODE] File ID: `{share['file_id']}`.",
                f"- [CODE] Permission: type `{permission['type']}`, role `{permission['role']}`, target `{target}`.",
                f"- [CODE] Verify capability: `{share['verify_capability']}`.",
                f"- [CODE] Send notification email: {share['send_notification_email']}.",
                f"- [CODE] Human confirmation: {share['requires_human_confirmation']}.",
                f"- [INFERENCE] Permission changes should be executed only after the user confirms the exact target and role.",
            ]
        )
    return "\n".join(lines)


def validation_lines(data: dict[str, Any], schema: dict[str, Any]) -> str:
    actions = {operation["action"] for operation in data["operations"]}
    mutating = sorted(actions & set(schema["mutating_actions"]))
    return "\n".join(
        [
            "- [CODE] Structured input passed schema and policy validation.",
            "- [CODE] Read-only-first gate is true.",
            f"- [CODE] Operation actions covered: {', '.join(sorted(actions))}.",
            f"- [CODE] Mutating actions requiring confirmation: {', '.join(mutating) if mutating else 'none'}.",
            "- [CODE] Search/list operations require q, fields, trashed = false, spaces, corpora, and page size.",
            "- [CODE] Sharing operations require canShare verification and human confirmation.",
            "- [CODE] The compiler performed no network, OAuth, Drive, or MCP calls.",
        ]
    )


def risk_lines(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "- [INFERENCE] Live Drive execution can still fail because of OAuth scope, Shared Drive policy, file capabilities, or missing user access.",
            "- [INFERENCE] This plan does not prove that a Drive file exists; it only validates the requested operation contract.",
            "- [ASSUMPTION] File IDs, folder IDs, local paths, and recipient addresses in the input were supplied by a trusted user or a prior read-only discovery step.",
        ]
    )


def render(data: dict[str, Any], base: Path, assets: dict[str, dict[str, Any]]) -> str:
    template = (base / "assets" / "google-drive-mcp-template.md").read_text(encoding="utf-8")
    replacements = {
        "{{REQUEST_ID}}": str(data["request_id"]),
        "{{REQUEST_TITLE}}": str(data["request_title"]),
        "{{MCP_SERVER}}": str(data["mcp_server"]),
        "{{OPERATION_MODE}}": str(data["operation_mode"]),
        "{{DRIVE_SPACE}}": str(data["drive_space"]),
        "{{READ_ONLY_FIRST}}": str(data["read_only_first"]),
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{MCP_PREFLIGHT}}": mcp_preflight_lines(data, assets["mcp_contract"]),
        "{{OPERATION_TABLE}}": operation_table(data),
        "{{SEARCH_CONTRACT}}": search_contract_lines(data),
        "{{SCOPE_PLAN}}": scope_plan_lines(data, assets["scope_policy"]),
        "{{UPLOAD_PLAN}}": upload_plan_lines(data),
        "{{DOWNLOAD_EXPORT_PLAN}}": download_export_plan_lines(data),
        "{{FOLDER_PLAN}}": folder_plan_lines(data),
        "{{SHARING_PLAN}}": sharing_plan_lines(data),
        "{{VALIDATION}}": validation_lines(data, assets["schema"]),
        "{{RISKS}}": risk_lines(data),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def load_assets(base: Path) -> dict[str, dict[str, Any]]:
    return {
        "schema": load_json(base / "assets" / "google-drive-mcp-schema.json"),
        "query_policy": load_json(base / "assets" / "query-policy.json"),
        "scope_policy": load_json(base / "assets" / "scope-policy.json"),
        "upload_policy": load_json(base / "assets" / "upload-policy.json"),
        "sharing_policy": load_json(base / "assets" / "sharing-permission-policy.json"),
        "mime_map": load_json(base / "assets" / "mime-export-map.json"),
        "mcp_contract": load_json(base / "assets" / "mcp-tool-contract.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic Google Drive MCP plan")
    parser.add_argument("--input", required=True, help="Structured Google Drive MCP JSON")
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
