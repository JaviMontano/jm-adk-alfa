#!/usr/bin/env python3
"""Validate deterministic certify-skill report fixtures."""

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


def has_tag(value: Any, tags: list[str]) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return any(tag in text for tag in tags)


def phase_checks(phases: dict[str, Any], phase_id: str) -> list[str]:
    for phase in phases["phases"]:
        if phase["id"] == phase_id:
            return list(phase["checks"])
    raise KeyError(phase_id)


def validate_sections(report: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any], errors: list[str]) -> None:
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"missing section: {section}")
        elif is_blank(report[section]) and section not in contract.get("allow_empty_sections", []):
            errors.append(f"empty section: {section}")
    serialized = json.dumps(report, ensure_ascii=False).lower()
    for phrase in contract["blocked_phrases"]:
        if phrase in serialized:
            errors.append(f"blocked phrase present: {phrase}")
    if not has_tag(report, evidence["allowed_evidence_tags"]):
        errors.append("missing evidence tag")


def validate_summary(report: dict[str, Any], contract: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> str:
    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        return ""
    for field in contract["summary_fields"]:
        if field not in summary:
            errors.append(f"summary missing {field}")
    level = str(summary.get("certification", ""))
    if level not in policy["levels"]:
        errors.append("summary.certification invalid")
    score = summary.get("overall_score")
    if not isinstance(score, (int, float)) or not 0 <= float(score) <= 10:
        errors.append("summary.overall_score must be 0-10")
    return level


def validate_check_rows(
    rows: Any,
    expected_ids: list[str],
    section: str,
    contract: dict[str, Any],
    evidence: dict[str, Any],
    errors: list[str],
) -> tuple[int, int, bool]:
    if not isinstance(rows, list):
        errors.append(f"{section} must be a list")
        return 0, 0, False
    seen: set[str] = set()
    pass_count = 0
    fail_count = 0
    s1_failed = False
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"{section}[{index}] must be an object")
            continue
        for field in contract["check_fields"]:
            if field not in row:
                errors.append(f"{section}[{index}] missing {field}")
        cid = str(row.get("id", ""))
        if cid in seen:
            errors.append(f"{section}[{index}] duplicate id: {cid}")
        seen.add(cid)
        if cid not in expected_ids:
            errors.append(f"{section}[{index}] unexpected id: {cid}")
        result = row.get("result")
        if result not in contract["allowed_results"]:
            errors.append(f"{section}[{index}].result invalid")
        if result == "PASS":
            pass_count += 1
        elif result == "FAIL":
            fail_count += 1
            if cid == "S1":
                s1_failed = True
        if result in {"PASS", "FAIL"} and not has_tag(row.get("evidence"), evidence["allowed_evidence_tags"]):
            errors.append(f"{section}[{index}].evidence missing evidence tag")
    missing = set(expected_ids) - seen
    for cid in sorted(missing):
        errors.append(f"{section} missing check: {cid}")
    if len(rows) != len(expected_ids):
        errors.append(f"{section} must contain exactly {len(expected_ids)} rows")
    return pass_count, fail_count, s1_failed


def validate_rubric(report: dict[str, Any], phases: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any], errors: list[str]) -> tuple[float, int, bool]:
    rows = report.get("rubric_scores")
    if not isinstance(rows, list):
        errors.append("rubric_scores must be a list")
        return 0.0, 0, False
    expected = list(phases["rubric_dimensions"])
    seen: set[str] = set()
    scores: list[float] = []
    has_below_six = False
    six_count = 0
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"rubric_scores[{index}] must be an object")
            continue
        for field in contract["rubric_fields"]:
            if field not in row:
                errors.append(f"rubric_scores[{index}] missing {field}")
        criterion = str(row.get("criterion", ""))
        if criterion in seen:
            errors.append(f"rubric_scores duplicate criterion: {criterion}")
        seen.add(criterion)
        if criterion not in expected:
            errors.append(f"rubric_scores unexpected criterion: {criterion}")
        score = row.get("score")
        if not isinstance(score, (int, float)) or not 1 <= float(score) <= 10:
            errors.append(f"rubric_scores[{index}].score must be 1-10")
            continue
        score_f = float(score)
        scores.append(score_f)
        if score_f < 6:
            has_below_six = True
        if score_f == 6:
            six_count += 1
        if not has_tag(row.get("evidence"), evidence["allowed_evidence_tags"]):
            errors.append(f"rubric_scores[{index}].evidence missing evidence tag")
    for criterion in sorted(set(expected) - seen):
        errors.append(f"rubric_scores missing criterion: {criterion}")
    if len(rows) != len(expected):
        errors.append(f"rubric_scores must contain exactly {len(expected)} rows")
    average = round(sum(scores) / len(scores), 2) if scores else 0.0
    return average, six_count, has_below_six


