#!/usr/bin/env python3
"""Validate deterministic Constitution v6 compliance report fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def has_evidence_tag(value: Any, tags: list[str]) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return any(tag in text for tag in tags)


def validate_sections(report: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"missing section: {section}")
        elif is_blank(report[section]):
            errors.append(f"empty section: {section}")

    serialized = json.dumps(report, ensure_ascii=False).lower()
    for phrase in contract["blocked_phrases"]:
        if phrase.lower() in serialized:
            errors.append(f"blocked phrase present: {phrase}")
    if not has_evidence_tag(report, contract["allowed_evidence_tags"]):
        errors.append("missing evidence tag")


def validate_summary(report: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        return
    for field in contract["summary_fields"]:
        if field not in summary:
            errors.append(f"summary missing {field}")
    if summary.get("constitution_version") != "v6.0.0":
        errors.append("summary.constitution_version must be v6.0.0")
    if summary.get("overall_status") not in contract["overall_statuses"]:
        errors.append("summary.overall_status invalid")
    confidence = summary.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
        errors.append("summary.confidence must be 0-1")


def validate_principles(
    report: dict[str, Any],
    principles: dict[str, Any],
    contract: dict[str, Any],
    severity_policy: dict[str, Any],
    errors: list[str],
) -> tuple[int, int]:
    rows = report.get("principle_matrix")
    if not isinstance(rows, list):
        errors.append("principle_matrix must be a list")
        return 0, 0

    expected = {item["id"]: item["name"] for item in principles["principles"]}
    valid_statuses = set(contract["principle_statuses"])
    valid_severities = {item["id"] for item in severity_policy["severities"]}
    seen: set[int] = set()
    blocking = 0
    not_verified = 0

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"principle_matrix[{index}] must be an object")
            continue
        for field in contract["principle_fields"]:
            if field not in row:
                errors.append(f"principle_matrix[{index}] missing {field}")
        pid = row.get("principle_id")
        if pid not in expected:
            errors.append(f"principle_matrix[{index}].principle_id unknown: {pid}")
        else:
            seen.add(int(pid))
            if row.get("principle_name") != expected[pid]:
                errors.append(f"principle_matrix[{index}].principle_name mismatch")

        status = row.get("status")
        severity = row.get("severity")
        if status not in valid_statuses:
            errors.append(f"principle_matrix[{index}].status invalid")
        if severity not in valid_severities:
            errors.append(f"principle_matrix[{index}].severity invalid")
        if not isinstance(row.get("gate_impact"), list) or not row.get("gate_impact"):
            errors.append(f"principle_matrix[{index}].gate_impact must be non-empty list")
        if not has_evidence_tag(row.get("evidence"), contract["allowed_evidence_tags"]):
            errors.append(f"principle_matrix[{index}].evidence missing evidence tag")

        if status == "fail":
            if severity in {"P0", "P1"}:
                blocking += 1
            if is_blank(row.get("remediation")):
                errors.append(f"principle_matrix[{index}] fail requires remediation")
            if severity == "none":
                errors.append(f"principle_matrix[{index}] fail cannot use severity none")
        elif status == "not_verified":
            not_verified += 1
            if is_blank(row.get("missing_evidence")):
                errors.append(f"principle_matrix[{index}] not_verified requires missing_evidence")
            if is_blank(row.get("remediation")):
                errors.append(f"principle_matrix[{index}] not_verified requires remediation")
        elif status in {"pass", "not_applicable"}:
            if severity not in {"none", "P3"}:
                errors.append(f"principle_matrix[{index}] {status} cannot use severity {severity}")

    missing = set(expected) - seen
    extra = seen - set(expected)
    for pid in sorted(missing):
        errors.append(f"missing principle row: {pid}")
    for pid in sorted(extra):
        errors.append(f"unexpected principle row: {pid}")
    if len(rows) != len(expected):
        errors.append(f"principle_matrix must contain exactly {len(expected)} rows")
    return blocking, not_verified


def validate_gates(report: dict[str, Any], principles: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> int:
    rows = report.get("gate_impact")
    if not isinstance(rows, list):
        errors.append("gate_impact must be a list")
        return 0
    expected = {item["id"] for item in principles["gates"]}
    seen: set[str] = set()
    blocking = 0
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"gate_impact[{index}] must be an object")
            continue
        for field in contract["gate_impact_fields"]:
            if field not in row:
                errors.append(f"gate_impact[{index}] missing {field}")
        gate = row.get("gate")
        if gate not in expected:
            errors.append(f"gate_impact[{index}].gate invalid")
        else:
            seen.add(str(gate))
        if row.get("status") not in ["pass", "blocked", "not_verified", "not_applicable"]:
            errors.append(f"gate_impact[{index}].status invalid")
        if row.get("blocking") is True:
            blocking += 1
        if not has_evidence_tag(row.get("evidence"), contract["allowed_evidence_tags"]):
            errors.append(f"gate_impact[{index}].evidence missing evidence tag")
    for gate in sorted(expected - seen):
        errors.append(f"missing gate impact row: {gate}")
    return blocking


def validate_decision(
    report: dict[str, Any],
    contract: dict[str, Any],
    blocking_findings: int,
    not_verified_count: int,
    gate_blocks: int,
    errors: list[str],
) -> None:
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    decision = report.get("decision")
    if not isinstance(decision, dict):
        errors.append("decision must be an object")
        return
    for field in contract["decision_fields"]:
        if field not in decision:
            errors.append(f"decision missing {field}")

    if summary.get("blocking_findings") != blocking_findings:
        errors.append(f"summary.blocking_findings must be {blocking_findings}")
    if summary.get("not_verified_count") != not_verified_count:
        errors.append(f"summary.not_verified_count must be {not_verified_count}")

    overall = summary.get("overall_status")
    if (blocking_findings or gate_blocks) and overall != "blocked":
        errors.append("overall_status must be blocked when blocking findings or gate blocks exist")
    if not_verified_count and overall == "pass":
        errors.append("overall_status cannot be pass when evidence is not verified")
    if overall == "pass" and decision.get("release_decision") != "allow":
        errors.append("pass report requires decision.release_decision=allow")
    if overall == "blocked" and decision.get("release_decision") != "block":
        errors.append("blocked report requires decision.release_decision=block")


def validate_report(principles: dict[str, Any], contract: dict[str, Any], severity: dict[str, Any], report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validate_sections(report, contract, errors)
    validate_summary(report, contract, errors)
    blocking, not_verified = validate_principles(report, principles, contract, severity, errors)
    gate_blocks = validate_gates(report, principles, contract, errors)
    validate_decision(report, contract, blocking, not_verified, gate_blocks, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate constitution compliance report")
    parser.add_argument("--principles", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--severity", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        errors = validate_report(
            principles=load_json(args.principles),
            contract=load_json(args.contract),
            severity=load_json(args.severity),
            report=load_json(args.report),
        )
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    status = "fail" if errors else "pass"
    print(json.dumps({"status": status, "errors": errors}, indent=2, ensure_ascii=False))
    if args.expect:
        if status != args.expect:
            print(f"ERROR: expected {args.expect}, observed {status}", file=sys.stderr)
            return 1
        return 0
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
