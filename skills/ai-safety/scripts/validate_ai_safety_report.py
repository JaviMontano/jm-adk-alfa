#!/usr/bin/env python3
"""Validate deterministic AI safety reports."""

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
            errors.append(f"{path}: unknown id {ref}")


def validate_evidence(report: dict[str, Any], errors: list[str]) -> set[str]:
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence: must be a non-empty list")
        return set()
    allowed_tags = {"[EXPLICIT]", "[INFERRED]", "[OPEN]"}
    seen: set[str] = set()
    for index, item in enumerate(evidence):
        path = f"evidence[{index}]"
        require_fields(errors, item, path, ["id", "tag", "source", "summary"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if not is_non_empty_string(evidence_id):
            errors.append(f"{path}.id: must be non-empty")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate {evidence_id}")
        else:
            seen.add(evidence_id)
        if item.get("tag") not in allowed_tags:
            errors.append(f"{path}.tag: invalid")
        for field in ("source", "summary"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
    return seen


def validate_system(report: dict[str, Any], errors: list[str]) -> None:
    system = report.get("system")
    require_fields(errors, system, "system", ["name", "use_case", "risk_level", "high_stakes"])
    if not isinstance(system, dict):
        return
    for field in ("name", "use_case"):
        if not is_non_empty_string(system.get(field)):
            errors.append(f"system.{field}: must be non-empty")
    if system.get("risk_level") not in {"low", "medium", "high"}:
        errors.append("system.risk_level: must be low, medium, or high")
    if not isinstance(system.get("high_stakes"), bool):
        errors.append("system.high_stakes: must be boolean")


def validate_risks(report: dict[str, Any], errors: list[str], known_evidence: set[str], taxonomy: dict[str, Any]) -> dict[str, str]:
    risks = report.get("risk_assessment")
    if not isinstance(risks, list) or not risks:
        errors.append("risk_assessment: must be a non-empty list")
        return {}
    risk_severity: dict[str, str] = {}
    for index, item in enumerate(risks):
        path = f"risk_assessment[{index}]"
        require_fields(errors, item, path, ["id", "domain", "severity", "scenario", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        risk_id = item.get("id")
        if not is_non_empty_string(risk_id):
            errors.append(f"{path}.id: must be non-empty")
        else:
            risk_severity[str(risk_id)] = str(item.get("severity"))
        if item.get("domain") not in set(taxonomy["allowed_domains"]):
            errors.append(f"{path}.domain: invalid")
        if item.get("severity") not in set(taxonomy["allowed_severities"]):
            errors.append(f"{path}.severity: invalid")
        if not is_non_empty_string(item.get("scenario")):
            errors.append(f"{path}.scenario: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return risk_severity


def validate_controls(report: dict[str, Any], errors: list[str], known_evidence: set[str], risk_severity: dict[str, str], control_policy: dict[str, Any]) -> None:
    controls = report.get("controls")
    if not isinstance(controls, list) or not controls:
        errors.append("controls: must be a non-empty list")
        return
    covered: set[str] = set()
    for index, item in enumerate(controls):
        path = f"controls[{index}]"
        require_fields(errors, item, path, ["id", "control_type", "target_risk_ids", "action", "description", "test_oracle", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if item.get("control_type") not in set(control_policy["allowed_control_types"]):
            errors.append(f"{path}.control_type: invalid")
        action = item.get("action")
        if action not in set(control_policy["allowed_actions"]):
            errors.append(f"{path}.action: invalid")
        targets = item.get("target_risk_ids")
        if not isinstance(targets, list) or not targets:
            errors.append(f"{path}.target_risk_ids: must be a non-empty list")
        else:
            for risk_id in targets:
                if risk_id not in risk_severity:
                    errors.append(f"{path}.target_risk_ids: unknown risk {risk_id}")
                else:
                    covered.add(str(risk_id))
                    if risk_severity[str(risk_id)] == "critical" and action == "allow":
                        errors.append(f"{path}.action: critical risk cannot be allow")
        for field in ("description", "test_oracle"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = set(risk_severity) - covered
    if missing:
        errors.append(f"controls: uncovered risks {sorted(missing)}")


def validate_jailbreak_tests(report: dict[str, Any], errors: list[str], known_evidence: set[str], jailbreak_policy: dict[str, Any]) -> None:
    tests = report.get("jailbreak_tests")
    if not isinstance(tests, list) or not tests:
        errors.append("jailbreak_tests: must be a non-empty list")
        return
    for index, item in enumerate(tests):
        path = f"jailbreak_tests[{index}]"
        require_fields(errors, item, path, ["id", "attack_type", "expected_action", "oracle", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if item.get("attack_type") not in set(jailbreak_policy["allowed_attack_types"]):
            errors.append(f"{path}.attack_type: invalid")
        if item.get("expected_action") not in set(jailbreak_policy["allowed_expected_actions"]):
            errors.append(f"{path}.expected_action: invalid")
        if not is_non_empty_string(item.get("oracle")):
            errors.append(f"{path}.oracle: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_evaluation(report: dict[str, Any], errors: list[str], known_evidence: set[str], evaluation_policy: dict[str, Any]) -> None:
    evaluation = report.get("evaluation")
    require_fields(errors, evaluation, "evaluation", ["metrics"])
    if not isinstance(evaluation, dict):
        return
    metrics = evaluation.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        errors.append("evaluation.metrics: must be a non-empty list")
        return
    seen: set[str] = set()
    for index, item in enumerate(metrics):
        path = f"evaluation.metrics[{index}]"
        require_fields(errors, item, path, ["metric", "threshold", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        metric = item.get("metric")
        if metric not in set(evaluation_policy["allowed_metrics"]):
            errors.append(f"{path}.metric: invalid")
        else:
            seen.add(str(metric))
        if not is_non_empty_string(item.get("threshold")):
            errors.append(f"{path}.threshold: must be non-empty")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = set(evaluation_policy["required_metrics"]) - seen
    if missing:
        errors.append(f"evaluation.metrics: missing required metrics {sorted(missing)}")


def validate_escalation(report: dict[str, Any], errors: list[str]) -> None:
    escalation = report.get("escalation")
    require_fields(errors, escalation, "escalation", ["owner", "channels", "criteria"])
    if not isinstance(escalation, dict):
        return
    if not is_non_empty_string(escalation.get("owner")):
        errors.append("escalation.owner: must be non-empty")
    for field in ("channels", "criteria"):
        if not isinstance(escalation.get(field), list) or not escalation[field]:
            errors.append(f"escalation.{field}: must be a non-empty list")


def validate_validation(report: dict[str, Any], errors: list[str], required_checks: set[str]) -> None:
    validation = report.get("validation")
    require_fields(errors, validation, "validation", ["status", "checks"])
    if not isinstance(validation, dict):
        return
    if validation.get("status") not in {"pass", "warn", "block"}:
        errors.append("validation.status: invalid")
    checks = validation.get("checks")
    if not isinstance(checks, list):
        errors.append("validation.checks: must be a list")
    else:
        missing = required_checks - set(checks)
        if missing:
            errors.append(f"validation.checks: missing required checks {sorted(missing)}")


def validate_report(report_path: Path) -> list[str]:
    errors: list[str] = []
    report = load_json(report_path)
    if not isinstance(report, dict):
        return ["report: must be a JSON object"]
    contract = load_json(ASSET_DIR / "safety-report-contract.json")
    taxonomy = load_json(ASSET_DIR / "risk-taxonomy.json")
    control_policy = load_json(ASSET_DIR / "control-policy.json")
    jailbreak_policy = load_json(ASSET_DIR / "jailbreak-policy.json")
    evaluation_policy = load_json(ASSET_DIR / "evaluation-policy.json")

    require_fields(errors, report, "report", contract["required_top_level_fields"])
    if report.get("schema") != contract["report_schema"]:
        errors.append(f"schema: must be {contract['report_schema']}")
    known_evidence = validate_evidence(report, errors)
    validate_system(report, errors)
    risk_severity = validate_risks(report, errors, known_evidence, taxonomy)
    validate_controls(report, errors, known_evidence, risk_severity, control_policy)
    validate_jailbreak_tests(report, errors, known_evidence, jailbreak_policy)
    validate_evaluation(report, errors, known_evidence, evaluation_policy)
    validate_escalation(report, errors)
    validate_validation(report, errors, set(contract["required_validation_checks"]))
    if not isinstance(report.get("risks"), list):
        errors.append("risks: must be a list")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI safety report")
    parser.add_argument("report", help="Path to report JSON fixture")
    args = parser.parse_args()
    report_path = Path(args.report)
    try:
        errors = validate_report(report_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {report_path}: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR {report_path}: {error}", file=sys.stderr)
        return 1
    print(f"report={report_path.name} status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