def validate_blockers(report: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    rows = report.get("blockers")
    if not isinstance(rows, list):
        errors.append("blockers must be a list")
        return
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"blockers[{index}] must be an object")
            continue
        for field in contract["blocker_fields"]:
            if field not in row or is_blank(row[field]):
                errors.append(f"blockers[{index}] missing {field}")


def expected_level(
    structural_failures: int,
    s1_failed: bool,
    rubric_average: float,
    six_count: int,
    has_below_six: bool,
    moat_failures: int,
) -> str:
    if s1_failed or structural_failures >= 3 or has_below_six:
        return "BLOCKED"
    certified = structural_failures == 0 and six_count == 0 and rubric_average >= 8.0
    if certified and moat_failures == 0:
        return "MOAT"
    if certified:
        return "CERTIFIED"
    conditional_structural = 1 <= structural_failures <= 2 and rubric_average >= 8.0 and not has_below_six
    conditional_rubric = 1 <= six_count <= 2 and rubric_average >= 8.0 and structural_failures == 0
    if conditional_structural or conditional_rubric:
        return "CONDITIONAL"
    return "BLOCKED"


def validate_report(phases: dict[str, Any], policy: dict[str, Any], contract: dict[str, Any], evidence: dict[str, Any], report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validate_sections(report, contract, evidence, errors)
    observed_level = validate_summary(report, contract, policy, errors)
    structural_pass, structural_failures, s1_failed = validate_check_rows(
        report.get("structural_checks"),
        phase_checks(phases, "structural"),
        "structural_checks",
        contract,
        evidence,
        errors,
    )
    content_pass, _content_failures, _ = validate_check_rows(
        report.get("content_checks"),
        phase_checks(phases, "content"),
        "content_checks",
        contract,
        evidence,
        errors,
    )
    validate_check_rows(
        report.get("systemic_checks"),
        phase_checks(phases, "systemic"),
        "systemic_checks",
        contract,
        evidence,
        errors,
    )
    _moat_pass, moat_failures, _ = validate_check_rows(
        report.get("moat_checks"),
        phase_checks(phases, "moat"),
        "moat_checks",
        contract,
        evidence,
        errors,
    )
    rubric_average, six_count, has_below_six = validate_rubric(report, phases, contract, evidence, errors)
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    if round(float(summary.get("overall_score", 0)), 2) != rubric_average:
        errors.append(f"summary.overall_score must be {rubric_average}")
    if summary.get("structural_pass") != structural_pass:
        errors.append(f"summary.structural_pass must be {structural_pass}")
    if summary.get("structural_total") != len(phase_checks(phases, "structural")):
        errors.append("summary.structural_total mismatch")
    if summary.get("content_pass") != content_pass:
        errors.append(f"summary.content_pass must be {content_pass}")
    if summary.get("content_total") != len(phase_checks(phases, "content")):
        errors.append("summary.content_total mismatch")
    computed = expected_level(structural_failures, s1_failed, rubric_average, six_count, has_below_six, moat_failures)
    if observed_level and observed_level != computed:
        errors.append(f"summary.certification must be {computed}")
    validate_blockers(report, contract, errors)
    if computed in {"CONDITIONAL", "BLOCKED"} and not report.get("blockers"):
        errors.append("blockers required for CONDITIONAL or BLOCKED")
    if computed in {"MOAT", "CERTIFIED"} and report.get("blockers"):
        errors.append("blockers must be empty for MOAT or CERTIFIED")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate certify-skill certification report")
    parser.add_argument("--phases", required=True, type=Path)
    parser.add_argument("--level-policy", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()
    try:
        errors = validate_report(
            phases=load_json(args.phases),
            policy=load_json(args.level_policy),
            contract=load_json(args.contract),
            evidence=load_json(args.evidence),
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
