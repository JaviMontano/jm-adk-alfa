#!/usr/bin/env python3
"""Validate deterministic audit-content-quality JSON reports."""

from __future__ import annotations

import argparse
import json
import sys
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


def grade_for_percentage(percentage: float, thresholds: list[dict[str, Any]]) -> str:
    for item in thresholds:
        if float(item["min_percentage"]) <= percentage <= float(item["max_percentage"]):
            return str(item["grade"])
    raise ValueError(f"no grade threshold for percentage {percentage}")


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


def validate_required_fields(item: dict[str, Any], fields: list[str], label: str) -> list[str]:
    errors: list[str] = []
    for field in fields:
        if field not in item:
            errors.append(f"{label}: missing field {field}")
        elif isinstance(item[field], str) and not item[field].strip():
            errors.append(f"{label}.{field}: must not be empty")
        elif isinstance(item[field], list) and field != "skipped_skills" and not item[field]:
            errors.append(f"{label}.{field}: must not be empty")
    return errors


def close_enough(actual: Any, expected: float, label: str, errors: list[str], tolerance: float = 0.01) -> None:
    if not isinstance(actual, (int, float)):
        errors.append(f"{label}: must be numeric")
        return
    if abs(float(actual) - expected) > tolerance:
        errors.append(f"{label}: expected {expected:.2f}, got {actual}")


