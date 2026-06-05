#!/usr/bin/env python3
"""Validate deterministic code-review report fixtures."""

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


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_report(report: dict[str, Any], taxonomy: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_sections = contract.get("required_sections", [])
    for section in required_sections:
        if section not in report:
            errors.append(f"missing section: {section}")

    severities = taxonomy.get("severities", [])
    categories = taxonomy.get("categories", [])
    decisions = contract.get("release_decisions", [])
    allowed_tags = evidence.get("allowed_tags", [])

    scope = report.get("scope", {})
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        for field in contract.get("scope_fields", []):
            if field not in scope:
                errors.append(f"scope missing field: {field}")

    findings = report.get("findings", [])
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []

    expected_ids = [f"CR-{index:03d}" for index in range(1, len(findings) + 1)]
    actual_ids = [str(item.get("id", "")) for item in findings if isinstance(item, dict)]
    if actual_ids != expected_ids:
        errors.append(f"finding ids must be gapless: expected {expected_ids}, got {actual_ids}")

    has_blocker = False
    for item in findings:
        if not isinstance(item, dict):
            errors.append("finding must be an object")
            continue
        for field in contract.get("finding_fields", []):
            if field not in item:
                errors.append(f"{item.get('id', '<unknown>')} missing field: {field}")
        severity = item.get("severity")
        category = item.get("category")
        tag = item.get("evidence_tag")
        if severity not in severities:
            errors.append(f"{item.get('id', '<unknown>')} invalid severity: {severity}")
        if category not in categories or category == "positive":
            errors.append(f"{item.get('id', '<unknown>')} invalid finding category: {category}")
        if tag not in allowed_tags:
            errors.append(f"{item.get('id', '<unknown>')} invalid evidence_tag: {tag}")
        line = item.get("line")
        if not isinstance(line, int) or line < 1:
            errors.append(f"{item.get('id', '<unknown>')} line must be positive integer")
        if not str(item.get("file", "")).strip():
            errors.append(f"{item.get('id', '<unknown>')} file is required")
        claim = str(item.get("claim", ""))
        action = str(item.get("suggested_action", ""))
        if not claim.strip():
            errors.append(f"{item.get('id', '<unknown>')} claim is required")
        if not action.strip():
            errors.append(f"{item.get('id', '<unknown>')} suggested_action is required")
        if severity == "BLOCKER":
            has_blocker = True
        if re.search(r"sk-[A-Za-z0-9]{20,}", claim):
            errors.append(f"{item.get('id', '<unknown>')} appears to echo a secret")

    positive_patterns = report.get("positive_patterns", [])
    if not isinstance(positive_patterns, list):
        errors.append("positive_patterns must be a list")
        positive_patterns = []
    for pattern in positive_patterns:
        if not isinstance(pattern, dict):
            errors.append("positive pattern must be an object")
            continue
        for field in contract.get("positive_pattern_fields", []):
            if field not in pattern:
                errors.append(f"positive pattern missing field: {field}")
        if pattern.get("evidence_tag") not in allowed_tags:
            errors.append("positive pattern evidence_tag invalid")

    validation = report.get("validation", {})
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        for field in contract.get("validation_fields", []):
            if field not in validation:
                errors.append(f"validation missing field: {field}")

    decision = report.get("decision", {})
    if not isinstance(decision, dict):
        errors.append("decision must be an object")
        decision_value = None
    else:
        for field in contract.get("decision_fields", []):
            if field not in decision:
                errors.append(f"decision missing field: {field}")
        decision_value = decision.get("release_decision")
        if decision_value not in decisions:
            errors.append(f"invalid release_decision: {decision_value}")

    missing_inputs = []
    if isinstance(scope, dict):
        missing_inputs = as_list(scope.get("minimum_inputs_missing"))

    if has_blocker and decision_value != "request_changes":
        errors.append("BLOCKER findings require request_changes")
    if missing_inputs and decision_value != "needs_context" and not findings:
        errors.append("missing inputs without findings require needs_context")
    if not findings and not missing_inputs and decision_value == "approve" and not positive_patterns:
        errors.append("approve with no findings requires positive_patterns")
    if not findings and decision_value == "request_changes":
        errors.append("request_changes requires at least one finding")

    full_text = json.dumps(report, ensure_ascii=False).lower()
    for phrase in contract.get("forbidden_phrases", []):
        if phrase.lower() in full_text:
            errors.append(f"forbidden phrase present: {phrase}")

    if report.get("mode") and report.get("mode") != "read_only":
        errors.append("mode must be read_only when present")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a code-review report fixture")
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
