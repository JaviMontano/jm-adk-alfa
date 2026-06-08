#!/usr/bin/env python3
"""Validate deterministic runtime-routing reports."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


SKILL = "runtime-routing"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def set_path(data: Any, dotted_path: str, value: Any) -> None:
    cursor = data
    parts = dotted_path.split(".")
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    last = parts[-1]
    if isinstance(cursor, list):
        cursor[int(last)] = value
    else:
        cursor[last] = value


def evidence_valid(report: dict[str, Any], evidence_policy: dict[str, Any]) -> tuple[bool, set[str]]:
    evidence = report.get("evidence")
    if not isinstance(evidence, list):
        return False, set()
    ids: set[str] = set()
    verified = 0
    ok = True
    for item in evidence:
        if not isinstance(item, dict):
            ok = False
            continue
        for field in evidence_policy["required_fields"]:
            if field not in item:
                ok = False
        if item.get("source_type") not in evidence_policy["allowed_source_types"]:
            ok = False
        if not non_empty_string(item.get("locator")):
            ok = False
        if item.get("verified") is not True:
            ok = False
        if non_empty_string(item.get("id")):
            ids.add(str(item["id"]))
        if item.get("verified") is True:
            verified += 1
    return ok and verified >= evidence_policy["minimum_verified_evidence"], ids


def matrix_valid(report: dict[str, Any], ids: set[str], catalog: dict[str, Any], matrix_policy: dict[str, Any]) -> tuple[bool, dict[str, Any] | None]:
    task = report.get("task")
    if not isinstance(task, dict):
        return False, None
    for field in matrix_policy["required_task_fields"]:
        if field not in task:
            return False, None
    required = set(task.get("required_capabilities", [])) if isinstance(task.get("required_capabilities"), list) else set()
    matrix = report.get("capability_matrix")
    if not isinstance(matrix, list) or not matrix:
        return False, None
    recommendation = report.get("recommendation") if isinstance(report.get("recommendation"), dict) else {}
    rec_runtime = recommendation.get("runtime")
    rec_entry = None
    ok = True
    for entry in matrix:
        if not isinstance(entry, dict):
            ok = False
            continue
        for field in matrix_policy["required_fields"]:
            if field not in entry:
                ok = False
        runtime = entry.get("runtime")
        if runtime not in catalog["allowed_runtimes"]:
            ok = False
        if entry.get("validation_status") not in matrix_policy["allowed_validation_statuses"]:
            ok = False
        if entry.get("permission_level") not in catalog["allowed_permission_levels"]:
            ok = False
        evidence_ids = entry.get("evidence_ids")
        if entry.get("validation_status") == "verified":
            if not isinstance(evidence_ids, list) or not evidence_ids:
                ok = False
            elif any(evidence_id not in ids for evidence_id in evidence_ids):
                ok = False
        capabilities = set(entry.get("capabilities", [])) if isinstance(entry.get("capabilities"), list) else set()
        if runtime == rec_runtime:
            rec_entry = entry
            if not required.issubset(capabilities):
                ok = False
    return ok and rec_entry is not None, rec_entry


def fallback_valid(report: dict[str, Any], fallback_policy: dict[str, Any]) -> bool:
    fallback = report.get("fallback")
    if not isinstance(fallback, dict):
        return False
    for field in fallback_policy["required_fields"]:
        if field not in fallback:
            return False
    return (
        fallback.get("local_first") is True
        and non_empty_string(fallback.get("path"))
        and fallback.get("missing_data_handling") in fallback_policy["allowed_missing_data_handling"]
        and isinstance(fallback.get("validation_limits"), list)
        and bool(fallback["validation_limits"])
    )


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("runtime-routing-contract.json")["json_contract"]
    catalog = asset("runtime-catalog-policy.json")
    evidence_policy = asset("evidence-policy.json")
    matrix_policy = asset("capability-matrix-policy.json")
    fallback_policy = asset("fallback-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("route_id")):
        errors.append("route_id must be non-empty")

    evidence_ok, ids = evidence_valid(report, evidence_policy)
    matrix_ok, rec_entry = matrix_valid(report, ids, catalog, matrix_policy)
    recommendation = report.get("recommendation") if isinstance(report.get("recommendation"), dict) else {}
    fallback_ok = fallback_valid(report, fallback_policy)
    rec_verified = isinstance(rec_entry, dict) and rec_entry.get("validation_status") == "verified"
    validation_limits_visible = isinstance(recommendation.get("validation_limit_labels"), list) and bool(recommendation["validation_limit_labels"])
    lowest_permission = recommendation.get("permission_level") in catalog["allowed_permission_levels"] and recommendation.get("lowest_permission") is True

    checks = {
        "evidence_grounded": evidence_ok,
        "runtime_supported": matrix_ok and rec_verified,
        "lowest_permission_selected": lowest_permission,
        "fallback_defined": fallback_ok,
        "validation_limits_visible": validation_limits_visible,
        "deterministic_script_passed": True,
    }
    for field, ok in checks.items():
        if not ok:
            errors.append(f"{field} is false")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    for field, expected in checks.items():
        if validation.get(field) is not expected:
            errors.append(f"validation.{field} must be {expected}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
        guardian = {}
    decision = guardian.get("decision")
    if decision not in contract["guardian_decisions"]:
        errors.append("guardian.decision is not allowed")
    if not non_empty_string(guardian.get("reason")):
        errors.append("guardian.reason must be non-empty")
    blocking_needed = any(value is False for value in checks.values())
    if decision == "pass" and blocking_needed:
        errors.append("guardian pass requires all validation flags true")
    if decision == "block" and not blocking_needed:
        errors.append("guardian block requires validation failure")
    return errors


def run_fixture_suite(fixtures_dir: Path) -> tuple[int, int]:
    valid_count = 0
    for fixture in sorted(fixtures_dir.glob("valid-*.json")):
        errors = validate(load_json(fixture))
        if errors:
            raise AssertionError(f"{fixture.name} should pass: {errors}")
        valid_count += 1
    invalid_spec = load_json(fixtures_dir / "invalid-mutations.json")
    base = invalid_spec["base_report"]
    invalid_count = 0
    for case in invalid_spec["mutations"]:
        report = copy.deepcopy(base)
        for mutation in case["set"]:
            set_path(report, mutation["path"], mutation["value"])
        if not validate(report):
            raise AssertionError(f"{case['id']} should fail")
        invalid_count += 1
    return valid_count, invalid_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a runtime-routing JSON report")
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--fixture-suite", type=Path)
    args = parser.parse_args()
    try:
        if args.fixture_suite:
            valid_count, invalid_count = run_fixture_suite(args.fixture_suite)
            print(f"runtime-routing check passed: valid={valid_count} invalid={invalid_count}")
            return 0
        if args.report is None:
            raise ValueError("report path or --fixture-suite is required")
        errors = validate(load_json(args.report))
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
