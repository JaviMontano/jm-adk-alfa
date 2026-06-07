#!/usr/bin/env python3
"""Validate deterministic AI software architecture reports."""

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
    allowed_tags = set(policy["allowed_tags"])
    seen: set[str] = set()
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
    require_fields(errors, system, "system", ["name", "use_case", "risk_level", "architecture_scope"])
    if not isinstance(system, dict):
        return
    for field in ("name", "use_case", "architecture_scope"):
        if not is_non_empty_string(system.get(field)):
            errors.append(f"system.{field}: must be non-empty")
    if system.get("risk_level") not in {"low", "medium", "high"}:
        errors.append("system.risk_level: must be low, medium, or high")


def validate_layers(report: dict[str, Any], errors: list[str], layer_policy: dict[str, Any], known_evidence: set[str]) -> None:
    layers = report.get("layer_view")
    if not isinstance(layers, list) or not layers:
        errors.append("layer_view: must be a non-empty list")
        return
    required_layers = set(layer_policy["required_layers"])
    seen: set[str] = set()
    for index, item in enumerate(layers):
        path = f"layer_view[{index}]"
        require_fields(errors, item, path, ["layer", "modules", "responsibility", "dependencies", "owner", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        layer = item.get("layer")
        if layer not in required_layers:
            errors.append(f"{path}.layer: invalid")
        else:
            seen.add(str(layer))
        if not isinstance(item.get("modules"), list) or not item["modules"]:
            errors.append(f"{path}.modules: must be a non-empty list")
        if not isinstance(item.get("dependencies"), list):
            errors.append(f"{path}.dependencies: must be a list")
        for field in ("responsibility", "owner"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = required_layers - seen
    if missing:
        errors.append(f"layer_view: missing required layers {sorted(missing)}")


def validate_components(report: dict[str, Any], errors: list[str], layer_policy: dict[str, Any], known_evidence: set[str]) -> None:
    components = report.get("components")
    if not isinstance(components, list) or not components:
        errors.append("components: must be a non-empty list")
        return
    required_layers = set(layer_policy["required_layers"])
    for index, item in enumerate(components):
        path = f"components[{index}]"
        require_fields(errors, item, path, ["id", "layer", "responsibility", "interfaces", "dependencies", "owner", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if not is_non_empty_string(item.get("id")):
            errors.append(f"{path}.id: must be non-empty")
        if item.get("layer") not in required_layers:
            errors.append(f"{path}.layer: invalid")
        if not isinstance(item.get("interfaces"), list) or not item["interfaces"]:
            errors.append(f"{path}.interfaces: must be a non-empty list")
        if not isinstance(item.get("dependencies"), list):
            errors.append(f"{path}.dependencies: must be a list")
        for field in ("responsibility", "owner"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_patterns(report: dict[str, Any], errors: list[str], pattern_policy: dict[str, Any], quality_policy: dict[str, Any], known_evidence: set[str]) -> None:
    patterns = report.get("patterns")
    if not isinstance(patterns, list) or not patterns:
        errors.append("patterns: must be a non-empty list")
        return
    allowed_patterns = set(pattern_policy["allowed_patterns"])
    allowed_decisions = set(pattern_policy["allowed_decisions"])
    allowed_attributes = set(quality_policy["allowed_attributes"])
    selected = 0
    for index, item in enumerate(patterns):
        path = f"patterns[{index}]"
        require_fields(errors, item, path, ["id", "name", "decision", "rationale", "enabled_quality_attributes", "alternatives", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if item.get("name") not in allowed_patterns:
            errors.append(f"{path}.name: invalid")
        if item.get("decision") not in allowed_decisions:
            errors.append(f"{path}.decision: invalid")
        if item.get("decision") == "selected":
            selected += 1
        if not is_non_empty_string(item.get("rationale")):
            errors.append(f"{path}.rationale: must be non-empty")
        attrs = item.get("enabled_quality_attributes")
        if not isinstance(attrs, list) or not attrs:
            errors.append(f"{path}.enabled_quality_attributes: must be a non-empty list")
        else:
            for attr in attrs:
                if attr not in allowed_attributes:
                    errors.append(f"{path}.enabled_quality_attributes: invalid {attr}")
        if not isinstance(item.get("alternatives"), list) or not item["alternatives"]:
            errors.append(f"{path}.alternatives: must be a non-empty list")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    if selected == 0:
        errors.append("patterns: at least one pattern must be selected")


def validate_quality_scenarios(report: dict[str, Any], errors: list[str], quality_policy: dict[str, Any], known_evidence: set[str]) -> None:
    scenarios = report.get("quality_scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("quality_scenarios: must be a non-empty list")
        return
    allowed_attributes = set(quality_policy["allowed_attributes"])
    seen: set[str] = set()
    for index, item in enumerate(scenarios):
        path = f"quality_scenarios[{index}]"
        require_fields(errors, item, path, ["id", *quality_policy["scenario_fields"]])
        if not isinstance(item, dict):
            continue
        attr = item.get("attribute")
        if attr not in allowed_attributes:
            errors.append(f"{path}.attribute: invalid")
        else:
            seen.add(str(attr))
        for field in ("id", "stimulus", "response", "measure"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = set(quality_policy["required_attributes"]) - seen
    if missing:
        errors.append(f"quality_scenarios: missing required attributes {sorted(missing)}")


def validate_adrs(report: dict[str, Any], errors: list[str], adr_policy: dict[str, Any], known_evidence: set[str]) -> None:
    adrs = report.get("adrs")
    if not isinstance(adrs, list) or not adrs:
        errors.append("adrs: must be a non-empty list")
        return
    allowed_statuses = set(adr_policy["allowed_statuses"])
    for index, item in enumerate(adrs):
        path = f"adrs[{index}]"
        require_fields(errors, item, path, adr_policy["required_fields"])
        if not isinstance(item, dict):
            continue
        if item.get("status") not in allowed_statuses:
            errors.append(f"{path}.status: invalid")
        for field in ("id", "title", "context", "decision", "consequences"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        if not isinstance(item.get("alternatives"), list) or not item["alternatives"]:
            errors.append(f"{path}.alternatives: must be a non-empty list")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_debt(report: dict[str, Any], errors: list[str], known_evidence: set[str]) -> set[str]:
    debt = report.get("debt")
    if not isinstance(debt, list) or not debt:
        errors.append("debt: must be a non-empty list")
        return set()
    seen: set[str] = set()
    for index, item in enumerate(debt):
        path = f"debt[{index}]"
        require_fields(errors, item, path, ["id", "type", "severity", "owner", "mitigation", "sequence", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        debt_id = item.get("id")
        if not is_non_empty_string(debt_id):
            errors.append(f"{path}.id: must be non-empty")
        else:
            seen.add(str(debt_id))
        if item.get("severity") not in {"low", "medium", "high"}:
            errors.append(f"{path}.severity: must be low, medium, or high")
        if not isinstance(item.get("sequence"), int) or item["sequence"] < 1:
            errors.append(f"{path}.sequence: must be a positive integer")
        for field in ("type", "owner", "mitigation"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return seen


def validate_evolution(report: dict[str, Any], errors: list[str], known_debt: set[str]) -> None:
    plan = report.get("evolution_plan")
    if not isinstance(plan, list) or not plan:
        errors.append("evolution_plan: must be a non-empty list")
        return
    covered: set[str] = set()
    for index, item in enumerate(plan):
        path = f"evolution_plan[{index}]"
        require_fields(errors, item, path, ["step", "objective", "debt_ids", "validation"])
        if not isinstance(item, dict):
            continue
        if not isinstance(item.get("step"), int) or item["step"] < 1:
            errors.append(f"{path}.step: must be a positive integer")
        for field in ("objective", "validation"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        debt_ids = item.get("debt_ids")
        if not isinstance(debt_ids, list) or not debt_ids:
            errors.append(f"{path}.debt_ids: must be a non-empty list")
        else:
            for debt_id in debt_ids:
                if debt_id not in known_debt:
                    errors.append(f"{path}.debt_ids: unknown debt {debt_id}")
                else:
                    covered.add(str(debt_id))
    missing = known_debt - covered
    if missing:
        errors.append(f"evolution_plan: uncovered debt {sorted(missing)}")


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
    contract = load_json(ASSET_DIR / "architecture-report-contract.json")
    layer_policy = load_json(ASSET_DIR / "layer-model.json")
    quality_policy = load_json(ASSET_DIR / "quality-attribute-policy.json")
    pattern_policy = load_json(ASSET_DIR / "pattern-policy.json")
    adr_policy = load_json(ASSET_DIR / "adr-policy.json")
    evidence_policy = load_json(ASSET_DIR / "evidence-policy.json")

    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing required section {section}")
    if errors:
        return errors

    validate_system(report, errors)
    known_evidence = validate_evidence(report, errors, evidence_policy)
    validate_layers(report, errors, layer_policy, known_evidence)
    validate_components(report, errors, layer_policy, known_evidence)
    validate_patterns(report, errors, pattern_policy, quality_policy, known_evidence)
    validate_quality_scenarios(report, errors, quality_policy, known_evidence)
    validate_adrs(report, errors, adr_policy, known_evidence)
    known_debt = validate_debt(report, errors, known_evidence)
    validate_evolution(report, errors, known_debt)
    validate_validation(report, errors, contract)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI software architecture report JSON fixture")
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
