#!/usr/bin/env python3
"""Validate deterministic audit-security JSON reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected list")
    return value


def validate_required_fields(item: dict[str, Any], fields: list[str], label: str) -> list[str]:
    errors: list[str] = []
    for field in fields:
        if field not in item:
            errors.append(f"{label}: missing field {field}")
        elif isinstance(item[field], str) and not item[field].strip():
            errors.append(f"{label}.{field}: must not be empty")
        elif isinstance(item[field], list) and field not in {"files_skipped"} and not item[field]:
            errors.append(f"{label}.{field}: must not be empty")
    return errors


def find_blocked_phrase(value: Any, phrases: list[str], path: str = "$") -> str | None:
    if isinstance(value, str):
        lower = value.lower()
        for phrase in phrases:
            if phrase.lower() in lower:
                return f"{path}: blocked phrase: {phrase}"
    elif isinstance(value, dict):
        for key, item in value.items():
            found = find_blocked_phrase(item, phrases, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = find_blocked_phrase(item, phrases, f"{path}[{index}]")
            if found:
                return found
    return None


def expected_overall_status(critical_count: int, warning_count: int) -> str:
    if critical_count:
        return "blocked"
    if warning_count:
        return "needs_review"
    return "pass"


def validate_report(
    report: dict[str, Any],
    contract: dict[str, Any],
    scan_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing section {section}")
    if errors:
        return errors

    blocked = find_blocked_phrase(report, list(contract.get("blocked_phrases", [])))
    if blocked:
        errors.append(blocked)

    summary = require_object(report["summary"], "summary")
    errors.extend(validate_required_fields(summary, contract["summary_fields"], "summary"))

    categories = list(scan_policy["categories"])
    categories_executed = require_list(report["categories_executed"], "categories_executed")
    if categories_executed != categories:
        errors.append(f"categories_executed: expected exact category order {categories}")

    findings_raw = require_list(report["findings"], "findings")
    findings = [require_object(item, f"findings[{index}]") for index, item in enumerate(findings_raw)]
    allowed_severities = set(scan_policy["severities"])
    allowed_statuses = set(scan_policy["finding_statuses"])
    finding_id_re = re.compile(r"^SEC-[0-9]{3}$")
    expected_ids = [f"SEC-{index:03d}" for index in range(1, len(findings) + 1)]
    actual_ids = [str(item.get("id", "")) for item in findings]
    if actual_ids != expected_ids:
        errors.append(f"findings: ids must be ascending and gapless: {expected_ids}")

    severity_counts = {"CRITICAL": 0, "WARNING": 0, "INFO": 0}
    finding_by_id: dict[str, dict[str, Any]] = {}
    placeholder_patterns = list(scan_policy["placeholder_patterns"])
    for index, item in enumerate(findings):
        label = f"findings[{index}]"
        errors.extend(validate_required_fields(item, contract["finding_fields"], label))
        finding_id = str(item.get("id", ""))
        if not finding_id_re.fullmatch(finding_id):
            errors.append(f"{label}.id: must match SEC-NNN")
        finding_by_id[finding_id] = item
        category = item.get("category")
        if category not in categories:
            errors.append(f"{label}.category: unsupported category {category}")
        severity = item.get("severity")
        if severity not in allowed_severities:
            errors.append(f"{label}.severity: unsupported severity {severity}")
        else:
            severity_counts[str(severity)] += 1
        status = item.get("status")
        if status not in allowed_statuses:
            errors.append(f"{label}.status: unsupported status {status}")
        line = item.get("line")
        if not isinstance(line, int) or line < 1:
            errors.append(f"{label}.line: must be a positive integer")
        evidence = str(item.get("evidence", ""))
        if not any(tag in evidence for tag in evidence_policy["allowed_tags"]):
            errors.append(f"{label}.evidence: missing allowed evidence tag")
        pattern = str(item.get("pattern", ""))
        if any(token in pattern or token in evidence for token in placeholder_patterns):
            if severity != "INFO" or status != "placeholder":
                errors.append(f"{label}: placeholder/example secrets must be INFO with status placeholder")
        if severity in {"CRITICAL", "WARNING"} and len(str(item.get("remediation", "")).strip()) < 18:
            errors.append(f"{label}.remediation: CRITICAL/WARNING findings require specific remediation")

    expected_summary_counts = {
        "total_findings": len(findings),
        "critical_count": severity_counts["CRITICAL"],
        "warning_count": severity_counts["WARNING"],
        "info_count": severity_counts["INFO"],
        "categories_executed_count": len(categories),
    }
    for key, expected in expected_summary_counts.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key}: expected {expected}, got {summary.get(key)}")
    expected_status = expected_overall_status(severity_counts["CRITICAL"], severity_counts["WARNING"])
    if summary.get("overall_status") != expected_status:
        errors.append(f"summary.overall_status: expected {expected_status}, got {summary.get('overall_status')}")

    remediation_plan = [
        require_object(item, f"remediation_plan[{index}]")
        for index, item in enumerate(require_list(report["remediation_plan"], "remediation_plan"))
    ]
    remediation_ids = {str(item.get("finding_id", "")) for item in remediation_plan}
    for index, item in enumerate(remediation_plan):
        errors.extend(validate_required_fields(item, contract["remediation_fields"], f"remediation_plan[{index}]"))
        if item.get("finding_id") not in finding_by_id:
            errors.append(f"remediation_plan[{index}].finding_id: unknown finding")
        if item.get("priority") not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"remediation_plan[{index}].priority: unsupported priority")
    required_remediation = {
        finding_id
        for finding_id, item in finding_by_id.items()
        if item.get("severity") in {"CRITICAL", "WARNING"}
    }
    missing_remediation = sorted(required_remediation - remediation_ids)
    if missing_remediation:
        errors.append(f"remediation_plan: missing entries for {missing_remediation}")

    coverage = require_object(report["coverage"], "coverage")
    errors.extend(validate_required_fields(coverage, contract["coverage_fields"], "coverage"))
    if not isinstance(coverage.get("files_scanned"), int) or coverage.get("files_scanned") < 0:
        errors.append("coverage.files_scanned: must be non-negative integer")

    forbidden_tags = list(evidence_policy.get("forbidden_tags", []))
    text = json.dumps(report, ensure_ascii=False)
    for tag in forbidden_tags:
        if tag in text:
            errors.append(f"report: forbidden evidence tag appears: {tag}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate audit-security report fixtures")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--scan-policy", required=True, type=Path)
    parser.add_argument("--evidence-policy", required=True, type=Path)
    args = parser.parse_args()

    try:
        report = require_object(load_json(args.report), "report")
        contract = require_object(load_json(args.contract), "contract")
        scan_policy = require_object(load_json(args.scan_policy), "scan_policy")
        evidence_policy = require_object(load_json(args.evidence_policy), "evidence_policy")
        errors = validate_report(report, contract, scan_policy, evidence_policy)
    except ValueError as exc:
        errors = [str(exc)]

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"report={args.report} valid=false errors={len(errors)}")
        return 1
    print(f"report={args.report} valid=true errors=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
