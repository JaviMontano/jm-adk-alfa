#!/usr/bin/env python3
"""Validate deterministic AI testing strategy reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_fields(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def validate_refs(errors: list[str], refs: Any, known: set[str], path: str) -> None:
    if not isinstance(refs, list) or not refs:
        errors.append(f"{path}: must be a non-empty list")
        return
    for ref in refs:
        if ref not in known:
            errors.append(f"{path}: unknown evidence id {ref}")


def validate_evidence(report: dict[str, Any], errors: list[str], policy: dict[str, Any]) -> set[str]:
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence: must be a non-empty list")
        return set()
    seen: set[str] = set()
    allowed_tags = set(policy["allowed_tags"])
    for index, item in enumerate(evidence):
        path = f"evidence[{index}]"
        require_fields(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if not is_non_empty_string(evidence_id):
            errors.append(f"{path}.id: must be non-empty")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate {evidence_id}")
        else:
            seen.add(str(evidence_id))
        if item.get("tag") not in allowed_tags:
            errors.append(f"{path}.tag: invalid")
        for field in ("source", "summary"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
    return seen


def validate_system(report: dict[str, Any], errors: list[str]) -> None:
    system = report.get("system")
    require_fields(errors, system, "system", ["name", "use_case", "risk_level", "strategy_scope"])
    if not isinstance(system, dict):
        return
    for field in ("name", "use_case", "strategy_scope"):
        if not is_non_empty_string(system.get(field)):
            errors.append(f"system.{field}: must be non-empty")
    if system.get("risk_level") not in {"low", "medium", "high"}:
        errors.append("system.risk_level: must be low, medium, or high")


def validate_matrix(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_evidence: set[str]) -> None:
    matrix = report.get("matrix_coverage")
    require_fields(errors, matrix, "matrix_coverage", ["covered_test_types", "covered_layers", "cells"])
    if not isinstance(matrix, dict):
        return
    missing_types = set(policy["test_types"]) - set(matrix.get("covered_test_types", []))
    missing_layers = set(policy["layers"]) - set(matrix.get("covered_layers", []))
    if missing_types:
        errors.append(f"matrix_coverage.covered_test_types: missing {sorted(missing_types)}")
    if missing_layers:
        errors.append(f"matrix_coverage.covered_layers: missing {sorted(missing_layers)}")
    cells = matrix.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append("matrix_coverage.cells: must be a non-empty list")
        return
    for index, item in enumerate(cells):
        path = f"matrix_coverage.cells[{index}]"
        require_fields(errors, item, path, ["test_type", "layer", "priority", "coverage_target", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if item.get("test_type") not in set(policy["test_types"]):
            errors.append(f"{path}.test_type: invalid")
        if item.get("layer") not in set(policy["layers"]):
            errors.append(f"{path}.layer: invalid")
        if item.get("priority") not in set(policy["priorities"]):
            errors.append(f"{path}.priority: invalid")
        if not is_non_empty_string(item.get("coverage_target")):
            errors.append(f"{path}.coverage_target: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_test_set(report: dict[str, Any], errors: list[str], section: str, policy: dict[str, Any], known_evidence: set[str], automation_policy: dict[str, Any]) -> None:
    tests = report.get(section)
    if not isinstance(tests, list) or not tests:
        errors.append(f"{section}: must be a non-empty list")
        return
    seen: set[str] = set()
    required_fields = policy["required_fields"]
    for index, item in enumerate(tests):
        path = f"{section}[{index}]"
        require_fields(errors, item, path, required_fields)
        if not isinstance(item, dict):
            continue
        category = item.get("category")
        if category not in set(policy["required_categories"]):
            errors.append(f"{path}.category: invalid")
        else:
            seen.add(str(category))
        if item.get("automation_tier") not in set(automation_policy["tiers"]):
            errors.append(f"{path}.automation_tier: invalid")
        for field in ("oracle", "threshold"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = set(policy["required_categories"]) - seen
    if missing:
        errors.append(f"{section}: missing required categories {sorted(missing)}")


def validate_integration(report: dict[str, Any], errors: list[str], known_evidence: set[str]) -> None:
    integration = report.get("integration_strategy")
    require_fields(errors, integration, "integration_strategy", ["approach", "rationale", "harness", "contracts", "evidence_ids"])
    if not isinstance(integration, dict):
        return
    if integration.get("approach") not in {"top_down", "bottom_up", "parallel", "big_bang", "bottom_up_harness", "digital_twin"}:
        errors.append("integration_strategy.approach: invalid")
    for field in ("rationale", "harness"):
        if not is_non_empty_string(integration.get(field)):
            errors.append(f"integration_strategy.{field}: must be non-empty")
    contracts = integration.get("contracts")
    if not isinstance(contracts, list) or not contracts:
        errors.append("integration_strategy.contracts: must be a non-empty list")
    validate_refs(errors, integration.get("evidence_ids"), known_evidence, "integration_strategy.evidence_ids")


def validate_automation(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_evidence: set[str]) -> None:
    gates = report.get("automation_gates")
    if not isinstance(gates, list) or not gates:
        errors.append("automation_gates: must be a non-empty list")
        return
    seen: set[str] = set()
    for index, item in enumerate(gates):
        path = f"automation_gates[{index}]"
        require_fields(errors, item, path, ["gate", "tier", "trigger", "blocks", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        gate = item.get("gate")
        if gate not in set(policy["required_gates"]):
            errors.append(f"{path}.gate: invalid")
        else:
            seen.add(str(gate))
        if item.get("tier") not in set(policy["tiers"]):
            errors.append(f"{path}.tier: invalid")
        if item.get("blocks") not in set(policy["allowed_blocking"]):
            errors.append(f"{path}.blocks: invalid")
        if not is_non_empty_string(item.get("trigger")):
            errors.append(f"{path}.trigger: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = set(policy["required_gates"]) - seen
    if missing:
        errors.append(f"automation_gates: missing required gates {sorted(missing)}")


def validate_monitoring(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_evidence: set[str]) -> None:
    monitoring = report.get("monitoring")
    if not isinstance(monitoring, list) or not monitoring:
        errors.append("monitoring: must be a non-empty list")
        return
    seen: set[str] = set()
    for index, item in enumerate(monitoring):
        path = f"monitoring[{index}]"
        require_fields(errors, item, path, ["signal", "threshold", "response", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        signal = item.get("signal")
        if signal not in set(policy["required_monitoring"]):
            errors.append(f"{path}.signal: invalid")
        else:
            seen.add(str(signal))
        for field in ("threshold", "response"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = set(policy["required_monitoring"]) - seen
    if missing:
        errors.append(f"monitoring: missing required signals {sorted(missing)}")


def validate_validation(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    validation = report.get("validation")
    require_fields(errors, validation, "validation", ["status", "checks"])
    if not isinstance(validation, dict):
        return
    if validation.get("status") not in set(contract["allowed_validation_statuses"]):
        errors.append("validation.status: invalid")
    checks = validation.get("checks")
    if not isinstance(checks, list):
        errors.append("validation.checks: must be a list")
        return
    missing = set(contract["required_validation_checks"]) - set(checks)
    if missing:
        errors.append(f"validation.checks: missing required checks {sorted(missing)}")


def validate_report(report: dict[str, Any]) -> list[str]:
    contract = load_json(ASSET_DIR / "testing-strategy-contract.json")
    matrix_policy = load_json(ASSET_DIR / "matrix-policy.json")
    model_policy = load_json(ASSET_DIR / "model-test-policy.json")
    data_policy = load_json(ASSET_DIR / "data-quality-policy.json")
    fairness_policy = load_json(ASSET_DIR / "fairness-compliance-policy.json")
    automation_policy = load_json(ASSET_DIR / "automation-policy.json")
    evidence_policy = load_json(ASSET_DIR / "evidence-policy.json")

    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing required section {section}")
    if errors:
        return errors

    validate_system(report, errors)
    known_evidence = validate_evidence(report, errors, evidence_policy)
    validate_matrix(report, errors, matrix_policy, known_evidence)
    validate_test_set(report, errors, "model_tests", model_policy, known_evidence, automation_policy)
    validate_test_set(report, errors, "data_quality_tests", data_policy, known_evidence, automation_policy)
    validate_test_set(report, errors, "fairness_compliance_tests", fairness_policy, known_evidence, automation_policy)
    validate_integration(report, errors, known_evidence)
    validate_automation(report, errors, automation_policy, known_evidence)
    validate_monitoring(report, errors, automation_policy, known_evidence)
    validate_validation(report, errors, contract)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI testing strategy report JSON fixture")
    parser.add_argument("report", help="Path to report JSON")
    args = parser.parse_args()

    report_path = Path(args.report)
    try:
        report = load_json(report_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {report_path}: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(report, dict):
        print(f"ERROR {report_path}: root must be an object", file=sys.stderr)
        return 1
    errors = validate_report(report)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(f"report={report_path.name} status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
