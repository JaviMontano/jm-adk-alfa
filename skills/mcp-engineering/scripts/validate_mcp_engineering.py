#!/usr/bin/env python3
"""Validate deterministic MCP engineering reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "mcp-engineering"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def policy(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def contains_forbidden_secret(value: Any, forbidden: list[str]) -> bool:
    if not isinstance(value, str):
        return False
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in forbidden)


def validate_env_values(report: dict[str, Any], secret_policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    env_pattern = re.compile(secret_policy["env_var_pattern"])
    forbidden = secret_policy["forbidden_literal_patterns"]
    mcp_config = report.get("mcp_config", {})
    servers = mcp_config.get("mcpServers") if isinstance(mcp_config, dict) else None
    if not isinstance(servers, dict) or not servers:
        return ["mcp_config.mcpServers must be a non-empty object"]

    env_refs: set[str] = set()
    for server_name, server in servers.items():
        if not isinstance(server, dict):
            errors.append(f"mcp_config.mcpServers.{server_name} must be an object")
            continue
        if not non_empty_string(server.get("command")):
            errors.append(f"mcp_config.mcpServers.{server_name}.command must be non-empty")
        env = server.get("env")
        if not isinstance(env, dict) or not env:
            errors.append(f"mcp_config.mcpServers.{server_name}.env must be a non-empty object")
            continue
        for key, value in env.items():
            if not re.match(r"^[A-Z][A-Z0-9_]*$", str(key)):
                errors.append(f"env key must be uppercase snake case: {key}")
            if not isinstance(value, str) or not env_pattern.match(value):
                errors.append(f"env value for {key} must use ${{ENV_VAR}} expansion")
            if contains_forbidden_secret(value, forbidden):
                errors.append(f"env value for {key} contains a forbidden literal secret marker")
            env_refs.add(str(key))

    credentials = report.get("credentials", {})
    declared_env = set(credentials.get("env_vars", [])) if isinstance(credentials.get("env_vars"), list) else set()
    if env_refs != declared_env:
        errors.append("credentials.env_vars must match env keys in mcp_config")
    return errors


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("mcp-engineering-contract.json")["json_contract"]
    scope_policy = policy("scope-policy.json")
    secret_policy = policy("secret-policy.json")
    error_policy = policy("typed-error-policy.json")
    retry_policy_asset = policy("client-retry-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    for field in ["report_id", "scenario"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")

    scope = report.get("scope_decision")
    if not isinstance(scope, dict):
        errors.append("scope_decision must be an object")
        scope = {}
    else:
        for field in scope_policy["required_fields"]:
            if field not in scope:
                errors.append(f"scope_decision missing field {field}")
        inheritance = scope.get("requested_inheritance")
        if inheritance not in scope_policy["allowed_inheritance"]:
            errors.append("scope_decision.requested_inheritance must be team or personal")
        else:
            expected = scope_policy["targets"][inheritance]
            if scope.get("config_target") != expected["config_target"]:
                errors.append(f"scope_decision.config_target must be {expected['config_target']} for {inheritance}")
            if scope.get("versioned") is not expected["versioned"]:
                errors.append(f"scope_decision.versioned must be {expected['versioned']} for {inheritance}")
        if not non_empty_string(scope.get("reason")):
            errors.append("scope_decision.reason must be non-empty")

    mcp_config = report.get("mcp_config")
    if not isinstance(mcp_config, dict):
        errors.append("mcp_config must be an object")
        mcp_config = {}
    else:
        if not non_empty_string(mcp_config.get("server_name")):
            errors.append("mcp_config.server_name must be non-empty")
        if mcp_config.get("config_path") != scope.get("config_target"):
            errors.append("mcp_config.config_path must match scope_decision.config_target")
        errors.extend(validate_env_values(report, secret_policy))

    credentials = report.get("credentials")
    if not isinstance(credentials, dict):
        errors.append("credentials must be an object")
        credentials = {}
    else:
        if not isinstance(credentials.get("env_vars"), list) or not credentials.get("env_vars"):
            errors.append("credentials.env_vars must be a non-empty list")
        if credentials.get("literal_secret_count") != 0:
            errors.append("credentials.literal_secret_count must be 0")
        if not isinstance(credentials.get("leaked_secret_detected"), bool):
            errors.append("credentials.leaked_secret_detected must be boolean")
        remediation = credentials.get("remediation_steps")
        if not isinstance(remediation, list):
            errors.append("credentials.remediation_steps must be a list")
            remediation = []
        if credentials.get("leaked_secret_detected") is True:
            required = set(secret_policy["required_leak_remediation_steps"])
            if not required.issubset(set(remediation)):
                errors.append("leaked secrets require rotate_provider_secret and purge_git_history_with_filter_repo")

    error_contract = report.get("error_contract")
    if not isinstance(error_contract, dict):
        errors.append("error_contract must be an object")
        error_contract = {}
    categories = error_contract.get("categories")
    if not isinstance(categories, list) or not categories:
        errors.append("error_contract.categories must be a non-empty list")
        categories = []
    seen_categories: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(categories):
        if not isinstance(item, dict):
            errors.append(f"error_contract.categories[{index}] must be an object")
            continue
        for field in error_policy["required_fields"]:
            if field not in item:
                errors.append(f"error category {index} missing field {field}")
        category = item.get("errorCategory")
        if category in seen_categories:
            errors.append(f"duplicate errorCategory: {category}")
        if isinstance(category, str):
            seen_categories[category] = item
        if not isinstance(item.get("isRetryable"), bool):
            errors.append(f"errorCategory {category} isRetryable must be boolean")
        retry_after = item.get("retryAfterSeconds")
        if retry_after is not None and (not isinstance(retry_after, int) or retry_after <= 0):
            errors.append(f"errorCategory {category} retryAfterSeconds must be null or positive integer")
        if not isinstance(item.get("http_statuses"), list) or not item.get("http_statuses"):
            errors.append(f"errorCategory {category} http_statuses must be a non-empty list")

    for category, expected in error_policy["required_categories"].items():
        item = seen_categories.get(category)
        if item is None:
            errors.append(f"missing required errorCategory: {category}")
            continue
        if item.get("isRetryable") is not expected["isRetryable"]:
            errors.append(f"errorCategory {category} isRetryable must be {expected['isRetryable']}")
        expected_retry_after = expected["retryAfterSeconds"]
        retry_after = item.get("retryAfterSeconds")
        if expected_retry_after is None and retry_after is not None:
            errors.append(f"errorCategory {category} retryAfterSeconds must be null")
        if expected_retry_after == "required_positive_integer" and (not isinstance(retry_after, int) or retry_after <= 0):
            errors.append(f"errorCategory {category} retryAfterSeconds must be a positive integer")
        if expected_retry_after == "nullable_or_positive_integer" and retry_after is not None and (
            not isinstance(retry_after, int) or retry_after <= 0
        ):
            errors.append(f"errorCategory {category} retryAfterSeconds must be null or positive integer")
    if error_contract.get("generic_error_string_allowed") is not False:
        errors.append("error_contract.generic_error_string_allowed must be false")

    retry_policy = report.get("retry_policy")
    if not isinstance(retry_policy, dict):
        errors.append("retry_policy must be an object")
        retry_policy = {}
    else:
        if retry_policy.get("owner") != retry_policy_asset["owner"]:
            errors.append("retry_policy.owner must be client")
        if retry_policy.get("max_attempts") not in retry_policy_asset["allowed_max_attempts"]:
            errors.append("retry_policy.max_attempts must be 2 or 3")
        for field, expected in retry_policy_asset["required_flags"].items():
            if retry_policy.get(field) is not expected:
                errors.append(f"retry_policy.{field} must be {expected}")
        if not non_empty_string(retry_policy.get("nonretryable_action")):
            errors.append("retry_policy.nonretryable_action must be non-empty")

    builtin_review = report.get("builtin_review")
    if not isinstance(builtin_review, dict):
        errors.append("builtin_review must be an object")
        builtin_review = {}
    else:
        if not isinstance(builtin_review.get("builtin_covers_need"), bool):
            errors.append("builtin_review.builtin_covers_need must be boolean")
        if not isinstance(builtin_review.get("checked_tools"), list) or not builtin_review.get("checked_tools"):
            errors.append("builtin_review.checked_tools must be a non-empty list")
        if not non_empty_string(builtin_review.get("justification")):
            errors.append("builtin_review.justification must be non-empty")
        if builtin_review.get("builtin_covers_need") is True:
            errors.append("MCP must not be provisioned when a built-in tool covers the need")

    evidence = report.get("evidence")
    accepted_evidence = set(evidence_policy["accepted_evidence_types"])
    if not isinstance(evidence, list) or len(evidence) < evidence_policy["minimum_evidence_items"]:
        errors.append(f"evidence must contain at least {evidence_policy['minimum_evidence_items']} items")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            if item.get("type") not in accepted_evidence:
                errors.append(f"evidence[{index}].type must be accepted")
            if not non_empty_string(item.get("detail")):
                errors.append(f"evidence[{index}].detail must be non-empty")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        expected_flags = {
            "scope_matches_inheritance": True,
            "env_var_expansion_only": True,
            "literal_secret_count": 0,
            "typed_error_categories_complete": True,
            "retry_policy_in_client": True,
            "builtin_not_sufficient": True,
            "deterministic_script_passed": True,
        }
        for field, expected in expected_flags.items():
            if validation.get(field) != expected:
                errors.append(f"validation.{field} must be {expected}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        if guardian.get("decision") not in contract["guardian_decisions"]:
            errors.append(f"guardian.decision must be one of {contract['guardian_decisions']}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")
        if guardian.get("decision") == "pass" and builtin_review.get("builtin_covers_need") is True:
            errors.append("guardian must not pass when built-in tools cover the need")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an MCP engineering JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON report")
    args = parser.parse_args()

    try:
        report = load_json(args.report)
        errors = validate(report)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
