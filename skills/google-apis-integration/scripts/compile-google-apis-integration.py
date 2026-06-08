#!/usr/bin/env python3
"""Compile a deterministic multi-service Google API integration plan.

This script is intentionally offline. It reads local assets and fixtures only;
it never calls Google APIs, OAuth, HTTP, network, or MCP tools.
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


def asset(name: str) -> Path:
    return skill_dir() / "assets" / name


def service_catalog(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    services = catalog.get("services")
    if not isinstance(services, dict):
        raise ValueError("service-catalog services must be an object")
    return services


def scope_profiles(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    profiles = policy.get("profiles")
    if not isinstance(profiles, list):
        raise ValueError("auth-scope-policy profiles must be a list")
    return {str(profile["id"]): profile for profile in profiles if isinstance(profile, dict)}


def retry_policies(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    policies = policy.get("retry_policies")
    if not isinstance(policies, dict):
        raise ValueError("error-retry-policy retry_policies must be an object")
    return policies


def validate_project(data: dict[str, Any], schema: dict[str, Any]) -> None:
    project = require_object(data, "project")
    require_fields(project, schema["required_project_fields"], "project")
    if data["integration_mode"] not in schema["supported_integration_modes"]:
        raise ValueError(f"unsupported integration_mode: {data['integration_mode']}")


def validate_consent(data: dict[str, Any], schema: dict[str, Any], consent_policy: dict[str, Any]) -> None:
    consent = require_object(data, "human_consent")
    require_fields(consent, schema["required_human_consent_fields"], "human_consent")
    has_mutations = any(bool(service.get("mutation")) for service in data["services"])
    if not has_mutations:
        return
    expected_status = consent_policy["human_consent"]["accepted_status"]
    if consent["status"] != expected_status:
        raise ValueError(f"mutating Google API operations require human_consent.status={expected_status}")
    prefix = consent_policy["human_consent"]["confirmation_text_prefix"]
    if not str(consent["confirmation_text"]).startswith(prefix):
        raise ValueError(f"human_consent.confirmation_text must start with {prefix}")


def validate_secrets(data: dict[str, Any], schema: dict[str, Any], consent_policy: dict[str, Any]) -> None:
    secrets = require_object(data, "secrets")
    require_fields(secrets, schema["required_secret_fields"], "secrets")
    allowed_storage = consent_policy["secrets"]["allowed_token_storage"]
    if secrets["token_storage"] not in allowed_storage:
        raise ValueError(f"secrets.token_storage must be one of {allowed_storage}")
    if secrets["client_secret_exposure"] != consent_policy["secrets"]["client_secret_exposure"]:
        raise ValueError("secrets.client_secret_exposure must be never")
    if secrets["maps_api_key_restriction"] != consent_policy["secrets"]["maps_api_key_restriction"]:
        raise ValueError("secrets.maps_api_key_restriction must be http_referrer_and_api_restricted")
    for field in consent_policy["secrets"]["required_true"]:
        if secrets.get(field) is not True:
            raise ValueError(f"secrets.{field} must be true")


def operation_for(service: dict[str, Any], services: dict[str, dict[str, Any]]) -> dict[str, Any]:
    service_id = str(service["id"])
    if service_id not in services:
        raise ValueError(f"unsupported service id: {service_id}")
    operations = services[service_id].get("operations", {})
    operation = str(service["operation"])
    if operation not in operations:
        raise ValueError(f"unsupported operation for {service_id}: {operation}")
    return operations[operation]


def validate_scope_profile(
    service: dict[str, Any],
    operation: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
    access_rank: dict[str, int],
) -> dict[str, Any]:
    profile_id = str(service["auth_profile"])
    if profile_id not in profiles:
        raise ValueError(f"unknown auth_profile for {service['id']}: {profile_id}")
    profile = profiles[profile_id]
    if profile["service"] != service["id"]:
        raise ValueError(f"auth_profile {profile_id} belongs to {profile['service']}, not {service['id']}")
    expected_scopes = profile.get("scopes", [])
    if service["requested_scopes"] != expected_scopes:
        raise ValueError(f"requested_scopes must match auth_profile {profile_id}: {expected_scopes}")

    op_access = str(operation["access"])
    profile_access = str(profile["access"])
    if access_rank[profile_access] > access_rank[op_access]:
        raise ValueError(f"auth_profile {profile_id} is broader than needed for operation {service['operation']}")
    if profile.get("broad_by_default") and not service.get("scope_escalation_reason"):
        raise ValueError(f"auth_profile {profile_id} requires scope_escalation_reason")
    if profile.get("requires_key_restrictions"):
        api_key_policy = require_object(service, "api_key_policy")
        if api_key_policy.get("restricted") is not True:
            raise ValueError(f"{service['id']} requires api_key_policy.restricted=true")
        if not api_key_policy.get("allowed_apis"):
            raise ValueError(f"{service['id']} requires api_key_policy.allowed_apis")
    return profile


def validate_quota_strategy(service: dict[str, Any], schema: dict[str, Any]) -> None:
    quota = require_object(service, "quota_strategy")
    require_fields(quota, schema["required_quota_strategy_fields"], f"{service['id']}.quota_strategy")
    if not isinstance(quota["batching"], bool):
        raise ValueError(f"{service['id']}.quota_strategy.batching must be boolean")
    if not str(quota["partial_response_fields"]).strip():
        raise ValueError(f"{service['id']}.quota_strategy.partial_response_fields must be non-empty")
    if not str(quota["quota_user_or_key_restriction"]).strip():
        raise ValueError(f"{service['id']}.quota_strategy.quota_user_or_key_restriction must be non-empty")


def validate_idempotency(service: dict[str, Any], schema: dict[str, Any]) -> None:
    if not service["mutation"]:
        return
    key = str(service.get("idempotency_key", ""))
    if not key:
        raise ValueError(f"{service['id']} {service['operation']} requires idempotency_key")
    if not re.match(schema["idempotency_key_pattern"], key):
        raise ValueError(f"{service['id']} idempotency_key is not stable kebab-case: {key}")


def validate_services(
    data: dict[str, Any],
    schema: dict[str, Any],
    services: dict[str, dict[str, Any]],
    profiles: dict[str, dict[str, Any]],
    auth_policy: dict[str, Any],
    retry_policy: dict[str, Any],
) -> list[dict[str, Any]]:
    service_items = require_list(data, "services")
    policies = retry_policies(retry_policy)
    validated: list[dict[str, Any]] = []
    seen = set()
    for index, service in enumerate(service_items, start=1):
        if not isinstance(service, dict):
            raise ValueError(f"services[{index}] must be an object")
        require_fields(service, schema["required_service_fields"], f"services[{index}]")
        key = (service["id"], service["operation"], service["purpose"])
        if key in seen:
            raise ValueError(f"duplicate service operation: {key}")
        seen.add(key)

        operation = operation_for(service, services)
        if bool(service["mutation"]) != bool(operation["mutation"]):
            raise ValueError(f"{service['id']} mutation must match catalog operation {service['operation']}")
        profile = validate_scope_profile(service, operation, profiles, auth_policy["access_rank"])
        if service["retry_policy"] not in policies:
            raise ValueError(f"{service['id']} unknown retry_policy: {service['retry_policy']}")
        if service["mutation"] and service.get("read_before_write") is not True:
            raise ValueError(f"{service['id']} {service['operation']} requires read_before_write=true")
        validate_idempotency(service, schema)
        validate_quota_strategy(service, schema)
        resources = require_object(service, "resource_identifiers")
        if not resources:
            raise ValueError(f"{service['id']} resource_identifiers must not be empty")
        validated.append({"input": service, "operation": operation, "profile": profile})
    return validated


def validate_test_matrix(data: dict[str, Any], matrix_policy: dict[str, Any]) -> None:
    matrix = require_list(data, "test_matrix")
    layers = {str(item.get("layer")) for item in matrix if isinstance(item, dict)}
    missing = [layer for layer in matrix_policy["required_layers"] if layer not in layers]
    if missing:
        raise ValueError(f"test_matrix missing required layers: {missing}")
    for item in matrix:
        if not isinstance(item, dict):
            raise ValueError("test_matrix entries must be objects")
        require_fields(item, ["id", "layer", "covers"], f"test_matrix.{item}")
        if not isinstance(item["covers"], list) or not item["covers"]:
            raise ValueError(f"test_matrix {item['id']} covers must be a non-empty list")


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    schema = assets["schema"]
    require_fields(data, schema["required_root_fields"], "root")
    if data["schema_version"] != schema["schema"]:
        raise ValueError(f"schema_version must be {schema['schema']}")
    validate_project(data, schema)
    validated_services = validate_services(
        data=data,
        schema=schema,
        services=service_catalog(assets["catalog"]),
        profiles=scope_profiles(assets["auth"]),
        auth_policy=assets["auth"],
        retry_policy=assets["retry"],
    )
    validate_consent(data, schema, assets["consent"])
    validate_secrets(data, schema, assets["consent"])
    validate_test_matrix(data, assets["matrix"])
    evidence = require_object(data, "evidence")
    if not evidence:
        raise ValueError("evidence must not be empty")
    return validated_services


def bullet(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def service_checklist(validated: list[dict[str, Any]]) -> str:
    lines = []
    for item in validated:
        service = item["input"]
        operation = item["operation"]
        lines.append(
            "[DOC] `{}` uses `{}` `{}`; mutation={}; purpose: {}.".format(
                service["id"],
                operation["method"],
                service["operation"],
                str(service["mutation"]).lower(),
                service["purpose"],
            )
        )
        lines.append(f"[CODE] Resource identifiers: `{json.dumps(service['resource_identifiers'], sort_keys=True)}`.")
    return bullet(lines)


def auth_scope_plan(validated: list[dict[str, Any]]) -> str:
    lines = []
    for item in validated:
        service = item["input"]
        profile = item["profile"]
        scopes = service["requested_scopes"] or ["restricted-api-key/no-oauth-scope"]
        lines.append(f"[DOC] `{service['id']}` auth profile `{profile['id']}` uses `{', '.join(scopes)}`.")
        lines.append(f"[INFERENCE] Rationale: {profile['rationale']}")
    return bullet(lines)


def retry_idempotency_plan(validated: list[dict[str, Any]], retry_asset: dict[str, Any]) -> str:
    policies = retry_policies(retry_asset)
    lines = []
    for item in validated:
        service = item["input"]
        policy = policies[service["retry_policy"]]
        lines.append(
            "[DOC] `{}` uses retry policy `{}` with max_attempts={} and jitter={}.".format(
                service["id"],
                service["retry_policy"],
                policy["max_attempts"],
                str(policy["jitter"]).lower(),
            )
        )
        if service["mutation"]:
            lines.append(f"[CODE] `{service['id']}` idempotency key: `{service['idempotency_key']}`.")
        lines.append(f"[CODE] `{service['id']}` quota strategy: `{json.dumps(service['quota_strategy'], sort_keys=True)}`.")
    return bullet(lines)


def secrets_consent_plan(data: dict[str, Any]) -> str:
    consent = data["human_consent"]
    secrets = data["secrets"]
    lines = [
        f"[CODE] Human consent status: `{consent['status']}` by `{consent['confirmed_by']}`.",
        f"[CODE] Confirmation text: {consent['confirmation_text']}",
        f"[CODE] Token storage: `{secrets['token_storage']}`.",
        f"[CODE] Client secret exposure: `{secrets['client_secret_exposure']}`.",
        f"[CODE] API keys restricted: {secrets['api_keys_restricted']}.",
        f"[CODE] OAuth tokens server-side: {secrets['oauth_tokens_server_side']}.",
    ]
    return bullet(lines)


def api_specific_notes(validated: list[dict[str, Any]]) -> str:
    lines = []
    for item in validated:
        service = item["input"]
        operation = item["operation"]
        lines.append(f"[DOC] `{service['id']}` `{service['operation']}`: {operation['notes']}")
    return bullet(lines)


def test_matrix_lines(data: dict[str, Any]) -> str:
    lines = []
    for item in data["test_matrix"]:
        covers = ", ".join(item["covers"])
        lines.append(f"[CODE] `{item['layer']}` via `{item['id']}` covers: {covers}.")
    return bullet(lines)


def validation_lines(validated: list[dict[str, Any]]) -> str:
    mutation_count = sum(1 for item in validated if item["input"]["mutation"])
    return bullet(
        [
            "[CODE] Local schema validation passed.",
            "[CODE] Service catalog mapping passed.",
            "[CODE] Auth profile and requested scope validation passed.",
            f"[CODE] Mutating operation count: {mutation_count}.",
            "[CODE] Secrets, consent, retry, quota, idempotency, and test matrix gates passed.",
            "[CODE] No live Google, OAuth, HTTP, network, or MCP call was made.",
        ]
    )


def risks_lines() -> str:
    return bullet(
        [
            "[INFERENCE] Live execution still depends on enabled APIs, Google Cloud project policy, OAuth consent configuration, account access, quotas, and resource ACLs.",
            "[INFERENCE] Generated operations must be implemented with service-specific client libraries or REST calls outside this offline compiler.",
            "[INFERENCE] API behavior and quota policy can change; refresh official references before external publication or deployment approval.",
        ]
    )


def build_plan(data: dict[str, Any], assets: dict[str, dict[str, Any]], validated: list[dict[str, Any]]) -> dict[str, Any]:
    services = []
    for item in validated:
        service = item["input"]
        operation = item["operation"]
        profile = item["profile"]
        services.append(
            {
                "service": service["id"],
                "display_name": assets["catalog"]["services"][service["id"]]["display_name"],
                "operation": service["operation"],
                "method": operation["method"],
                "path": operation["path"],
                "mutation": service["mutation"],
                "auth_profile": profile["id"],
                "requested_scopes": service["requested_scopes"],
                "retry_policy": service["retry_policy"],
                "idempotency_key": service["idempotency_key"] if service["mutation"] else "",
                "quota_strategy": service["quota_strategy"],
                "resource_identifiers": service["resource_identifiers"],
            }
        )
    return {
        "plan_schema": assets["schema"]["plan_schema"],
        "skill": "google-apis-integration",
        "project": data["project"],
        "integration_mode": data["integration_mode"],
        "service_count": len(services),
        "mutation_count": sum(1 for service in services if service["mutation"]),
        "consent_gate": data["human_consent"]["status"],
        "services": services,
        "test_matrix": data["test_matrix"],
        "validation": {
            "offline": True,
            "schema_valid": True,
            "service_catalog_valid": True,
            "auth_scope_valid": True,
            "consent_valid": True,
            "secrets_valid": True,
            "test_matrix_valid": True,
        },
    }


def render_markdown(data: dict[str, Any], assets: dict[str, dict[str, Any]], validated: list[dict[str, Any]]) -> str:
    project = data["project"]
    summary = bullet(
        [
            f"[CODE] Project: `{project['name']}`.",
            f"[CODE] Owner: `{project['owner']}`.",
            f"[CODE] Environment: `{project['environment']}`.",
            f"[CODE] Integration mode: `{data['integration_mode']}`.",
            f"[CODE] Services planned: {len(validated)}.",
            f"[CODE] Mutating operations: {sum(1 for item in validated if item['input']['mutation'])}.",
        ]
    )
    replacements = {
        "{{SUMMARY}}": summary,
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{SERVICE_CHECKLIST}}": service_checklist(validated),
        "{{AUTH_SCOPE_PLAN}}": auth_scope_plan(validated),
        "{{RETRY_IDEMPOTENCY_PLAN}}": retry_idempotency_plan(validated, assets["retry"]),
        "{{SECRETS_CONSENT_PLAN}}": secrets_consent_plan(data),
        "{{API_SPECIFIC_NOTES}}": api_specific_notes(validated),
        "{{TEST_MATRIX}}": test_matrix_lines(data),
        "{{VALIDATION}}": validation_lines(validated),
        "{{RISKS}}": risks_lines(),
    }
    template = (skill_dir() / "assets" / "google-apis-integration-template.md").read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def load_assets() -> dict[str, dict[str, Any]]:
    return {
        "schema": load_json(asset("google-apis-integration-schema.json")),
        "catalog": load_json(asset("service-catalog.json")),
        "auth": load_json(asset("auth-scope-policy.json")),
        "retry": load_json(asset("error-retry-policy.json")),
        "consent": load_json(asset("consent-secrets-policy.json")),
        "matrix": load_json(asset("test-matrix-policy.json")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an offline Google APIs integration plan")
    parser.add_argument("--input", required=True, help="Path to input JSON fixture")
    parser.add_argument("--output", help="Write output to a file instead of stdout")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        assets = load_assets()
        data = load_json(Path(args.input))
        validated = validate_input(data, assets)
        if args.format == "json":
            rendered = json.dumps(build_plan(data, assets, validated), indent=2, sort_keys=True) + "\n"
        else:
            rendered = render_markdown(data, assets, validated)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
