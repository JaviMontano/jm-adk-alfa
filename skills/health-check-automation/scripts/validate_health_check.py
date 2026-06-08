#!/usr/bin/env python3
"""Validate deterministic health-check reports for health-check-automation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


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


def string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(non_empty_string(item) for item in value)


def object_at(report: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = report.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def list_at(report: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = report.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return []
    return value


def validate_resource_check(check: dict[str, Any], errors: list[str]) -> None:
    for field in ["unit", "observed", "warning_threshold", "critical_threshold"]:
        if field not in check:
            errors.append(f"resource check {check.get('id', '<unknown>')} missing {field}")
    if check.get("unit") not in policy("resource-policy.json")["allowed_units"]:
        errors.append(f"resource check {check.get('id', '<unknown>')} has unsupported unit")

    observed = check.get("observed")
    warning = check.get("warning_threshold")
    critical = check.get("critical_threshold")
    status = check.get("status")
    if not all(isinstance(v, (int, float)) for v in [observed, warning, critical]):
        errors.append(f"resource check {check.get('id', '<unknown>')} thresholds must be numeric")
        return
    if warning >= critical:
        errors.append(f"resource check {check.get('id', '<unknown>')} warning_threshold must be below critical_threshold")
    if observed >= critical and status != "fail":
        errors.append(f"resource check {check.get('id', '<unknown>')} at critical threshold must fail")
    elif observed >= warning and status not in {"warn", "fail"}:
        errors.append(f"resource check {check.get('id', '<unknown>')} at warning threshold must warn or fail")
    elif observed < warning and status != "pass":
        errors.append(f"resource check {check.get('id', '<unknown>')} below warning threshold must pass")


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("health-check-contract.json")
    alert_policy = policy("alert-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")

    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "health-check-automation":
        errors.append("skill must be health-check-automation")
    if not non_empty_string(report.get("scenario_id")):
        errors.append("scenario_id must be a non-empty string")

    allowed_overall = set(contract["json_contract"]["allowed_overall_statuses"])
    allowed_check_statuses = set(contract["json_contract"]["allowed_check_statuses"])
    overall = report.get("overall_status")
    if overall not in allowed_overall:
        errors.append(f"overall_status must be one of {sorted(allowed_overall)}")

    snapshot = object_at(report, "snapshot", errors)
    for field in evidence_policy["required_snapshot_fields"]:
        if not non_empty_string(snapshot.get(field)):
            errors.append(f"snapshot.{field} must be a non-empty string")
    if snapshot.get("freshness") not in evidence_policy["allowed_freshness"]:
        errors.append(f"snapshot.freshness must be one of {evidence_policy['allowed_freshness']}")
    if overall == "healthy" and snapshot.get("freshness") != "fresh":
        errors.append("overall healthy requires fresh snapshot evidence")

    checks = list_at(report, "checks", errors)
    if not checks:
        errors.append("checks must not be empty")

    required_statuses: list[str] = []
    warn_or_fail_checks: list[str] = []
    required_unknown = False
    required_fail = False
    required_warn = False

    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"checks[{index}] must be an object")
            continue
        check_id = check.get("id", f"checks[{index}]")
        for field in ["id", "kind", "type", "required", "status", "evidence"]:
            if field not in check:
                errors.append(f"check {check_id} missing {field}")
        if not non_empty_string(check.get("id")):
            errors.append(f"check {check_id} id must be non-empty")
        if check.get("kind") not in {"service", "dependency", "resource"}:
            errors.append(f"check {check_id} kind must be service, dependency, or resource")
        if not isinstance(check.get("required"), bool):
            errors.append(f"check {check_id} required must be boolean")
        status = check.get("status")
        if status not in allowed_check_statuses:
            errors.append(f"check {check_id} status must be one of {sorted(allowed_check_statuses)}")
        if not non_empty_string(check.get("evidence")):
            errors.append(f"check {check_id} evidence must be non-empty")

        if check.get("kind") == "dependency" and not non_empty_string(check.get("owner")):
            errors.append(f"dependency check {check_id} owner must be non-empty")
        if check.get("kind") == "resource":
            validate_resource_check(check, errors)

        if check.get("required") is True:
            required_statuses.append(status)
            if status == "unknown":
                required_unknown = True
            if status == "fail":
                required_fail = True
            if status == "warn":
                required_warn = True
        if status in {"warn", "fail"}:
            warn_or_fail_checks.append(str(check_id))

    if overall == "healthy" and any(status != "pass" for status in required_statuses):
        errors.append("overall healthy requires every required check to pass")
    if overall == "healthy" and not required_statuses:
        errors.append("overall healthy requires at least one required check")
    if required_unknown and overall != "blocked":
        errors.append("required unknown checks require overall_status=blocked")
    if required_fail and overall not in {"unhealthy", "degraded"}:
        errors.append("required fail checks require unhealthy or degraded overall status")
    if required_warn and overall == "healthy":
        errors.append("required warn checks cannot be overall healthy")

    alerts = object_at(report, "alerts", errors)
    if not non_empty_string(alerts.get("severity")):
        errors.append("alerts.severity must be a non-empty string")
    elif alerts.get("severity") not in alert_policy["allowed_severities"]:
        errors.append(f"alerts.severity must be one of {alert_policy['allowed_severities']}")
    if warn_or_fail_checks or overall in {"degraded", "unhealthy", "blocked"}:
        for field in alert_policy["required_fields_when_not_healthy"]:
            value = alerts.get(field)
            if field == "handoff":
                if not string_list(value):
                    errors.append("alerts.handoff must be a non-empty list when not healthy")
            elif not non_empty_string(value):
                errors.append(f"alerts.{field} must be non-empty when not healthy")
    if any(
        isinstance(check, dict) and check.get("status") == "fail"
        for check in checks
    ) and alerts.get("severity") != "critical":
        errors.append("fail checks require critical alert severity")

    degradation = object_at(report, "degradation", errors)
    if overall == "healthy":
        if degradation.get("active") is not False:
            errors.append("healthy reports require degradation.active=false")
    else:
        if degradation.get("active") is not True:
            errors.append("non-healthy reports require degradation.active=true")
        for field in ["mode", "reason", "next_action"]:
            if not non_empty_string(degradation.get(field)):
                errors.append(f"degradation.{field} must be non-empty when not healthy")

    validation = object_at(report, "validation", errors)
    for field in evidence_policy["required_validation_fields"]:
        if not string_list(validation.get(field)):
            errors.append(f"validation.{field} must be a non-empty list")

    guardian = object_at(report, "guardian", errors)
    if guardian.get("decision") not in {"pass", "warn", "block"}:
        errors.append("guardian.decision must be pass, warn, or block")
    if overall == "healthy" and guardian.get("decision") != "pass":
        errors.append("healthy report requires guardian.decision=pass")
    if overall == "blocked" and guardian.get("decision") != "block":
        errors.append("blocked report requires guardian.decision=block")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a health-check JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON health-check report")
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
