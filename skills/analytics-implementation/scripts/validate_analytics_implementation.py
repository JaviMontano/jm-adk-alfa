#!/usr/bin/env python3
"""Validate deterministic analytics implementation plans."""

from __future__ import annotations

import argparse
import json
import re
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


def validate_evidence(report: dict[str, Any], errors: list[str], policy: dict[str, Any]) -> set[str]:
    items = report.get("evidence")
    if not isinstance(items, list) or not items:
        errors.append("evidence: must be a non-empty list")
        return set()
    allowed = set(policy["allowed_tags"])
    seen: set[str] = set()
    for index, item in enumerate(items):
        path = f"evidence[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if is_text(evidence_id):
            if evidence_id in seen:
                errors.append(f"{path}.id: duplicate {evidence_id}")
            seen.add(str(evidence_id))
        else:
            errors.append(f"{path}.id: must be non-empty")
        if item.get("tag") not in allowed:
            errors.append(f"{path}.tag: invalid")
        for field in ("source", "summary"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
    return seen


def validate_system(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    system = report.get("system")
    require(errors, system, "system", contract["required_system_fields"])
    if not isinstance(system, dict):
        return
    for field in ("name", "scope"):
        if not is_text(system.get(field)):
            errors.append(f"system.{field}: must be non-empty")
    for field in ("platforms", "tools"):
        values = system.get(field)
        if not isinstance(values, list) or not values or not all(is_text(value) for value in values):
            errors.append(f"system.{field}: must be a non-empty list")


def validate_setup(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> None:
    items = report.get("ga4_setup")
    if not isinstance(items, list) or not items:
        errors.append("ga4_setup: must be a non-empty list")
        return
    for index, item in enumerate(items):
        path = f"ga4_setup[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        if item.get("tool") not in set(policy["allowed_tools"]):
            errors.append(f"{path}.tool: invalid")
        if item.get("consent_policy") not in set(policy["required_consent_values"]):
            errors.append(f"{path}.consent_policy: invalid")
        for field in ("surface", "owner", "validation_method"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")


def validate_events(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> set[str]:
    items = report.get("events")
    if not isinstance(items, list) or not items:
        errors.append("events: must be a non-empty list")
        return set()
    pattern = re.compile(policy["event_name_pattern"])
    allowed_types = set(policy["allowed_types"])
    allowed_pii = set(policy["allowed_pii"])
    blocked = set(policy["blocked_names"])
    names: set[str] = set()
    for index, item in enumerate(items):
        path = f"events[{index}]"
        require(errors, item, path, policy["required_event_fields"])
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if is_text(name):
            event_name = str(name)
            names.add(event_name)
            if not pattern.match(event_name) or len(event_name) > int(policy["max_event_name_length"]):
                errors.append(f"{path}.name: invalid")
        else:
            errors.append(f"{path}.name: must be non-empty")
        for field in ("trigger", "platform", "owner", "destination", "validation_method"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        parameters = item.get("parameters")
        if not isinstance(parameters, list) or not parameters:
            errors.append(f"{path}.parameters: must be a non-empty list")
        else:
            for p_index, param in enumerate(parameters):
                p_path = f"{path}.parameters[{p_index}]"
                require(errors, param, p_path, policy["required_parameter_fields"])
                if not isinstance(param, dict):
                    continue
                param_name = param.get("name")
                if not is_text(param_name):
                    errors.append(f"{p_path}.name: must be non-empty")
                elif str(param_name) in blocked:
                    errors.append(f"{p_path}.name: blocked raw personal data")
                if param.get("type") not in allowed_types:
                    errors.append(f"{p_path}.type: invalid")
                if param.get("pii") not in allowed_pii:
                    errors.append(f"{p_path}.pii: invalid")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")
    return names


def validate_named_list(report: dict[str, Any], errors: list[str], section: str) -> None:
    if not isinstance(report.get(section), list):
        errors.append(f"{section}: must be a list")


def validate_conversions(report: dict[str, Any], errors: list[str], policy: dict[str, Any], events: set[str], known: set[str]) -> None:
    validate_named_list(report, errors, "conversions")
    for index, item in enumerate(report.get("conversions", [])):
        path = f"conversions[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        if item.get("event_name") not in events:
            errors.append(f"{path}.event_name: unknown")
        for field in ("owner", "condition", "validation_method"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")


def validate_user_properties(report: dict[str, Any], errors: list[str], event_policy: dict[str, Any], known: set[str]) -> None:
    validate_named_list(report, errors, "user_properties")
    allowed_types = set(event_policy["allowed_types"])
    allowed_pii = set(event_policy["allowed_pii"])
    blocked = set(event_policy["blocked_names"])
    for index, item in enumerate(report.get("user_properties", [])):
        path = f"user_properties[{index}]"
        require(errors, item, path, ["name", "type", "description", "pii", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not is_text(name):
            errors.append(f"{path}.name: must be non-empty")
        elif str(name) in blocked:
            errors.append(f"{path}.name: blocked raw personal data")
        if item.get("type") not in allowed_types:
            errors.append(f"{path}.type: invalid")
        if item.get("pii") not in allowed_pii:
            errors.append(f"{path}.pii: invalid")
        if not is_text(item.get("description")):
            errors.append(f"{path}.description: must be non-empty")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")


def validate_bigquery(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> None:
    item = report.get("bigquery_export")
    require(errors, item, "bigquery_export", policy["required_fields"])
    if not isinstance(item, dict):
        return
    if item.get("enabled") is not policy["enabled_required"]:
        errors.append("bigquery_export.enabled: must be true")
    for field in ("dataset", "location", "retention", "partitioning", "pii_handling", "owner", "validation_method"):
        if not is_text(item.get(field)):
            errors.append(f"bigquery_export.{field}: must be non-empty")
    refs(errors, item.get("evidence_ids"), known, "bigquery_export.evidence_ids")


def validate_dashboards(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known: set[str]) -> None:
    items = report.get("dashboards")
    if not isinstance(items, list) or not items:
        errors.append("dashboards: must be a non-empty list")
        return
    for index, item in enumerate(items):
        path = f"dashboards[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        for field in ("name", "data_source", "owner", "freshness", "validation_method"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        metrics = item.get("metrics")
        if not isinstance(metrics, list) or not metrics or not all(is_text(metric) for metric in metrics):
            errors.append(f"{path}.metrics: must be a non-empty list")
        refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")


def validate_steps(report: dict[str, Any], errors: list[str], known: set[str]) -> None:
    items = report.get("implementation_steps")
    if not isinstance(items, list) or not items:
        errors.append("implementation_steps: must be a non-empty list")
        return
    for index, item in enumerate(items):
        path = f"implementation_steps[{index}]"
        require(errors, item, path, ["id", "task", "owner", "validation_method", "evidence_ids"])
        if isinstance(item, dict):
            for field in ("id", "task", "owner", "validation_method"):
                if not is_text(item.get(field)):
                    errors.append(f"{path}.{field}: must be non-empty")
            refs(errors, item.get("evidence_ids"), known, f"{path}.evidence_ids")


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
    contract = load_json(ASSET_DIR / "analytics-implementation-contract.json")
    ga4_policy = load_json(ASSET_DIR / "ga4-policy.json")
    event_policy = load_json(ASSET_DIR / "event-policy.json")
    conversion_policy = load_json(ASSET_DIR / "conversion-policy.json")
    bigquery_policy = load_json(ASSET_DIR / "bigquery-policy.json")
    dashboard_policy = load_json(ASSET_DIR / "dashboard-policy.json")
    evidence_policy = load_json(ASSET_DIR / "evidence-policy.json")
    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing required section {section}")
    if errors:
        return errors
    validate_system(report, errors, contract)
    known = validate_evidence(report, errors, evidence_policy)
    validate_setup(report, errors, ga4_policy, known)
    events = validate_events(report, errors, event_policy, known)
    validate_conversions(report, errors, conversion_policy, events, known)
    validate_user_properties(report, errors, event_policy, known)
    validate_bigquery(report, errors, bigquery_policy, known)
    validate_dashboards(report, errors, dashboard_policy, known)
    validate_steps(report, errors, known)
    validate_validation(report, errors, contract)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an analytics implementation JSON plan")
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