def validate_report(
    report: dict[str, Any],
    contract: dict[str, Any],
    rubric: dict[str, Any],
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

    dimensions = list(rubric["dimensions"])
    score_min = int(rubric["score_min"])
    score_max = int(rubric["score_max"])
    total_max = int(rubric["total_max"])
    thresholds = list(rubric["grade_thresholds"])
    bottom_count = int(rubric["bottom_count"])
    priority_policy = require_object(rubric["priority_policy"], "priority_policy")
    gap_threshold = float(rubric["systematic_gap_threshold"])

    summary = require_object(report["summary"], "summary")
    errors.extend(validate_required_fields(summary, contract["summary_fields"], "summary"))

    scorecards_raw = require_list(report["scorecards"], "scorecards")
    scorecards = [require_object(item, f"scorecards[{index}]") for index, item in enumerate(scorecards_raw)]
    if not scorecards:
        errors.append("scorecards: must contain at least one skill")

    totals: list[float] = []
    percentages: list[float] = []
    dimension_totals = {dimension: 0.0 for dimension in dimensions}
    for index, item in enumerate(scorecards):
        label = f"scorecards[{index}]"
        errors.extend(validate_required_fields(item, contract["scorecard_fields"], label))
        scores = require_object(item.get("scores"), f"{label}.scores")
        rationales = require_object(item.get("rationales"), f"{label}.rationales")
        missing_scores = [dimension for dimension in dimensions if dimension not in scores]
        missing_rationales = [dimension for dimension in dimensions if dimension not in rationales]
        if missing_scores:
            errors.append(f"{label}.scores: missing dimensions {missing_scores}")
        if missing_rationales:
            errors.append(f"{label}.rationales: missing dimensions {missing_rationales}")

        total = 0.0
        for dimension in dimensions:
            score = scores.get(dimension)
            if not isinstance(score, (int, float)):
                errors.append(f"{label}.scores.{dimension}: must be numeric")
                continue
            if not score_min <= float(score) <= score_max:
                errors.append(f"{label}.scores.{dimension}: expected {score_min}-{score_max}")
            rationale = str(rationales.get(dimension, ""))
            if len(rationale.strip()) < 12:
                errors.append(f"{label}.rationales.{dimension}: rationale too short")
            total += float(score)
            dimension_totals[dimension] += float(score)

        percentage = (total / total_max) * 100 if total_max else 0.0
        expected_grade = grade_for_percentage(percentage, thresholds)
        close_enough(item.get("total_score"), total, f"{label}.total_score", errors)
        close_enough(item.get("percentage"), percentage, f"{label}.percentage", errors)
        if item.get("grade") != expected_grade:
            errors.append(f"{label}.grade: expected {expected_grade}, got {item.get('grade')}")
        lowest_dimension = min(dimensions, key=lambda dimension: float(scores.get(dimension, score_max)))
        if item.get("lowest_dimension") != lowest_dimension:
            errors.append(f"{label}.lowest_dimension: expected {lowest_dimension}, got {item.get('lowest_dimension')}")
        if total < 48 and len(str(item.get("recommendation", "")).strip()) < 20:
            errors.append(f"{label}.recommendation: weak skills require specific recommendation")
        totals.append(total)
        percentages.append(percentage)

    total_skills = len(scorecards)
    average_score = sum(totals) / total_skills if total_skills else 0.0
    average_percentage = sum(percentages) / total_skills if total_skills else 0.0
    close_enough(summary.get("average_score"), average_score, "summary.average_score", errors)
    close_enough(summary.get("average_percentage"), average_percentage, "summary.average_percentage", errors)
    if summary.get("total_skills") != total_skills:
        errors.append(f"summary.total_skills: expected {total_skills}, got {summary.get('total_skills')}")
    expected_summary_grade = grade_for_percentage(average_percentage, thresholds)
    if summary.get("grade") != expected_summary_grade:
        errors.append(f"summary.grade: expected {expected_summary_grade}, got {summary.get('grade')}")

    coverage = require_object(report["coverage"], "coverage")
    errors.extend(validate_required_fields(coverage, contract["coverage_fields"], "coverage"))
    if coverage.get("scored_skills") != total_skills:
        errors.append(f"coverage.scored_skills: expected {total_skills}, got {coverage.get('scored_skills')}")
    if not isinstance(coverage.get("discovered_skills"), int) or coverage.get("discovered_skills") < total_skills:
        errors.append("coverage.discovered_skills: must be >= scored skills")

    sorted_cards = sorted(scorecards, key=lambda item: (float(item["total_score"]), str(item["skill"])))
    expected_bottom = sorted_cards[: min(bottom_count, total_skills)]
    bottom_raw = require_list(report["bottom_skills"], "bottom_skills")
    bottom = [require_object(item, f"bottom_skills[{index}]") for index, item in enumerate(bottom_raw)]
    if len(bottom) != len(expected_bottom):
        errors.append(f"bottom_skills: expected {len(expected_bottom)} entries, got {len(bottom)}")
    for index, expected in enumerate(expected_bottom):
        if index >= len(bottom):
            break
        actual = bottom[index]
        errors.extend(validate_required_fields(actual, contract["bottom_skill_fields"], f"bottom_skills[{index}]"))
        for field in ["skill", "total_score", "grade"]:
            if actual.get(field) != expected.get(field):
                errors.append(f"bottom_skills[{index}].{field}: expected {expected.get(field)}, got {actual.get(field)}")
        expected_priority = priority_policy[str(expected["grade"])]
        if actual.get("priority") != expected_priority:
            errors.append(f"bottom_skills[{index}].priority: expected {expected_priority}, got {actual.get('priority')}")

    expected_gaps = []
    for dimension in dimensions:
        average = dimension_totals[dimension] / total_skills if total_skills else 0.0
        if average < gap_threshold:
            expected_gaps.append((dimension, average))
    systematic_raw = require_list(report["systematic_gaps"], "systematic_gaps")
    systematic = [require_object(item, f"systematic_gaps[{index}]") for index, item in enumerate(systematic_raw)]
    if summary.get("systematic_gap_count") != len(expected_gaps):
        errors.append(f"summary.systematic_gap_count: expected {len(expected_gaps)}, got {summary.get('systematic_gap_count')}")
    actual_gap_map = {str(item.get("dimension")): item for item in systematic}
    for dimension, average in expected_gaps:
        if dimension not in actual_gap_map:
            errors.append(f"systematic_gaps: missing dimension {dimension}")
            continue
        item = actual_gap_map[dimension]
        errors.extend(validate_required_fields(item, contract["systematic_gap_fields"], f"systematic_gaps.{dimension}"))
        close_enough(item.get("average_score"), average, f"systematic_gaps.{dimension}.average_score", errors)
    for dimension in actual_gap_map:
        if dimension not in {gap[0] for gap in expected_gaps}:
            errors.append(f"systematic_gaps: unexpected dimension {dimension}")

    allowed_tags = list(evidence_policy["allowed_tags"])
    forbidden_tags = list(evidence_policy["forbidden_tags"])
    text = json.dumps(report, ensure_ascii=False)
    if not any(tag in text for tag in allowed_tags):
        errors.append("report: at least one allowed evidence tag must appear")
    for tag in forbidden_tags:
        if tag in text:
            errors.append(f"report: forbidden evidence tag appears: {tag}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate audit-content-quality report fixtures")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--rubric", required=True, type=Path)
    parser.add_argument("--evidence-policy", required=True, type=Path)
    args = parser.parse_args()

    try:
        report = require_object(load_json(args.report), "report")
        contract = require_object(load_json(args.contract), "contract")
        rubric = require_object(load_json(args.rubric), "rubric")
        evidence_policy = require_object(load_json(args.evidence_policy), "evidence_policy")
        errors = validate_report(report, contract, rubric, evidence_policy)
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
