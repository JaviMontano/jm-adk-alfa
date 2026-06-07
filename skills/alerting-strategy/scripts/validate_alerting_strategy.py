#!/usr/bin/env python3
"""Validate deterministic alerting strategy reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def refs(errors: list[str], values: Any, known: set[str], path: str) -> None:
    if not isinstance(values, list) or not values:
        errors.append(f"{path}: must be a non-empty list")
        return
    for value in values:
        if value not in known:
            errors.append(f"{path}: unknown evidence id {value}")


def evidence(report: dict[str, Any], errors: list[str], policy: dict[str, Any]) -> set[str]:
    items = report.get("evidence")
    if not isinstance(items, list) or not items:
        errors.append("evidence: must be a non-empty list")
        return set()
    seen: set[str] = set()
    for index, item in enumerate(items):
        path = f"evidence[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        if item.get("tag") not in set(policy["allowed_tags"]):
            errors.append(f"{path}.tag: invalid")
        evidence_id = item.get("id")
        if not is_text(evidence_id):
            errors.append(f"{path}.id: must be non-empty")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate {evidence_id}")
        else:
            seen.add(str(evidence_id))
        for field in ("source", "summary"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
    return seen


def validate_system(report: dict[str, Any], errors: list[str]) -> None:
    system = report.get("system")
    require(errors, system, "system", ["name", "scope", "risk_level"])
    if isinstance(system, dict):
        if system.get("risk_level") not in {"low", "medium", "high"}:
            errors.append("system.risk_level: must be low, medium, or high")


def validate_severity(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> None:
    items = report.get("severity_model")
    if not isinstance(items, list) or not items:
        errors.append("severity_model: must be a non-empty list")
        return
    seen: set[str] = set()
    for index, item in enumerate(items):
        path = f"severity_model[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        sev = item.get("severity")
        if sev not in set(policy["allowed_severities"]):
            errors.append(f"{path}.severity: invalid")
        else:
            seen.add(str(sev))
        if not isinstance(item.get("page"), bool):
            errors.append(f"{path}.page: must be boolean")
        if sev in set(policy["paging_severities"]) and item.get("page") is not True:
            errors.append(f"{path}.page: paging severity must page")
        for field in ("target_response", "description"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")
    missing = {"critical", "high", "medium", "low"} - seen
    if missing:
        errors.append(f"severity_model: missing required severities {sorted(missing)}")


def validate_escalations(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> set[str]:
    items = report.get("escalation_paths")
    if not isinstance(items, list) or not items:
        errors.append("escalation_paths: must be a non-empty list")
        return set()
    ids: set[str] = set()
    for index, item in enumerate(items):
        path = f"escalation_paths[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        escalation_id = item.get("id")
        if is_text(escalation_id):
            ids.add(str(escalation_id))
        for field in ("owner_team", "primary_route", "backup_route", "handoff_condition"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")
    return ids


def validate_rules(report: dict[str, Any], errors: list[str], policy: dict[str, Any], severities: set[str], escalations: set[str], known: set[str]) -> None:
    items = report.get("alert_rules")
    if not isinstance(items, list) or not items:
        errors.append("alert_rules: must be a non-empty list")
        return
    for index, item in enumerate(items):
        path = f"alert_rules[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        if item.get("severity") not in severities:
            errors.append(f"{path}.severity: unknown")
        if item.get("escalation_id") not in escalations:
            errors.append(f"{path}.escalation_id: unknown")
        for field in ("id", "signal", "threshold", "owner", "oracle"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")


def validate_fatigue(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> None:
    items = report.get("fatigue_controls")
    if not isinstance(items, list) or not items:
        errors.append("fatigue_controls: must be a non-empty list")
        return
    seen: set[str] = set()
    for index, item in enumerate(items):
        path = f"fatigue_controls[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        control = item.get("control")
        if control not in set(policy["required_controls"]):
            errors.append(f"{path}.control: invalid")
        else:
            seen.add(str(control))
        for field in ("policy", "owner"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")
    missing = set(policy["required_controls"]) - seen
    if missing:
        errors.append(f"fatigue_controls: missing required controls {sorted(missing)}")


def validate_routing(report: dict[str, Any], errors: list[str], known: set[str]) -> None:
    routing = report.get("routing_policy")
    require(errors, routing, "routing_policy", ["default_route", "business_hours_route", "after_hours_route", "evidence_ids"])
    if isinstance(routing, dict):
        for field in ("default_route", "business_hours_route", "after_hours_route"):
            if not is_text(routing.get(field)):
                errors.append(f"routing_policy.{field}: must be non-empty")
        refs(errors, routing.get("evidence_ids"), known, "routing_policy.evidence_ids")


def validate_validation(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    validation = report.get("validation")
    require(errors, validation, "validation", ["status", "checks"])
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
    contract = load_json(ASSET_DIR / "alerting-strategy-contract.json")
    severity_policy = load_json(ASSET_DIR / "severity-policy.json")
    rule_policy = load_json(ASSET_DIR / "rule-policy.json")
    escalation_policy = load_json(ASSET_DIR / "escalation-policy.json")
    fatigue_policy = load_json(ASSET_DIR / "fatigue-policy.json")
    evidence_policy = load_json(ASSET_DIR / "evidence-policy.json")
    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing required section {section}")
    if errors:
        return errors
    validate_system(report, errors)
    known = evidence(report, errors, evidence_policy)
    validate_severity(report, errors, severity_policy, known)
    escalations = validate_escalations(report, errors, escalation_policy, known)
    severities = set(severity_policy["allowed_severities"])
    validate_rules(report, errors, rule_policy, severities, escalations, known)
    validate_fatigue(report, errors, fatigue_policy, known)
    validate_routing(report, errors, known)
    validate_validation(report, errors, contract)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an alerting strategy JSON fixture")
    parser.add_argument("report")
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
