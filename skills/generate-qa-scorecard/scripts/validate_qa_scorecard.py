#!/usr/bin/env python3
"""Validate deterministic QA scorecards."""

from __future__ import annotations

import argparse
import json
import math
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


def non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def grade_for(percent: float, thresholds: list[dict[str, Any]]) -> str:
    for item in thresholds:
        if item["min_percent"] <= percent <= item["max_percent"]:
            return str(item["grade"])
    return "F"


def expected_status(dimension: dict[str, Any]) -> str:
    if dimension.get("status") == "na" or dimension.get("evaluated") is False:
        return "na"
    critical = int(dimension.get("critical", 0))
    warning = int(dimension.get("warning", 0))
    if critical > 0:
        return "fail"
    if warning > 0:
        return "warn"
    return "pass"


def expected_actions(
    dimensions: list[dict[str, Any]],
    points: dict[str, int],
    max_actions: int,
) -> list[dict[str, Any]]:
    dimension_order = {str(item["id"]): int(item["order"]) for item in policy("dimensions-policy.json")["dimensions"]}
    candidates = []
    for dim in dimensions:
        status = dim.get("status")
        if status not in {"fail", "warn"}:
            continue
        score = int(dim.get("score", 0))
        improvement = points["pass"] - score
        candidates.append(
            {
                "dimension": dim["id"],
                "expected_improvement": improvement,
                "critical": int(dim.get("critical", 0)),
                "warning": int(dim.get("warning", 0)),
                "order": dimension_order[str(dim["id"])],
            }
        )
    status_rank = {"fail": 0, "warn": 1}
    candidates.sort(
        key=lambda item: (
            status_rank[next(dim["status"] for dim in dimensions if dim["id"] == item["dimension"])],
            -item["expected_improvement"],
            -item["critical"],
            -item["warning"],
            item["order"],
        )
    )
    return candidates[:max_actions]


