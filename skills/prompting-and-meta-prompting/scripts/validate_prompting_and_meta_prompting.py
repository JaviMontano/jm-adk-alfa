#!/usr/bin/env python3
"""Validate deterministic prompting-and-meta-prompting reports."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "prompting-and-meta-prompting"
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


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


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


def prompt_complete(report: dict[str, Any], prompt_policy: dict[str, Any]) -> bool:
    request = report.get("request")
    prompt = report.get("prompt_artifact")
    if not isinstance(request, dict) or not isinstance(prompt, dict):
        return False
    for field in prompt_policy["required_request_fields"]:
        value = request.get(field)
        if field in {"constraints", "missing_data"}:
            if not isinstance(value, list):
                return False
        elif not non_empty_string(value):
            return False
    for field in prompt_policy["required_prompt_fields"]:
        if field not in prompt:
            return False
    if not non_empty_string(prompt.get("role")) or not non_empty_string(prompt.get("task")):
        return False
    if not isinstance(prompt.get("sequence"), list) or len(prompt["sequence"]) < prompt_policy["minimum_sequence_steps"]:
        return False
    if not non_empty_list(prompt.get("constraints")):
        return False
    if not isinstance(prompt.get("anti_drift"), list) or len(prompt["anti_drift"]) < prompt_policy["minimum_anti_drift_rules"]:
        return False
    output_contract = prompt.get("output_contract")
    if not isinstance(output_contract, dict):
        return False
    for field in prompt_policy["required_output_contract_fields"]:
        value = output_contract.get(field)
        if field in {"required_sections", "failure_states"}:
            if not non_empty_list(value):
                return False
        elif not non_empty_string(value):
            return False
    missing = prompt.get("missing_data_handling")
    return isinstance(missing, dict) and missing.get("mode") in prompt_policy["allowed_missing_data_modes"]


def meta_prompt_complete(report: dict[str, Any], meta_policy: dict[str, Any]) -> bool:
    meta_prompt = report.get("meta_prompt")
    if not isinstance(meta_prompt, dict):
        return False
    if meta_prompt.get("enabled") is not True:
        return False
    if meta_prompt.get("mode") not in meta_policy["allowed_modes"]:
        return False
    dimensions = set(meta_prompt.get("review_dimensions", [])) if isinstance(meta_prompt.get("review_dimensions"), list) else set()
    return set(meta_policy["required_review_dimensions"]).issubset(dimensions)


def acceptance_criteria_valid(report: dict[str, Any], criteria_policy: dict[str, Any]) -> bool:
    criteria = report.get("acceptance_criteria")
    if not isinstance(criteria, list) or len(criteria) < criteria_policy["minimum_criteria"]:
        return False
    pattern = re.compile(criteria_policy["id_pattern"])
    for item in criteria:
        if not isinstance(item, dict):
            return False
        if set(criteria_policy["required_fields"]) - set(item):
            return False
        if not pattern.match(str(item.get("id", ""))):
            return False
        if not non_empty_string(item.get("criterion")):
            return False
        if item.get("verifiable") is not True:
            return False
    return True


def eval_cases_valid(report: dict[str, Any], eval_policy: dict[str, Any]) -> bool:
    cases = report.get("eval_cases")
    if not isinstance(cases, list) or len(cases) < eval_policy["minimum_cases"]:
        return False
    seen_types = set()
    for case in cases:
        if not isinstance(case, dict):
            return False
        if not non_empty_string(case.get("id")) or not non_empty_string(case.get("input")):
            return False
        if not isinstance(case.get("expected_activation"), bool):
            return False
        if not set(eval_policy["required_checks"]).issubset(set(case.get("expected_checks", []))):
            return False
        case_type = case.get("case_type")
        if case_type in eval_policy["required_case_types"]:
            seen_types.add(case_type)
    return set(eval_policy["required_case_types"]).issubset(seen_types)


def safety_valid(report: dict[str, Any], safety_policy: dict[str, Any]) -> bool:
    safety = report.get("safety")
    if not isinstance(safety, dict):
        return False
    for flag in safety_policy["required_safety_flags"]:
        if safety.get(flag) is not True:
            return False
    evidence = set(safety.get("evidence_requirements", [])) if isinstance(safety.get("evidence_requirements"), list) else set()
    return set(safety_policy["required_evidence_requirements"]).issubset(evidence)


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("prompting-and-meta-prompting-contract.json")["json_contract"]
    prompt_policy = asset("prompt-component-policy.json")
    meta_policy = asset("meta-prompt-policy.json")
    criteria_policy = asset("acceptance-criteria-policy.json")
    eval_policy = asset("eval-case-policy.json")
    safety_policy = asset("safety-anti-drift-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("artifact_id")):
        errors.append("artifact_id must be non-empty")

    checks = {
        "prompt_contract_complete": prompt_complete(report, prompt_policy),
        "meta_prompt_complete": meta_prompt_complete(report, meta_policy),
        "acceptance_criteria_verifiable": acceptance_criteria_valid(report, criteria_policy),
        "evals_cover_edges": eval_cases_valid(report, eval_policy),
        "safety_boundaries_present": safety_valid(report, safety_policy),
        "deterministic_script_passed": True,
    }

    if not checks["prompt_contract_complete"]:
        errors.append("prompt contract is incomplete")
    if not checks["meta_prompt_complete"]:
        errors.append("meta_prompt is incomplete")
    if not checks["acceptance_criteria_verifiable"]:
        errors.append("acceptance criteria must be verifiable")
    if not checks["evals_cover_edges"]:
        errors.append("eval cases must cover required edge cases")
    if not checks["safety_boundaries_present"]:
        errors.append("safety boundaries are incomplete")

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
        errors = validate(report)
        if not errors:
            raise AssertionError(f"{case['id']} should fail")
        invalid_count += 1
    return valid_count, invalid_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a prompting-and-meta-prompting JSON report")
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--fixture-suite", type=Path)
    args = parser.parse_args()

    try:
        if args.fixture_suite:
            valid_count, invalid_count = run_fixture_suite(args.fixture_suite)
            print(f"prompting-and-meta-prompting check passed: valid={valid_count} invalid={invalid_count}")
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
