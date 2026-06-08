#!/usr/bin/env python3
"""Compile a deterministic Google Workspace API integration plan.

This script is intentionally offline. It reads local assets and fixtures only;
it never calls Google APIs, OAuth endpoints, network resources, or MCP tools.
"""

from __future__ import annotations

import argparse
import json
import re
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


def asset(name: str) -> Path:
    return skill_dir() / "assets" / name


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


def profile_map(auth_policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    profiles = auth_policy.get("profiles")
    if not isinstance(profiles, list):
        raise ValueError("auth-scope-policy profiles must be a list")
    return {str(profile["id"]): profile for profile in profiles if isinstance(profile, dict)}


def service_map(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    services = matrix.get("services")
    if not isinstance(services, dict):
        raise ValueError("workspace-service-matrix services must be an object")
    return services


def tool_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tools = contract.get("tools")
    if not isinstance(tools, dict):
        raise ValueError("mcp-tool-contract tools must be an object")
    return tools


def validate_root(data: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(data, schema["required_root_fields"], "root")
    if data["schema_version"] != schema["schema"]:
        raise ValueError(f"schema_version must be {schema['schema']}")
    project = require_object(data, "project")
    require_fields(project, schema["required_project_fields"], "project")
    if data["integration_mode"] not in schema["supported_integration_modes"]:
        raise ValueError(f"unsupported integration_mode: {data['integration_mode']}")


def validate_secrets(data: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any]) -> None:
    secrets = require_object(data, "secrets")
    require_fields(secrets, schema["required_secret_fields"], "secrets")
    allowed = policy["secrets"]["allowed_credential_storage"]
    if secrets["credential_storage"] not in allowed:
        raise ValueError(f"secrets.credential_storage must be one of {allowed}")
    if secrets["tokens_committed"] != policy["secrets"]["tokens_committed"]:
        raise ValueError("secrets.tokens_committed must be false")
    if secrets["api_keys_restricted"] != policy["secrets"]["api_keys_restricted"]:
        raise ValueError("secrets.api_keys_restricted must be true")


def validate_consent(data: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any]) -> None:
    consent = require_object(data, "human_consent")
    require_fields(consent, schema["required_human_consent_fields"], "human_consent")
    has_mutations = any(bool(service.get("mutation")) for service in data["services"])
    if not has_mutations:
        return
    expected = policy["human_consent"]["accepted_status"]
    if consent["status"] != expected:
        raise ValueError(f"mutating operations require human_consent.status={expected}")
    prefix = policy["human_consent"]["confirmation_text_prefix"]
    if not str(consent["confirmation_text"]).startswith(prefix):
        raise ValueError(f"human_consent.confirmation_text must start with {prefix}")
    if not str(consent["confirmed_by"]).strip():
        raise ValueError("human_consent.confirmed_by is required for mutating operations")


def operation_for(service: dict[str, Any], services: dict[str, dict[str, Any]]) -> dict[str, Any]:
    service_id = str(service["id"])
    operation_id = str(service["operation"])
    if service_id not in services:
        raise ValueError(f"unsupported service id: {service_id}")
    operations = services[service_id].get("operations", {})
    if operation_id not in operations:
        raise ValueError(f"unsupported operation for {service_id}: {operation_id}")
    operation = operations[operation_id]
    if not isinstance(operation, dict):
        raise ValueError(f"operation catalog entry must be an object: {service_id}.{operation_id}")
    return operation


def validate_profile(service: dict[str, Any], operation: dict[str, Any], profiles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    profile_id = str(service["auth_profile"])
    if profile_id not in profiles:
        raise ValueError(f"unknown auth_profile for {service['id']}: {profile_id}")
    profile = profiles[profile_id]
    if profile["service"] != service["id"]:
        raise ValueError(f"auth_profile {profile_id} belongs to {profile['service']}, not {service['id']}")
    if service["requested_scopes"] != profile["scopes"]:
        raise ValueError(f"requested_scopes must match auth_profile {profile_id}: {profile['scopes']}")
    if profile["access"] != operation["access"]:
        raise ValueError(
            f"auth_profile {profile_id} access {profile['access']} does not match operation access {operation['access']}"
        )
    return profile


def validate_mcp_tool(service: dict[str, Any], tools: dict[str, dict[str, Any]]) -> dict[str, Any]:
    tool_name = str(service["mcp_tool"])
    if tool_name not in tools:
        raise ValueError(f"unknown mcp_tool for {service['id']}: {tool_name}")
    tool = tools[tool_name]
    if tool["service"] != service["id"]:
        raise ValueError(f"mcp_tool {tool_name} belongs to {tool['service']}, not {service['id']}")
    if service["operation"] not in tool.get("operations", []):
        raise ValueError(f"mcp_tool {tool_name} cannot perform {service['operation']}")
    return tool


def validate_quota(service: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any]) -> None:
    quota = require_object(service, "quota_strategy")
    require_fields(quota, schema["required_quota_strategy_fields"], f"{service['id']}.quota_strategy")
    if not isinstance(quota["batching"], bool):
        raise ValueError(f"{service['id']}.quota_strategy.batching must be boolean")
    if not str(quota["partial_response_fields"]).strip():
        raise ValueError(f"{service['id']}.quota_strategy.partial_response_fields is required")
    if quota["retry_policy"] != policy["retry"]["default_policy"]:
        raise ValueError(f"{service['id']}.quota_strategy.retry_policy must be {policy['retry']['default_policy']}")


def validate_mutation(service: dict[str, Any], operation: dict[str, Any], schema: dict[str, Any]) -> None:
    if bool(service["mutation"]) != bool(operation["mutation"]):
        raise ValueError(f"{service['id']} mutation must match operation catalog for {service['operation']}")
    if not service["mutation"]:
        return
    if service.get("read_before_write") is not True:
        raise ValueError(f"{service['id']} {service['operation']} requires read_before_write=true")
    key = str(service.get("idempotency_key", ""))
    if not re.match(schema["idempotency_key_pattern"], key):
        raise ValueError(f"{service['id']} {service['operation']} requires stable idempotency_key")


def validate_services(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    schema = assets["schema"]
    services = service_map(assets["matrix"])
    profiles = profile_map(assets["auth"])
    tools = tool_map(assets["mcp"])
    validated: list[dict[str, Any]] = []
    seen = set()
    for index, service in enumerate(require_list(data, "services"), start=1):
        if not isinstance(service, dict):
            raise ValueError(f"services[{index}] must be an object")
        require_fields(service, schema["required_service_fields"], f"services[{index}]")
        dedupe_key = (service["id"], service["operation"], service["purpose"])
        if dedupe_key in seen:
            raise ValueError(f"duplicate service operation: {dedupe_key}")
        seen.add(dedupe_key)
        operation = operation_for(service, services)
        profile = validate_profile(service, operation, profiles)
        tool = validate_mcp_tool(service, tools)
        validate_quota(service, schema, assets["operation"])
        validate_mutation(service, operation, schema)
        if not require_object(service, "resource_identifiers"):
            raise ValueError(f"{service['id']} resource_identifiers must not be empty")
        validated.append({"service": service, "operation": operation, "profile": profile, "tool": tool})
    return validated


def validate_workflow(data: dict[str, Any], schema: dict[str, Any]) -> None:
    workflow = require_object(data, "workflow")
    require_fields(workflow, schema["required_workflow_fields"], "workflow")
    has_mutations = any(bool(service.get("mutation")) for service in data["services"])
    if has_mutations and workflow["read_only_first"] is not True:
        raise ValueError("workflow.read_only_first must be true for mutating workflows")
    if not isinstance(workflow["cross_service_steps"], list) or not workflow["cross_service_steps"]:
        raise ValueError("workflow.cross_service_steps must be a non-empty list")
    if not str(workflow["rollback_plan"]).strip():
        raise ValueError("workflow.rollback_plan is required")


def validate_test_matrix(data: dict[str, Any], policy: dict[str, Any]) -> None:
    matrix = require_list(data, "test_matrix")
    layers = {str(item.get("layer")) for item in matrix if isinstance(item, dict)}
    missing = [layer for layer in policy["required_validation_layers"] if layer not in layers]
    if missing:
        raise ValueError(f"test_matrix missing required layers: {missing}")
    for item in matrix:
        if not isinstance(item, dict):
            raise ValueError("test_matrix entries must be objects")
        require_fields(item, ["id", "layer", "covers"], "test_matrix item")
        if not isinstance(item["covers"], list) or not item["covers"]:
            raise ValueError(f"test_matrix {item['id']} covers must be non-empty")


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    validate_root(data, assets["schema"])
    validate_services_result = validate_services(data, assets)
    validate_workflow(data, assets["schema"])
    validate_consent(data, assets["schema"], assets["operation"])
    validate_secrets(data, assets["schema"], assets["operation"])
    validate_test_matrix(data, assets["operation"])
    if not require_object(data, "evidence"):
        raise ValueError("evidence must not be empty")
    return validate_services_result


def bullet(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def service_matrix_lines(validated: list[dict[str, Any]]) -> str:
    lines = []
    for item in validated:
        service = item["service"]
        operation = item["operation"]
        lines.append(
            "[CODE] "
            f"{service['id']} {service['operation']} {operation['method']} "
            f"access={operation['access']} mutation={str(operation['mutation']).lower()} "
            f"profile={service['auth_profile']} tool={service['mcp_tool']} "
            f"purpose={service['purpose']}"
        )
    return bullet(lines)


def auth_scope_lines(validated: list[dict[str, Any]]) -> str:
    lines = []
    for item in validated:
        service = item["service"]
        profile = item["profile"]
        lines.append(f"[DOC] {service['id']} uses {profile['id']} with scopes {', '.join(profile['scopes'])}")
    return bullet(lines)


def mcp_lines(validated: list[dict[str, Any]]) -> str:
    lines = []
    for item in validated:
        service = item["service"]
        lines.append(f"[CODE] {service['mcp_tool']} is mapped to {service['id']}:{service['operation']}")
    return bullet(lines)


def workflow_lines(workflow: dict[str, Any]) -> str:
    return "\n".join(f"{idx}. [CODE] {step}" for idx, step in enumerate(workflow["cross_service_steps"], start=1))


def retry_lines(validated: list[dict[str, Any]], policy: dict[str, Any]) -> str:
    lines = [
        f"[CONFIG] Retry policy: {policy['retry']['default_policy']}, max_attempts={policy['retry']['max_attempts']}",
        f"[CONFIG] Retryable statuses: {', '.join(str(s) for s in policy['retry']['retryable_statuses'])}",
    ]
    for item in validated:
        service = item["service"]
        if service["mutation"]:
            lines.append(f"[CODE] {service['id']} {service['operation']} idempotency_key={service['idempotency_key']}")
    return bullet(lines)


def secrets_lines(secrets: dict[str, Any], consent: dict[str, Any]) -> str:
    return bullet(
        [
            f"[CONFIG] credential_storage={secrets['credential_storage']}",
            f"[CONFIG] tokens_committed={str(secrets['tokens_committed']).lower()}",
            f"[CONFIG] api_keys_restricted={str(secrets['api_keys_restricted']).lower()}",
            f"[CONFIG] human_consent.status={consent['status']} confirmed_by={consent['confirmed_by']}",
        ]
    )


def validation_lines(matrix: list[dict[str, Any]]) -> str:
    return bullet(
        [
            f"[CODE] {item['layer']}:{item['id']} covers {', '.join(item['covers'])}"
            for item in matrix
            if isinstance(item, dict)
        ]
    )


def render(data: dict[str, Any], validated: list[dict[str, Any]]) -> str:
    template = asset("google-workspace-apis-template.md").read_text(encoding="utf-8")
    project = data["project"]
    workflow = data["workflow"]
    replacements = {
        "{{SUMMARY}}": (
            f"[CODE] {project['name']} uses {len(validated)} Workspace operations in "
            f"{data['integration_mode']} mode for: {project['objective']}"
        ),
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{SERVICE_MATRIX}}": service_matrix_lines(validated),
        "{{AUTH_SCOPE_PLAN}}": auth_scope_lines(validated),
        "{{MCP_MAPPING}}": mcp_lines(validated),
        "{{WORKFLOW_SEQUENCE}}": workflow_lines(workflow),
        "{{RETRY_IDEMPOTENCY}}": retry_lines(validated, load_json(asset("operation-policy.json"))),
        "{{SECRETS_CONSENT}}": secrets_lines(data["secrets"], data["human_consent"]),
        "{{VALIDATION_MATRIX}}": validation_lines(data["test_matrix"]),
        "{{RISKS}}": bullet(
            [
                "[INFERENCE] Offline validation does not prove OAuth grants, API enablement, quota, billing, or live resource permissions.",
                f"[CONFIG] Rollback plan: {workflow['rollback_plan']}",
            ]
        ),
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    return template


def load_assets() -> dict[str, dict[str, Any]]:
    return {
        "schema": load_json(asset("google-workspace-apis-schema.json")),
        "matrix": load_json(asset("workspace-service-matrix.json")),
        "auth": load_json(asset("auth-scope-policy.json")),
        "mcp": load_json(asset("mcp-tool-contract.json")),
        "operation": load_json(asset("operation-policy.json")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a Google Workspace APIs integration plan")
    parser.add_argument("--input", required=True, help="Input JSON plan")
    parser.add_argument("--output", help="Optional Markdown output path")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.input))
        assets = load_assets()
        validated = validate_input(data, assets)
        rendered = render(data, validated)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
