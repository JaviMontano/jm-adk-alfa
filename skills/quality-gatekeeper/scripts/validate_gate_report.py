#!/usr/bin/env python3
"""Validate deterministic quality gatekeeper report fixtures."""

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


def blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def contains_tag(value: Any, tags: list[str]) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return any(tag in text for tag in tags)


def criteria_by_id(gates: dict[str, Any]) -> dict[str, dict[str, Any]]:
    criteria: dict[str, dict[str, Any]] = {}
    for gate in gates["gates"]:
        for item in gate["criteria"]:
            criteria[item["id"]] = {"gate": gate["id"], **item}
    return criteria


def scoped_criteria(gates: dict[str, Any], scope: list[str]) -> dict[str, dict[str, Any]]:
    allowed = set(scope)
    return {
        cid: item
        for cid, item in criteria_by_id(gates).items()
        if item["gate"] in allowed
    }


def validate_sections(report: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any], errors: list[str]) -> None:
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"missing section: {section}")
        elif blank(report[section]):
            errors.append(f"empty section: {section}")
    serialized = json.dumps(report, ensure_ascii=False).lower()
    for phrase in contract["blocked_phrases"]:
        if phrase in serialized:
            errors.append(f"blocked phrase present: {phrase}")
    if not contains_tag(report, evidence["allowed_evidence_tags"]):
        errors.append("missing evidence tag")


def validate_summary(report: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> list[str]:
    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        return []
    for field in contract["summary_fields"]:
        if field not in summary:
            errors.append(f"summary missing {field}")
    scope = summary.get("gate_scope")
    if not isinstance(scope, list) or not scope:
        errors.append("summary.gate_scope must be a non-empty list")
        scope = []
    if summary.get("overall_status") not in contract["overall_statuses"]:
        errors.append("summary.overall_status invalid")
    confidence = summary.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
        errors.append("summary.confidence must be 0-1")
    assumption_ratio = summary.get("assumption_ratio")
    if not isinstance(assumption_ratio, (int, float)) or not 0 <= float(assumption_ratio) <= 1:
        errors.append("summary.assumption_ratio must be 0-1")
    return [str(gate) for gate in scope]


def validate_gate_order(gates: dict[str, Any], scope: list[str], report: dict[str, Any], errors: list[str]) -> None:
    gate_order = gates["gate_order"]
    unknown = set(scope) - set(gate_order)
    for gate in sorted(unknown):
        errors.append(f"unknown gate in scope: {gate}")
    for gate in scope:
        gate_def = next((item for item in gates["gates"] if item["id"] == gate), None)
        if not gate_def:
            continue
        passed = set(report.get("previous_gates_passed", []))
        missing = set(gate_def["required_previous_gates"]) - passed
        if missing:
            summary = report.get("summary", {})
            if summary.get("overall_status") != "blocked":
                errors.append(f"{gate} missing previous gates must block")


def validate_gates(report: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any], scope: list[str], errors: list[str]) -> int:
    rows = report.get("gate_results")
    if not isinstance(rows, list):
        errors.append("gate_results must be a list")
        return 0
    seen: set[str] = set()
    blocking = 0
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"gate_results[{index}] must be an object")
            continue
        for field in contract["gate_fields"]:
            if field not in row:
                errors.append(f"gate_results[{index}] missing {field}")
        gate = row.get("gate")
        if gate in seen:
            errors.append(f"duplicate gate result: {gate}")
        seen.add(str(gate))
        if gate not in scope:
            errors.append(f"gate_results[{index}].gate not in scope: {gate}")
        if row.get("status") not in contract["gate_statuses"]:
            errors.append(f"gate_results[{index}].status invalid")
        if row.get("blocking") is True:
            blocking += 1
        if not contains_tag(row.get("evidence"), evidence["allowed_evidence_tags"]):
            errors.append(f"gate_results[{index}].evidence missing evidence tag")
    for gate in sorted(set(scope) - seen):
        errors.append(f"missing gate result: {gate}")
    return blocking


