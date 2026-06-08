#!/usr/bin/env python3
"""Validate deterministic GitHub Actions CI/CD plans."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


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


def string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(non_empty_string(item) for item in value)


def object_at(plan: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = plan.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def list_at(plan: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = plan.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return []
    return value


def validate(plan: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["plan must be a JSON object"]

    contract = policy("ci-workflow-contract.json")
    triggers_policy = policy("triggers-policy.json")
    permissions_policy = policy("permissions-policy.json")
    pinning_policy = policy("action-pinning-policy.json")
    cache_policy = policy("cache-policy.json")
    matrix_policy = policy("matrix-policy.json")
    secrets_policy = policy("secrets-policy.json")
    deployment_policy = policy("deployment-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in plan:
            errors.append(f"missing required field: {field}")

    if plan.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if plan.get("skill") != "github-actions-ci":
        errors.append("skill must be github-actions-ci")
    if not non_empty_string(plan.get("scenario_id")):
        errors.append("scenario_id must be a non-empty string")
    if plan.get("decision") not in contract["json_contract"]["allowed_decisions"]:
        errors.append(f"decision must be one of {contract['json_contract']['allowed_decisions']}")

    triggers = list_at(plan, "triggers", errors)
    allowed_events = set(triggers_policy["allowed_events"])
    for event in triggers:
        if event not in allowed_events:
            errors.append(f"unsupported trigger: {event}")

    permissions = object_at(plan, "permissions", errors)
    default_permissions = permissions.get("default")
    if not isinstance(default_permissions, dict):
        errors.append("permissions.default must be an object")
    elif default_permissions.get("contents") != "read":
        errors.append("permissions.default.contents must be read")
    if permissions.get("mode") in permissions_policy["blocked_without_justification"] and not non_empty_string(permissions.get("justification")):
        errors.append("write-all permissions require explicit justification")
    if plan.get("decision") == "ready" and permissions.get("mode") == "write-all":
        errors.append("ready plans cannot use write-all permissions")

    jobs = list_at(plan, "jobs", errors)
    if not jobs:
        errors.append("jobs must not be empty")
    job_ids: set[str] = set()
    deploy_job_ids: set[str] = set()
    for index, job in enumerate(jobs):
        if not isinstance(job, dict):
            errors.append(f"jobs[{index}] must be an object")
            continue
        job_id = job.get("id")
        if not non_empty_string(job_id):
            errors.append(f"jobs[{index}].id must be a non-empty string")
            job_id = f"jobs[{index}]"
        else:
            job_ids.add(job_id)
        for field in ["purpose", "runs_on"]:
            if not non_empty_string(job.get(field)):
                errors.append(f"job {job_id} missing {field}")
        if not string_list(job.get("commands")):
            errors.append(f"job {job_id} commands must be a non-empty list")
        if not isinstance(job.get("permissions"), dict):
            errors.append(f"job {job_id} permissions must be an object")
        if job.get("deploy") is True:
            deploy_job_ids.add(str(job_id))
        needs = job.get("needs", [])
        if needs is not None and not isinstance(needs, list):
            errors.append(f"job {job_id} needs must be a list")

    actions = list_at(plan, "actions", errors)
    sha_pattern = re.compile(pinning_policy["immutable_ref_pattern"])
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            errors.append(f"actions[{index}] must be an object")
            continue
        name = action.get("name")
        ref = action.get("ref")
        if not non_empty_string(name) or not non_empty_string(ref):
            errors.append(f"actions[{index}] requires name and ref")
            continue
        required_pin = action.get("required_pin") is True
        is_third_party = not any(str(name).startswith(prefix) for prefix in pinning_policy["official_prefixes"])
        if required_pin or is_third_party:
            if not sha_pattern.match(str(ref)):
                errors.append(f"action {name} must use immutable 40-character SHA ref")

    cache = object_at(plan, "cache", errors)
    if cache.get("enabled") is True:
        if not non_empty_string(cache.get("key")):
            errors.append("cache.key must be non-empty when cache is enabled")
        invalidation = cache.get("invalidation_source")
        if invalidation not in cache_policy["accepted_invalidation_sources"]:
            errors.append("cache.invalidation_source must be an accepted dependency file")
    elif cache.get("enabled") is not False:
        errors.append("cache.enabled must be boolean")

    matrix = object_at(plan, "matrix", errors)
    if matrix.get("enabled") is True:
        dimensions = matrix.get("dimensions")
        max_combinations = matrix.get("max_combinations")
        if not isinstance(dimensions, dict) or not dimensions:
            errors.append("matrix.dimensions must be a non-empty object when enabled")
        if not isinstance(max_combinations, int) or max_combinations < 1:
            errors.append("matrix.max_combinations must be a positive integer")
        elif max_combinations > matrix_policy["max_total_combinations"]:
            errors.append(f"matrix.max_combinations must be <= {matrix_policy['max_total_combinations']}")
    elif matrix.get("enabled") is not False:
        errors.append("matrix.enabled must be boolean")

    secrets = list_at(plan, "secrets", errors)
    blocked_secret_patterns = [re.compile(pattern) for pattern in secrets_policy["blocked_value_patterns"]]
    for index, secret in enumerate(secrets):
        if not isinstance(secret, dict):
            errors.append(f"secrets[{index}] must be an object")
            continue
        for field in secrets_policy["required_fields_when_used"]:
            if not non_empty_string(secret.get(field)):
                errors.append(f"secret entry {index} missing {field}")
        value = secret.get("value")
        if value is not None:
            value_text = str(value)
            if value_text:
                errors.append(f"secret {secret.get('name', index)} must not include inline value")
                if any(pattern.search(value_text) for pattern in blocked_secret_patterns):
                    errors.append(f"secret {secret.get('name', index)} resembles a credential value")

    deployment = object_at(plan, "deployment", errors)
    deployment_enabled = deployment.get("enabled")
    if deployment_enabled is True:
        for field in deployment_policy["required_fields_when_enabled"]:
            value = deployment.get(field)
            if field == "needs":
                if not string_list(value):
                    errors.append("deployment.needs must be a non-empty list when enabled")
            elif not non_empty_string(value):
                errors.append(f"deployment.{field} must be non-empty when enabled")
        if any(event in triggers for event in deployment_policy["blocked_events"]):
            if deployment.get("production_from_pull_request") is True:
                errors.append("production deploy must not run from pull_request")
        for needed_job in deployment.get("needs", []) if isinstance(deployment.get("needs"), list) else []:
            if needed_job not in job_ids:
                errors.append(f"deployment.needs references missing job: {needed_job}")
        if not deploy_job_ids:
            errors.append("deployment.enabled requires at least one job with deploy=true")
    elif deployment_enabled is not False:
        errors.append("deployment.enabled must be boolean")

    validation = object_at(plan, "validation", errors)
    for field in evidence_policy["required_validation_fields"]:
        if not string_list(validation.get(field)):
            errors.append(f"validation.{field} must be a non-empty list")
    if plan.get("decision") == "ready" and errors:
        errors.append("ready decision is invalid while validation errors exist")

    guardian = object_at(plan, "guardian", errors)
    if guardian.get("decision") not in {"pass", "warn", "block"}:
        errors.append("guardian.decision must be pass, warn, or block")
    if plan.get("decision") == "ready" and guardian.get("decision") != "pass":
        errors.append("ready plan requires guardian.decision=pass")
    if plan.get("decision") == "blocked" and guardian.get("decision") != "block":
        errors.append("blocked plan requires guardian.decision=block")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GitHub Actions CI/CD JSON plan")
    parser.add_argument("plan", type=Path, help="Path to a JSON CI/CD plan")
    args = parser.parse_args()

    try:
        plan = load_json(args.plan)
        errors = validate(plan)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.plan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
