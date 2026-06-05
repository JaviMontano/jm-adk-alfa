#!/usr/bin/env python3
"""Validate deterministic code-review-checklist report fixtures."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_report(report: dict[str, Any], taxonomy: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed_tags = evidence.get("allowed_tags", [])
    statuses = taxonomy.get("statuses", [])
    domains = taxonomy.get("domains", [])
    decisions = taxonomy.get("decisions", [])
    check_defs = {item["id"]: item for item in taxonomy.get("checks", [])}
    blocking_checks = set(taxonomy.get("blocking_checks", []))

    for section in contract.get("required_sections", []):
        if section not in report:
            errors.append(f"missing section: {section}")

    scope = report.get("scope", {})
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        for field in contract.get("scope_fields", []):
            if field not in scope:
                errors.append(f"scope missing field: {field}")

    scores = report.get("scores", {})
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
    else:
        for field in contract.get("score_fields", []):
            value = scores.get(field)
            if not isinstance(value, int) or value < 0 or value > 100:
                errors.append(f"score {field} must be integer 0..100")

    checks = report.get("checks", [])
    if not isinstance(checks, list):
        errors.append("checks must be a list")
        checks = []

    failed_blocking: list[str] = []
    seen_checks: set[str] = set()
    for item in checks:
        if not isinstance(item, dict):
            errors.append("check item must be object")
            continue
        for field in contract.get("check_fields", []):
            if field not in item:
                errors.append(f"check missing field: {field}")
        check_id = item.get("id")
        seen_checks.add(str(check_id))
        if check_id not in check_defs:
            errors.append(f"unknown check id: {check_id}")
        if item.get("domain") not in domains:
            errors.append(f"{check_id} invalid domain: {item.get('domain')}")
        if item.get("status") not in statuses:
            errors.append(f"{check_id} invalid status: {item.get('status')}")
        if item.get("evidence_tag") not in allowed_tags:
            errors.append(f"{check_id} invalid evidence_tag: {item.get('evidence_tag')}")
        source = item.get("source")
        if not isinstance(source, dict):
            errors.append(f"{check_id} source must be object")
        else:
            if not str(source.get("file", "")).strip():
                errors.append(f"{check_id} source.file is required")
            line = source.get("line")
            if line is not None and (not isinstance(line, int) or line < 1):
                errors.append(f"{check_id} source.line must be positive integer or null")
        if not str(item.get("why", "")).strip():
            errors.append(f"{check_id} why is required")
        if check_id in blocking_checks and item.get("status") == "fail":
            failed_blocking.append(str(check_id))

    findings = report.get("findings", [])
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    expected_finding_ids = [f"CRCF-{index:03d}" for index in range(1, len(findings) + 1)]
    actual_finding_ids = [str(item.get("id", "")) for item in findings if isinstance(item, dict)]
    if actual_finding_ids != expected_finding_ids:
        errors.append(f"finding ids must be gapless: expected {expected_finding_ids}, got {actual_finding_ids}")
    for item in findings:
        if not isinstance(item, dict):
            errors.append("finding must be object")
            continue
        for field in contract.get("finding_fields", []):
            if field not in item:
                errors.append(f"{item.get('id', '<unknown>')} missing field: {field}")
        if item.get("check_id") not in check_defs:
            errors.append(f"{item.get('id', '<unknown>')} references unknown check")
        if item.get("severity") not in contract.get("finding_severities", []):
            errors.append(f"{item.get('id', '<unknown>')} invalid severity")
        if item.get("evidence_tag") not in allowed_tags:
            errors.append(f"{item.get('id', '<unknown>')} invalid evidence_tag")
        if not isinstance(item.get("line"), int) or item.get("line") < 1:
            errors.append(f"{item.get('id', '<unknown>')} line must be positive integer")
        if re.search(r"sk-[A-Za-z0-9]{20,}", str(item.get("claim", ""))):
            errors.append(f"{item.get('id', '<unknown>')} appears to echo a secret")

    positive = report.get("positive_evidence", [])
    if not isinstance(positive, list):
        errors.append("positive_evidence must be a list")
        positive = []
    for item in positive:
        if not isinstance(item, dict):
            errors.append("positive_evidence item must be object")
            continue
        if item.get("evidence_tag") not in allowed_tags:
            errors.append("positive_evidence evidence_tag invalid")

    validation = report.get("validation", {})
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        for field in contract.get("validation_fields", []):
            if field not in validation:
                errors.append(f"validation missing field: {field}")
        if sorted(validation.get("blocking_failures", [])) != sorted(failed_blocking):
            errors.append("validation.blocking_failures must match failed blocking checks")

    decision = report.get("decision", {})
    decision_value = None
    if not isinstance(decision, dict):
        errors.append("decision must be an object")
    else:
        for field in contract.get("decision_fields", []):
            if field not in decision:
                errors.append(f"decision missing field: {field}")
        decision_value = decision.get("release_decision")
        if decision_value not in decisions:
            errors.append(f"invalid release_decision: {decision_value}")

    missing_inputs = scope.get("minimum_inputs_missing", []) if isinstance(scope, dict) else []
    if failed_blocking and decision_value != "request_changes":
        errors.append("blocking failures require request_changes")
    if not failed_blocking and findings and decision_value == "request_changes":
        errors.append("request_changes requires a blocking failure")
    if missing_inputs and not checks and decision_value != "needs_context":
        errors.append("missing minimum inputs without checks require needs_context")
    if not findings and not failed_blocking and not missing_inputs and decision_value == "approve" and not positive:
        errors.append("approve requires positive_evidence")

    full_text = json.dumps(report, ensure_ascii=False).lower()
    for phrase in contract.get("forbidden_phrases", []):
        if phrase.lower() in full_text:
            errors.append(f"forbidden phrase present: {phrase}")

    if report.get("mode") and report.get("mode") != "read_only":
        errors.append("mode must be read_only when present")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a code-review-checklist report fixture")
    parser.add_argument("--taxonomy", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--boundary", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--expect", choices=["pass", "fail"], required=True)
    args = parser.parse_args()

    taxonomy = load_json(Path(args.taxonomy))
    contract = load_json(Path(args.contract))
    evidence = load_json(Path(args.evidence))
    load_json(Path(args.boundary))
    report = load_json(Path(args.report))
    if not isinstance(report, dict):
        print("ERROR: report root must be object")
        return 1

    errors = validate_report(report, taxonomy, contract, evidence)
    passed = not errors
    expected_pass = args.expect == "pass"
    if passed != expected_pass:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"expected={args.expect} actual={'pass' if passed else 'fail'}")
        return 1
    print(f"OK: {Path(args.report).name} {'passed' if passed else 'failed as expected'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
