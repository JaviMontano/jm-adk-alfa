#!/usr/bin/env python3
"""Validate deterministic provenance-engineering reports."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "provenance-engineering"
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


def source_inventory(report: dict[str, Any], source_policy: dict[str, Any]) -> tuple[set[str], bool]:
    sources = report.get("sources")
    if not isinstance(sources, list) or not sources:
        return set(), False
    ids: set[str] = set()
    date_re = re.compile(source_policy["date_pattern"])
    ok = True
    for source in sources:
        if not isinstance(source, dict):
            ok = False
            continue
        for field in source_policy["required_source_fields"]:
            if not non_empty_string(source.get(field)):
                ok = False
        if source.get("source_type") not in source_policy["allowed_source_types"]:
            ok = False
        if not date_re.match(str(source.get("as_of", ""))):
            ok = False
        source_id = source.get("source_id")
        if non_empty_string(source_id):
            ids.add(source_id)
    return ids, ok


def claims_valid(report: dict[str, Any], source_ids: set[str], source_policy: dict[str, Any]) -> tuple[bool, bool, set[str]]:
    claims = report.get("claims")
    if not isinstance(claims, list) or not claims:
        return False, False, set()
    date_re = re.compile(source_policy["date_pattern"])
    all_have_sources = True
    all_sources_exist = True
    conflict_claim_ids: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            return False, False, set()
        for field in source_policy["required_claim_fields"]:
            if field not in claim:
                all_have_sources = False
        if not non_empty_string(claim.get("claim_id")) or not non_empty_string(claim.get("attribute")):
            all_have_sources = False
        if not non_empty_string(claim.get("as_of")) or not date_re.match(str(claim.get("as_of", ""))):
            all_have_sources = False
        claim_sources = claim.get("source_ids")
        if not isinstance(claim_sources, list) or not claim_sources:
            all_have_sources = False
            all_sources_exist = False
        else:
            for source_id in claim_sources:
                if source_id not in source_ids:
                    all_sources_exist = False
        if not isinstance(claim.get("conflict"), bool):
            all_have_sources = False
        if claim.get("conflict") is True and non_empty_string(claim.get("claim_id")):
            conflict_claim_ids.add(str(claim["claim_id"]))
    return all_have_sources, all_sources_exist, conflict_claim_ids


def conflicts_valid(
    report: dict[str, Any],
    source_ids: set[str],
    conflict_claim_ids: set[str],
    conflict_policy: dict[str, Any],
) -> tuple[bool, set[str]]:
    conflicts = report.get("conflicts")
    if not isinstance(conflicts, list):
        return False, set()
    if conflict_claim_ids and not conflicts:
        return False, set()
    conflict_ids: set[str] = set()
    represented_claims: set[str] = set()
    ok = True
    for conflict in conflicts:
        if not isinstance(conflict, dict):
            return False, set()
        for field in conflict_policy["required_conflict_fields"]:
            if field not in conflict:
                ok = False
        conflict_id = conflict.get("conflict_id")
        if non_empty_string(conflict_id):
            conflict_ids.add(str(conflict_id))
        claim_ids = conflict.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids:
            ok = False
        else:
            represented_claims.update(str(claim_id) for claim_id in claim_ids)
        conflict_sources = conflict.get("source_ids")
        if not isinstance(conflict_sources, list) or len(conflict_sources) < conflict_policy["minimum_sources_per_conflict"]:
            ok = False
        elif any(source_id not in source_ids for source_id in conflict_sources):
            ok = False
        values = conflict.get("values")
        if not isinstance(values, list) or len(values) < conflict_policy["minimum_values_per_conflict"]:
            ok = False
        policy = conflict.get("resolution_policy")
        if policy != conflict_policy["required_resolution_policy"]:
            ok = False
        if policy in conflict_policy["forbidden_resolution_policies"]:
            ok = False
        if conflict.get("status") not in conflict_policy["allowed_statuses"]:
            ok = False
    if not conflict_claim_ids.issubset(represented_claims):
        ok = False
    return ok, conflict_ids


def escalations_valid(report: dict[str, Any], conflict_ids: set[str], escalation_policy: dict[str, Any]) -> bool:
    escalations = report.get("escalations")
    if not isinstance(escalations, list):
        return False
    if conflict_ids and not escalations:
        return False
    escalated_conflicts: set[str] = set()
    ok = True
    for escalation in escalations:
        if not isinstance(escalation, dict):
            return False
        for field in escalation_policy["required_escalation_fields"]:
            if field not in escalation:
                ok = False
        conflict_id = escalation.get("conflict_id")
        if conflict_id in conflict_ids:
            escalated_conflicts.add(str(conflict_id))
        if escalation.get("assignee_type") != escalation_policy["required_assignee_type"]:
            ok = False
        if escalation.get("status") not in escalation_policy["allowed_statuses"]:
            ok = False
        if escalation.get("as_of_visible") is not True:
            ok = False
        if not isinstance(escalation.get("source_ids"), list) or not escalation["source_ids"]:
            ok = False
        if not non_empty_string(escalation.get("reason")):
            ok = False
    return ok and conflict_ids.issubset(escalated_conflicts)


def render_valid(report: dict[str, Any], render_policy: dict[str, Any]) -> bool:
    render = report.get("render")
    if not isinstance(render, dict):
        return False
    return all(render.get(flag) is True for flag in render_policy["required_flags"])


def structural_tests_valid(report: dict[str, Any], structural_policy: dict[str, Any]) -> bool:
    tests = report.get("structural_tests")
    if not isinstance(tests, dict):
        return False
    return all(tests.get(flag) is True for flag in structural_policy["required_flags"])


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("provenance-engineering-contract.json")["json_contract"]
    source_policy = asset("claim-source-policy.json")
    conflict_policy = asset("conflict-policy.json")
    escalation_policy = asset("escalation-policy.json")
    render_policy = asset("render-policy.json")
    structural_policy = asset("structural-test-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("report_id")):
        errors.append("report_id must be non-empty")

    source_ids, sources_ok = source_inventory(report, source_policy)
    all_claims_have_sources, all_claim_sources_exist, conflict_claim_ids = claims_valid(report, source_ids, source_policy)
    conflicts_preserved, conflict_ids = conflicts_valid(report, source_ids, conflict_claim_ids, conflict_policy)
    conflicts_escalated = escalations_valid(report, conflict_ids, escalation_policy)
    render_ok = render_valid(report, render_policy)
    structural_ok = structural_tests_valid(report, structural_policy)

    checks = {
        "sources_valid": sources_ok,
        "all_claims_have_sources": all_claims_have_sources,
        "all_claim_sources_exist": all_claim_sources_exist,
        "conflicts_preserved": conflicts_preserved,
        "conflicts_escalated": conflicts_escalated,
        "render_dates_and_sources": render_ok,
        "structural_tests_passed": structural_ok,
        "deterministic_script_passed": True,
    }

    if not sources_ok:
        errors.append("sources are incomplete")
    if not all_claims_have_sources:
        errors.append("all claims must have non-empty source_ids and as_of")
    if not all_claim_sources_exist:
        errors.append("all claim source_ids must exist in sources")
    if not conflicts_preserved:
        errors.append("conflicts must preserve claims, values, sources, and escalation policy")
    if not conflicts_escalated:
        errors.append("conflicts must be escalated to human review")
    if not render_ok:
        errors.append("render must show source ids, as_of, and conflict markers")
    if not structural_ok:
        errors.append("structural tests are incomplete")

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
    parser = argparse.ArgumentParser(description="Validate a provenance-engineering JSON report")
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--fixture-suite", type=Path)
    args = parser.parse_args()

    try:
        if args.fixture_suite:
            valid_count, invalid_count = run_fixture_suite(args.fixture_suite)
            print(f"provenance-engineering check passed: valid={valid_count} invalid={invalid_count}")
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