def validate(scorecard: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(scorecard, dict):
        return ["scorecard must be a JSON object"]

    contract = policy("scorecard-contract.json")
    dimensions_policy = policy("dimensions-policy.json")
    scoring_policy = policy("scoring-policy.json")
    grade_policy = policy("grade-policy.json")
    action_policy = policy("action-priority-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in scorecard:
            errors.append(f"missing required field: {field}")

    if scorecard.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if scorecard.get("skill") != "generate-qa-scorecard":
        errors.append("skill must be generate-qa-scorecard")
    if not non_empty_string(scorecard.get("scorecard_id")):
        errors.append("scorecard_id must be a non-empty string")
    if not non_empty_string(scorecard.get("subject")):
        errors.append("subject must be a non-empty string")

    dimensions = scorecard.get("dimensions")
    if not isinstance(dimensions, list):
        return errors + ["dimensions must be a list"]

    canonical = dimensions_policy["dimensions"]
    canonical_ids = [item["id"] for item in canonical]
    actual_ids = [dim.get("id") for dim in dimensions if isinstance(dim, dict)]
    if actual_ids != canonical_ids:
        errors.append(f"dimensions must appear exactly in canonical order: {canonical_ids}")

    points = scoring_policy["points"]
    allowed_statuses = set(scoring_policy["allowed_statuses"])
    total = 0
    evaluated_count = 0
    na_ids: list[str] = []
    computed_actions_source: list[dict[str, Any]] = []

    for index, dim in enumerate(dimensions):
        if not isinstance(dim, dict):
            errors.append(f"dimensions[{index}] must be an object")
            continue
        dim_id = dim.get("id", f"dimensions[{index}]")
        status = dim.get("status")
        if status not in allowed_statuses:
            errors.append(f"dimension {dim_id} status must be one of {sorted(allowed_statuses)}")
        for field in ["critical", "warning", "info"]:
            if not non_negative_int(dim.get(field)):
                errors.append(f"dimension {dim_id} {field} must be a non-negative integer")
        if status == "na":
            if dim.get("evaluated") is not False:
                errors.append(f"dimension {dim_id} status na requires evaluated=false")
            if not non_empty_string(dim.get("reason")):
                errors.append(f"dimension {dim_id} status na requires reason")
            if dim.get("score") not in {None, 0}:
                errors.append(f"dimension {dim_id} status na must not contribute score")
            na_ids.append(str(dim_id))
            continue

        if dim.get("evaluated") is False:
            errors.append(f"dimension {dim_id} evaluated=false requires status na")
        if not non_empty_string(dim.get("evidence")):
            errors.append(f"dimension {dim_id} evidence must be non-empty")
        expected = expected_status(dim)
        if status != expected:
            errors.append(f"dimension {dim_id} status {status} does not match expected {expected}")
        expected_score = points.get(str(status))
        if dim.get("score") != expected_score:
            errors.append(f"dimension {dim_id} score must be {expected_score}")
        total += int(expected_score or 0)
        evaluated_count += 1
        computed_actions_source.append(dim)

    evaluated_max = evaluated_count * points["pass"]
    if scorecard.get("total_score") != total:
        errors.append(f"total_score must be {total}")
    if scorecard.get("evaluated_max") != evaluated_max:
        errors.append(f"evaluated_max must be {evaluated_max}")

    expected_percent = round((total / evaluated_max) * 100, 2) if evaluated_max else 0.0
    actual_percent = scorecard.get("percentage")
    if not isinstance(actual_percent, (int, float)) or not math.isclose(float(actual_percent), expected_percent, abs_tol=0.01):
        errors.append(f"percentage must be {expected_percent}")
    expected_grade = grade_for(expected_percent, grade_policy["thresholds"])
    if scorecard.get("grade") != expected_grade:
        errors.append(f"grade must be {expected_grade}")

    reduced_scope = scorecard.get("reduced_scope")
    if not isinstance(reduced_scope, dict):
        errors.append("reduced_scope must be an object")
    else:
        if na_ids:
            if reduced_scope.get("active") is not True:
                errors.append("na dimensions require reduced_scope.active=true")
            if reduced_scope.get("dimensions") != na_ids:
                errors.append(f"reduced_scope.dimensions must be {na_ids}")
            if not non_empty_string(reduced_scope.get("note")):
                errors.append("reduced_scope.note must be non-empty when active")
        elif reduced_scope.get("active") is not False:
            errors.append("full scorecards require reduced_scope.active=false")

    priority_actions = scorecard.get("priority_actions")
    if not isinstance(priority_actions, list):
        errors.append("priority_actions must be a list")
    else:
        expected = expected_actions(dimensions, points, action_policy["max_actions"])
        if len(priority_actions) > action_policy["max_actions"]:
            errors.append(f"priority_actions must contain at most {action_policy['max_actions']} items")
        expected_pairs = [(item["dimension"], item["expected_improvement"]) for item in expected]
        actual_pairs = [
            (item.get("dimension"), item.get("expected_improvement"))
            for item in priority_actions
            if isinstance(item, dict)
        ]
        if actual_pairs != expected_pairs:
            errors.append(f"priority_actions order must be {expected_pairs}")
        for index, action in enumerate(priority_actions):
            if not isinstance(action, dict):
                errors.append(f"priority_actions[{index}] must be an object")
                continue
            if not non_empty_string(action.get("action")):
                errors.append(f"priority_actions[{index}].action must be non-empty")

    guardian = scorecard.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        allowed = set(contract["json_contract"]["guardian_decisions"])
        if guardian.get("decision") not in allowed:
            errors.append(f"guardian.decision must be one of {sorted(allowed)}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a QA scorecard JSON report")
    parser.add_argument("scorecard", type=Path, help="Path to a JSON scorecard")
    args = parser.parse_args()

    try:
        scorecard = load_json(args.scorecard)
        errors = validate(scorecard)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.scorecard}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