def validate_criteria(
    report: dict[str, Any],
    gates: dict[str, Any],
    contract: dict[str, Any],
    evidence: dict[str, Any],
    scope: list[str],
    errors: list[str],
) -> tuple[int, int, int]:
    rows = report.get("criteria_results")
    if not isinstance(rows, list):
        errors.append("criteria_results must be a list")
        return 0, 0, 0
    expected = scoped_criteria(gates, scope)
    seen: set[str] = set()
    blocking = 0
    not_verified = 0
    assumption_rows = 0
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"criteria_results[{index}] must be an object")
            continue
        for field in contract["criterion_fields"]:
            if field not in row:
                errors.append(f"criteria_results[{index}] missing {field}")
        cid = row.get("criterion_id")
        if cid not in expected:
            errors.append(f"criteria_results[{index}].criterion_id not in scope: {cid}")
        else:
            seen.add(str(cid))
            item = expected[str(cid)]
            if row.get("gate") != item["gate"]:
                errors.append(f"criteria_results[{index}].gate mismatch")
            if row.get("criterion_name") != item["name"]:
                errors.append(f"criteria_results[{index}].criterion_name mismatch")
            if row.get("required") != item["required"]:
                errors.append(f"criteria_results[{index}].required mismatch")
        status = row.get("status")
        severity = row.get("severity")
        if status not in contract["criterion_statuses"]:
            errors.append(f"criteria_results[{index}].status invalid")
        if severity not in contract["severities"]:
            errors.append(f"criteria_results[{index}].severity invalid")
        if not contains_tag(row.get("evidence"), evidence["allowed_evidence_tags"]):
            errors.append(f"criteria_results[{index}].evidence missing evidence tag")
        if contains_tag(row.get("evidence"), evidence["assumption_tags"]):
            assumption_rows += 1
        required = row.get("required") is True
        if status == "fail":
            if severity in {"P0", "P1"} or required:
                blocking += 1
            if blank(row.get("remediation")):
                errors.append(f"criteria_results[{index}] fail requires remediation")
            if severity == "none":
                errors.append(f"criteria_results[{index}] fail cannot use severity none")
        elif status == "not_verified":
            not_verified += 1
            if required:
                blocking += 1
            if blank(row.get("missing_evidence")):
                errors.append(f"criteria_results[{index}] not_verified requires missing_evidence")
            if blank(row.get("remediation")):
                errors.append(f"criteria_results[{index}] not_verified requires remediation")
        elif status == "pass":
            if severity != "none":
                errors.append(f"criteria_results[{index}] pass must use severity none")
        elif status == "not_applicable" and required:
            errors.append(f"criteria_results[{index}] required criterion cannot be not_applicable")
    for cid in sorted(set(expected) - seen):
        errors.append(f"missing criterion row: {cid}")
    if len(rows) != len(expected):
        errors.append(f"criteria_results must contain exactly {len(expected)} scoped rows")
    return blocking, not_verified, assumption_rows


def validate_score_history(report: dict[str, Any], score_schema: dict[str, Any], errors: list[str]) -> None:
    entry = report.get("score_history_entry")
    if not isinstance(entry, dict):
        errors.append("score_history_entry must be an object")
        return
    for field in score_schema["required_fields"]:
        if field not in entry:
            errors.append(f"score_history_entry missing {field}")
    if entry.get("decision") not in {"allow", "block", "needs_evidence"}:
        errors.append("score_history_entry.decision invalid")
    if not isinstance(entry.get("commands"), list):
        errors.append("score_history_entry.commands must be a list")


def validate_decision(
    report: dict[str, Any],
    contract: dict[str, Any],
    evidence_policy: dict[str, Any],
    blocking_findings: int,
    not_verified_count: int,
    gate_blocks: int,
    assumption_rows: int,
    criteria_count: int,
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
    if decision.get("release_decision") not in contract["release_decisions"]:
        errors.append("decision.release_decision invalid")
    if summary.get("blocking_findings") != blocking_findings:
        errors.append(f"summary.blocking_findings must be {blocking_findings}")
    if summary.get("not_verified_count") != not_verified_count:
        errors.append(f"summary.not_verified_count must be {not_verified_count}")
    expected_ratio = round(assumption_rows / criteria_count, 4) if criteria_count else 0
    if round(float(summary.get("assumption_ratio", 0)), 4) != expected_ratio:
        errors.append(f"summary.assumption_ratio must be {expected_ratio}")
    warning = report.get("warning_banner", "")
    if expected_ratio > float(evidence_policy["warning_threshold"]) and blank(warning):
        errors.append("warning_banner required when assumption ratio exceeds threshold")
    overall = summary.get("overall_status")
    if (blocking_findings or gate_blocks or not_verified_count) and overall != "blocked":
        errors.append("overall_status must be blocked when findings, gate blocks, or missing evidence exist")
    if overall == "pass" and decision.get("release_decision") != "allow":
        errors.append("pass report requires decision.release_decision=allow")
    if overall == "blocked" and decision.get("release_decision") != "block":
        errors.append("blocked report requires decision.release_decision=block")


def validate_report(gates: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any], score_schema: dict[str, Any], report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validate_sections(report, contract, evidence, errors)
    scope = validate_summary(report, contract, errors)
    validate_gate_order(gates, scope, report, errors)
    gate_blocks = validate_gates(report, contract, evidence, scope, errors)
    blocking, not_verified, assumption_rows = validate_criteria(report, gates, contract, evidence, scope, errors)
    validate_score_history(report, score_schema, errors)
    criteria_count = len(report.get("criteria_results", [])) if isinstance(report.get("criteria_results"), list) else 0
    validate_decision(report, contract, evidence, blocking, not_verified, gate_blocks, assumption_rows, criteria_count, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate quality gatekeeper report")
    parser.add_argument("--gates", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--score-schema", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()
    try:
        errors = validate_report(
            gates=load_json(args.gates),
            contract=load_json(args.contract),
            evidence=load_json(args.evidence),
            score_schema=load_json(args.score_schema),
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
