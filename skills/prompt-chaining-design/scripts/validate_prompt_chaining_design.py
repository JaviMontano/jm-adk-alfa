#!/usr/bin/env python3
"""Validate deterministic prompt chaining design reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SKILL = "prompt-chaining-design"
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


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("prompt-chaining-design-contract.json")["json_contract"]
    gate_policy = asset("single-pass-gate-policy.json")
    local_policy = asset("local-pass-schema-policy.json")
    transition_policy = asset("transition-schema-policy.json")
    integration_policy = asset("integration-pass-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("chain_id")):
        errors.append("chain_id must be non-empty")

    assessment = report.get("single_pass_assessment")
    if not isinstance(assessment, dict):
        errors.append("single_pass_assessment must be an object")
        assessment = {}
    use_chain = assessment.get("use_chain")
    if not isinstance(use_chain, bool):
        errors.append("single_pass_assessment.use_chain must be boolean")
    reasons = assessment.get("justification_reasons")
    if not isinstance(reasons, list):
        errors.append("single_pass_assessment.justification_reasons must be a list")
        reasons = []
    unknown_reasons = sorted(set(reasons) - set(gate_policy["justification_reasons"]))
    if unknown_reasons:
        errors.append(f"unknown chain justification reasons: {unknown_reasons}")
    chain_justified = use_chain is True and len(set(reasons)) >= gate_policy["minimum_reasons_for_chain"]

    unit = report.get("unit_contract")
    if not isinstance(unit, dict):
        errors.append("unit_contract must be an object")
        unit = {}
    if not non_empty_string(unit.get("atomic_unit")):
        errors.append("unit_contract.atomic_unit must be non-empty")
    for field in ["one_unit_per_local_pass", "idempotent", "parallelizable"]:
        if unit.get(field) is not True:
            errors.append(f"unit_contract.{field} must be true")

    local_schema = report.get("local_pass_schema")
    if not isinstance(local_schema, dict):
        errors.append("local_pass_schema must be an object")
        local_schema = {}
    fields = set(local_schema.get("fields", [])) if isinstance(local_schema.get("fields"), list) else set()
    if not set(local_policy["required_summary_fields"]).issubset(fields):
        errors.append("local_pass_schema.fields missing required summary fields")
    statuses = set(local_schema.get("status_values", [])) if isinstance(local_schema.get("status_values"), list) else set()
    if set(local_policy["allowed_statuses"]) != statuses:
        errors.append("local_pass_schema.status_values must be ok and error")
    if local_schema.get("throws_global_exception") is not False:
        errors.append("local_pass_schema.throws_global_exception must be false")

    transition = report.get("transition_schema")
    if not isinstance(transition, dict):
        errors.append("transition_schema must be an object")
        transition = {}
    transition_fields = set(transition.get("fields", [])) if isinstance(transition.get("fields"), list) else set()
    if not set(transition_policy["required_fields"]).issubset(transition_fields):
        errors.append("transition_schema.fields missing required fields")
    forbidden_payloads = set(transition.get("forbidden_payloads", [])) if isinstance(transition.get("forbidden_payloads"), list) else set()
    if not set(transition_policy["forbidden_payloads"]).issubset(forbidden_payloads):
        errors.append("transition_schema.forbidden_payloads missing raw payload bans")

    integration = report.get("integration_pass")
    if not isinstance(integration, dict):
        errors.append("integration_pass must be an object")
        integration = {}
    for field in integration_policy["required_flags"]:
        if integration.get(field) is not True:
            errors.append(f"integration_pass.{field} must be true")

    error_handling = report.get("error_handling")
    if not isinstance(error_handling, dict):
        errors.append("error_handling must be an object")
        error_handling = {}
    if error_handling.get("typed_per_unit") is not True:
        errors.append("error_handling.typed_per_unit must be true")
    if error_handling.get("propagates_as_data") is not True:
        errors.append("error_handling.propagates_as_data must be true")
    if error_handling.get("aborts_batch") is not False:
        errors.append("error_handling.aborts_batch must be false")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    expected = {
        "chain_justified": chain_justified,
        "local_pass_one_unit": unit.get("one_unit_per_local_pass") is True,
        "local_schema_typed": set(local_policy["required_summary_fields"]).issubset(fields),
        "transition_schema_present": set(transition_policy["required_fields"]).issubset(transition_fields),
        "integration_uses_summaries_only": integration.get("consumes_summaries_only") is True and integration.get("raw_units_forbidden") is True,
        "typed_error_state": error_handling.get("typed_per_unit") is True and error_handling.get("propagates_as_data") is True,
        "deterministic_script_passed": True,
    }
    for field, value in expected.items():
        if validation.get(field) is not value:
            errors.append(f"validation.{field} must be {value}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
        guardian = {}
    decision = guardian.get("decision")
    if decision not in contract["guardian_decisions"]:
        errors.append("guardian.decision is not allowed")
    if not non_empty_string(guardian.get("reason")):
        errors.append("guardian.reason must be non-empty")
    blocking_needed = any(value is False for value in expected.values())
    if decision == "pass" and blocking_needed:
        errors.append("guardian pass requires all validation flags true")
    if decision == "block" and not blocking_needed:
        errors.append("guardian block requires validation failure")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a prompt chaining design JSON report")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
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
