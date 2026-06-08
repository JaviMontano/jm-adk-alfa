#!/usr/bin/env python3
"""Validate deterministic self-correction-loops reports."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


SKILL = "self-correction-loops"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"
TOLERANCE = 1e-9


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


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


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


def epsilon_allowed(data_type: str, epsilon: Any, policy: dict[str, Any]) -> bool:
    if not is_number(epsilon) or epsilon < 0:
        return False
    if data_type == "integer":
        return epsilon == policy["integer_epsilon"]
    if data_type == "currency":
        return policy["currency_min_epsilon"] <= epsilon <= policy["currency_max_epsilon"]
    if data_type == "float":
        return policy["float_min_epsilon"] <= epsilon <= policy["float_max_epsilon"]
    return False


def field_specs_valid(report: dict[str, Any], cross_policy: dict[str, Any], epsilon_policy: dict[str, Any]) -> tuple[bool, dict[str, dict[str, Any]]]:
    fields = report.get("fields")
    if not isinstance(fields, list) or not fields:
        return False, {}
    specs: dict[str, dict[str, Any]] = {}
    ok = True
    for spec in fields:
        if not isinstance(spec, dict):
            ok = False
            continue
        for field in cross_policy["required_field_spec_fields"]:
            if field not in spec:
                ok = False
        name = spec.get("field")
        data_type = spec.get("data_type")
        if not non_empty_string(name) or name in specs:
            ok = False
            continue
        specs[str(name)] = spec
        if data_type not in epsilon_policy["allowed_data_types"]:
            ok = False
        if spec.get("verifiable") is not cross_policy["verifiable_required"]:
            ok = False
        if not non_empty_string(spec.get("declared_path")) or not non_empty_string(spec.get("components_path")):
            ok = False
        formula = spec.get("formula")
        if not non_empty_string(formula):
            ok = False
        else:
            lowered = str(formula).lower()
            if any(term not in lowered for term in cross_policy["required_formula_terms"]):
                ok = False
        if not non_empty_string(spec.get("epsilon_reason")):
            ok = False
        if not epsilon_allowed(str(data_type), spec.get("epsilon"), epsilon_policy):
            ok = False
    return ok, specs


def records_valid(
    report: dict[str, Any],
    specs: dict[str, dict[str, Any]],
    contract: dict[str, Any],
    mismatch_policy: dict[str, Any],
) -> tuple[bool, set[str]]:
    records = report.get("records")
    if not isinstance(records, list) or not records:
        return False, set()
    mismatch_ids: set[str] = set()
    ok = True
    covered_fields: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            ok = False
            continue
        for field in contract["record_required_fields"]:
            if field not in record:
                ok = False
        record_id = record.get("record_id")
        field = record.get("field")
        spec = specs.get(str(field))
        if not non_empty_string(record_id) or spec is None:
            ok = False
            continue
        covered_fields.add(str(field))
        for numeric_field in ["declared", "computed", "delta", "epsilon"]:
            if not is_number(record.get(numeric_field)):
                ok = False
        if record.get("data_type") != spec.get("data_type"):
            ok = False
        if record.get("epsilon") != spec.get("epsilon"):
            ok = False
        declared = record.get("declared")
        computed = record.get("computed")
        delta = record.get("delta")
        epsilon = record.get("epsilon")
        if all(is_number(value) for value in [declared, computed, delta, epsilon]):
            if abs((declared - computed) - delta) > TOLERANCE:
                ok = False
            expected_mismatch = abs(delta) > epsilon
            if record.get("mismatch") is not expected_mismatch:
                ok = False
            if expected_mismatch:
                mismatch_ids.add(str(record_id))
                if record.get("action") != mismatch_policy["mismatch_action"]:
                    ok = False
            elif record.get("action") != mismatch_policy["match_action"]:
                ok = False
        if record.get("action") not in mismatch_policy["allowed_actions"]:
            ok = False
        if record.get("overwritten") is not False:
            ok = False
    if set(specs) - covered_fields:
        ok = False
    return ok, mismatch_ids


def escalations_valid(report: dict[str, Any], mismatch_ids: set[str], policy: dict[str, Any]) -> bool:
    escalations = report.get("escalations")
    if not isinstance(escalations, list):
        return False
    seen: set[str] = set()
    ok = True
    for item in escalations:
        if not isinstance(item, dict):
            ok = False
            continue
        for field in policy["required_fields"]:
            if field not in item:
                ok = False
        record_id = item.get("record_id")
        if record_id in mismatch_ids:
            seen.add(str(record_id))
        if item.get("assignee_type") not in policy["allowed_assignee_types"]:
            ok = False
        if item.get("declared_visible") is not policy["declared_visible_required"]:
            ok = False
        if item.get("computed_visible") is not policy["computed_visible_required"]:
            ok = False
        if not non_empty_string(item.get("reason")):
            ok = False
    return ok and seen == mismatch_ids


def structural_tests_valid(report: dict[str, Any], policy: dict[str, Any]) -> bool:
    tests = report.get("structural_tests")
    if not isinstance(tests, dict):
        return False
    return all(tests.get(flag) is True for flag in policy["required_boolean_flags"])


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("self-correction-loops-contract.json")["json_contract"]
    cross_policy = asset("cross-check-policy.json")
    epsilon_policy = asset("epsilon-policy.json")
    mismatch_policy = asset("mismatch-policy.json")
    escalation_policy = asset("escalation-policy.json")
    structural_policy = asset("structural-test-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("check_id")):
        errors.append("check_id must be non-empty")

    fields_ok, specs = field_specs_valid(report, cross_policy, epsilon_policy)
    records_ok, mismatch_ids = records_valid(report, specs, contract, mismatch_policy)
    escalations_ok = escalations_valid(report, mismatch_ids, escalation_policy)
    structural_ok = structural_tests_valid(report, structural_policy)
    silent_blocked = records_ok and all(record.get("overwritten") is False for record in report.get("records", []) if isinstance(record, dict))

    checks = {
        "fields_verifiable": fields_ok,
        "epsilon_justified": fields_ok,
        "records_recomputed": records_ok,
        "mismatches_visible": records_ok and all(mismatch_ids),
        "mismatches_escalated": escalations_ok,
        "silent_correction_blocked": silent_blocked,
        "structural_tests_passed": structural_ok,
        "deterministic_script_passed": True,
    }
    if not mismatch_ids:
        checks["mismatches_visible"] = records_ok
        checks["mismatches_escalated"] = escalations_ok

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    for field, expected in checks.items():
        if not expected:
            errors.append(f"{field} is false")
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
    parser = argparse.ArgumentParser(description="Validate a self-correction-loops JSON report")
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--fixture-suite", type=Path)
    args = parser.parse_args()
    try:
        if args.fixture_suite:
            valid_count, invalid_count = run_fixture_suite(args.fixture_suite)
            print(f"self-correction-loops check passed: valid={valid_count} invalid={invalid_count}")
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
    raise SystemExit(main())
