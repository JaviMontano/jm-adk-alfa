#!/usr/bin/env python3
"""Validate deterministic Message Batch orchestration reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "message-batch-orchestration"
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


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("message-batch-orchestration-contract.json")["json_contract"]
    workload_policy = policy("workload-policy.json")
    custom_id_policy = policy("custom-id-policy.json")
    lifecycle_policy = policy("lifecycle-policy.json")
    retry_policy_asset = policy("retry-fragmentation-policy.json")
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

    workload = report.get("workload")
    if not isinstance(workload, dict):
        errors.append("workload must be an object")
        workload = {}
    else:
        if workload.get("mode") not in workload_policy["allowed_modes"]:
            errors.append("workload.mode must be offline")
        for field, expected in workload_policy["required_flags"].items():
            if workload.get(field) is not expected:
                errors.append(f"workload.{field} must be {expected}")
        if not isinstance(workload.get("item_count"), int) or workload.get("item_count", 0) < workload_policy["minimum_item_count"]:
            errors.append("workload.item_count must be at least 2")
        if not non_empty_string(workload.get("business_id_field")):
            errors.append("workload.business_id_field must be non-empty")

    request_modeling = report.get("request_modeling")
    custom_ids: list[str] = []
    if not isinstance(request_modeling, dict):
        errors.append("request_modeling must be an object")
        request_modeling = {}
    else:
        for field in custom_id_policy["required_fields"]:
            if field not in request_modeling:
                errors.append(f"request_modeling missing field {field}")
        custom_id_source = request_modeling.get("custom_id_source")
        if not non_empty_string(custom_id_source):
            errors.append("request_modeling.custom_id_source must be non-empty")
        if custom_id_source in custom_id_policy["forbidden_sources"]:
            errors.append("request_modeling.custom_id_source must not be index-derived")
        if custom_id_source and workload.get("business_id_field") and custom_id_source != workload.get("business_id_field"):
            errors.append("request_modeling.custom_id_source must match workload.business_id_field")
        if request_modeling.get("uniqueness_validated") is not True:
            errors.append("request_modeling.uniqueness_validated must be true")
        if request_modeling.get("index_based_custom_id") is not False:
            errors.append("request_modeling.index_based_custom_id must be false")
        values = request_modeling.get("custom_ids")
        if not isinstance(values, list) or len(values) < 2:
            errors.append("request_modeling.custom_ids must contain at least two ids")
        else:
            for index, value in enumerate(values):
                if not non_empty_string(value):
                    errors.append(f"custom_ids[{index}] must be a non-empty string")
                else:
                    custom_ids.append(str(value))
            if len(set(custom_ids)) != len(custom_ids):
                errors.append("request_modeling.custom_ids must be unique")
            patterns = [re.compile(pattern) for pattern in custom_id_policy["index_like_patterns"]]
            if any(any(pattern.match(custom_id.lower()) for pattern in patterns) for custom_id in custom_ids):
                errors.append("request_modeling.custom_ids must not look index-derived")

    lifecycle = report.get("batch_lifecycle")
    if not isinstance(lifecycle, dict):
        errors.append("batch_lifecycle must be an object")
        lifecycle = {}
    else:
        if lifecycle.get("create_request_count") != len(custom_ids):
            errors.append("batch_lifecycle.create_request_count must equal number of custom_ids")
        for field, expected in lifecycle_policy["required_flags"].items():
            if lifecycle.get(field) is not expected:
                errors.append(f"batch_lifecycle.{field} must be {expected}")
        if lifecycle.get("terminal_status") != lifecycle_policy["terminal_status"]:
            errors.append("batch_lifecycle.terminal_status must be ended")
        backoff = lifecycle.get("polling_backoff_seconds")
        if not isinstance(backoff, list) or len(backoff) < lifecycle_policy["minimum_backoff_steps"]:
            errors.append("batch_lifecycle.polling_backoff_seconds must contain at least two steps")
        else:
            if any(not isinstance(value, int) or value <= 0 for value in backoff):
                errors.append("batch_lifecycle.polling_backoff_seconds must be positive integers")
            if backoff != sorted(backoff):
                errors.append("batch_lifecycle.polling_backoff_seconds must be nondecreasing")

    fragmentation = report.get("result_fragmentation")
    succeeded: set[str] = set()
    failed: set[str] = set()
    if not isinstance(fragmentation, dict):
        errors.append("result_fragmentation must be an object")
        fragmentation = {}
    else:
        succeeded_values = fragmentation.get("succeeded_custom_ids")
        failed_values = fragmentation.get("failed_custom_ids")
        if not isinstance(succeeded_values, list):
            errors.append("result_fragmentation.succeeded_custom_ids must be a list")
            succeeded_values = []
        if not isinstance(failed_values, list):
            errors.append("result_fragmentation.failed_custom_ids must be a list")
            failed_values = []
        succeeded = set(str(value) for value in succeeded_values)
        failed = set(str(value) for value in failed_values)
        known = set(custom_ids)
        if not succeeded.issubset(known):
            errors.append("succeeded_custom_ids must be a subset of custom_ids")
        if not failed.issubset(known):
            errors.append("failed_custom_ids must be a subset of custom_ids")
        if succeeded & failed:
            errors.append("succeeded and failed custom_ids must be disjoint")
        if succeeded | failed != known:
            errors.append("succeeded plus failed custom_ids must cover custom_ids")
        failure_types = fragmentation.get("failure_types")
        if not isinstance(failure_types, list):
            errors.append("result_fragmentation.failure_types must be a list")
            failure_types = []
        allowed_failures = set(retry_policy_asset["failure_result_types"])
        mapped_failures: set[str] = set()
        for index, item in enumerate(failure_types):
            if not isinstance(item, dict):
                errors.append(f"failure_types[{index}] must be an object")
                continue
            custom_id = item.get("custom_id")
            result_type = item.get("result_type")
            if custom_id not in failed:
                errors.append(f"failure_types[{index}].custom_id must be in failed_custom_ids")
            else:
                mapped_failures.add(str(custom_id))
            if result_type not in allowed_failures:
                errors.append(f"failure_types[{index}].result_type must be one of {sorted(allowed_failures)}")
        if mapped_failures != failed:
            errors.append("failure_types must cover every failed_custom_id")
        if fragmentation.get("success_persisted") is not True:
            errors.append("result_fragmentation.success_persisted must be true")

    retry_policy = report.get("retry_policy")
    if not isinstance(retry_policy, dict):
        errors.append("retry_policy must be an object")
        retry_policy = {}
    else:
        for field, expected in retry_policy_asset["required_retry_flags"].items():
            if retry_policy.get(field) is not expected:
                errors.append(f"retry_policy.{field} must be {expected}")
        retry_ids = retry_policy.get("retry_custom_ids")
        if not isinstance(retry_ids, list):
            errors.append("retry_policy.retry_custom_ids must be a list")
            retry_ids = []
        retry_set = set(str(value) for value in retry_ids)
        if retry_set != failed:
            errors.append("retry_policy.retry_custom_ids must equal failed_custom_ids exactly")
        if retry_policy.get("max_retries") not in retry_policy_asset["allowed_max_retries"]:
            errors.append("retry_policy.max_retries must be 1, 2, or 3")
        attempts = retry_policy.get("retry_attempts_used")
        if not isinstance(attempts, int) or attempts < 0:
            errors.append("retry_policy.retry_attempts_used must be a non-negative integer")
        elif isinstance(retry_policy.get("max_retries"), int) and attempts > retry_policy["max_retries"]:
            errors.append("retry_policy.retry_attempts_used must not exceed max_retries")

    persistence = report.get("persistence")
    if not isinstance(persistence, dict):
        errors.append("persistence must be an object")
        persistence = {}
    else:
        if not non_empty_string(persistence.get("success_sink")):
            errors.append("persistence.success_sink must be non-empty")
        if persistence.get("idempotent_writes") is not True:
            errors.append("persistence.idempotent_writes must be true")
        if persistence.get("preserves_successes_before_retry") is not True:
            errors.append("persistence.preserves_successes_before_retry must be true")

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
            "offline_gate_passed": True,
            "custom_ids_unique": True,
            "custom_ids_stable": True,
            "polls_until_ended": True,
            "fragments_results": True,
            "retries_only_failed_custom_ids": True,
            "retry_cap_enforced": True,
            "synchronous_loop_absent": True,
            "deterministic_script_passed": True,
        }
        for field, expected in expected_flags.items():
            if validation.get(field) is not expected:
                errors.append(f"validation.{field} must be {expected}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        if guardian.get("decision") not in contract["guardian_decisions"]:
            errors.append(f"guardian.decision must be one of {contract['guardian_decisions']}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")
        if guardian.get("decision") == "pass" and validation and validation.get("offline_gate_passed") is not True:
            errors.append("guardian must not pass when offline gate fails")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Message Batch orchestration JSON report")
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
