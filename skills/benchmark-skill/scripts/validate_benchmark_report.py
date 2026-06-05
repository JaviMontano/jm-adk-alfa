#!/usr/bin/env python3
"""Validate deterministic benchmark-skill report fixtures."""

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


def average(values: list[float]) -> float:
    return round(sum(values) / len(values), 2)


def validate_inventory(report: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    inventory = report.get("inventory")
    if not isinstance(inventory, list) or len(inventory) < 1:
        errors.append("inventory must contain at least one row")
        return
    for index, row in enumerate(inventory, start=1):
        if not isinstance(row, dict):
            errors.append(f"inventory[{index}] must be an object")
            continue
        for field in contract["inventory_fields"]:
            if field not in row:
                errors.append(f"inventory[{index}] missing {field}")
            elif not isinstance(row[field], int):
                errors.append(f"inventory[{index}].{field} must be integer")


def validate_scores(report: dict[str, Any], rubric: dict[str, Any], errors: list[str]) -> tuple[list[float], list[float]]:
    dimensions = {item["key"] for item in rubric["dimensions"]}
    score_rows = report.get("dimension_scores")
    score_min = rubric["score_bounds"]["min"]
    score_max = rubric["score_bounds"]["max"]
    scores_a: list[float] = []
    scores_b: list[float] = []

    if not isinstance(score_rows, list):
        errors.append("dimension_scores must be a list")
        return scores_a, scores_b
    seen: set[str] = set()
    for index, row in enumerate(score_rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"dimension_scores[{index}] must be an object")
            continue
        for field in rubric["score_entry_fields"]:
            if field not in row:
                errors.append(f"dimension_scores[{index}] missing {field}")
        dimension = row.get("dimension")
        if dimension not in dimensions:
            errors.append(f"dimension_scores[{index}].dimension unknown: {dimension}")
        else:
            seen.add(str(dimension))
        for field in ["state_a", "state_b"]:
            value = row.get(field)
            if not isinstance(value, (int, float)) or not score_min <= float(value) <= score_max:
                errors.append(f"dimension_scores[{index}].{field} must be {score_min}-{score_max}")
        if isinstance(row.get("state_a"), (int, float)) and isinstance(row.get("state_b"), (int, float)):
            expected_delta = round(float(row["state_b"]) - float(row["state_a"]), 2)
            if round(float(row.get("delta", 999)), 2) != expected_delta:
                errors.append(f"dimension_scores[{index}].delta must be {expected_delta}")
            scores_a.append(float(row["state_a"]))
            scores_b.append(float(row["state_b"]))
        if row.get("direction") not in rubric["directions"]:
            errors.append(f"dimension_scores[{index}].direction invalid")
        if is_blank(row.get("evidence")):
            errors.append(f"dimension_scores[{index}].evidence required")

    missing = dimensions - seen
    for dimension in sorted(missing):
        errors.append(f"missing dimension score: {dimension}")
    return scores_a, scores_b


def validate_gates(report: dict[str, Any], gate_policy: dict[str, Any], errors: list[str]) -> None:
    gates = {item["key"] for item in gate_policy["gates"]}
    rows = report.get("gate_changes")
    if not isinstance(rows, list):
        errors.append("gate_changes must be a list")
        return
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"gate_changes[{index}] must be an object")
            continue
        for field in gate_policy["gate_entry_fields"]:
            if field not in row:
                errors.append(f"gate_changes[{index}] missing {field}")
        gate = row.get("gate")
        if gate not in gates:
            errors.append(f"gate_changes[{index}].gate unknown: {gate}")
        else:
            seen.add(str(gate))
        for field in ["state_a", "state_b"]:
            if row.get(field) not in gate_policy["outcomes"]:
                errors.append(f"gate_changes[{index}].{field} invalid")
        if row.get("change") not in gate_policy["changes"]:
            errors.append(f"gate_changes[{index}].change invalid")
        if is_blank(row.get("evidence")):
            errors.append(f"gate_changes[{index}].evidence required")

    missing = gates - seen
    for gate in sorted(missing):
        errors.append(f"missing gate row: {gate}")


def count_improved_and_regressed(score_rows: list[dict[str, Any]]) -> tuple[int, int, int]:
    improved = sum(1 for row in score_rows if float(row.get("delta", 0)) > 0)
    regressed = sum(1 for row in score_rows if float(row.get("delta", 0)) < 0)
    large_regressions = sum(1 for row in score_rows if float(row.get("delta", 0)) <= -2)
    return improved, regressed, large_regressions


def validate_summary(report: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        return
    for field in policy["required_summary_fields"]:
        if field not in summary:
            errors.append(f"summary missing {field}")

    rows = report.get("dimension_scores") if isinstance(report.get("dimension_scores"), list) else []
    numeric_rows = [row for row in rows if isinstance(row, dict) and isinstance(row.get("state_a"), (int, float)) and isinstance(row.get("state_b"), (int, float))]
    if numeric_rows:
        scores_a = [float(row["state_a"]) for row in numeric_rows]
        scores_b = [float(row["state_b"]) for row in numeric_rows]
        avg_a = average(scores_a)
        avg_b = average(scores_b)
        avg_delta = round(avg_b - avg_a, 2)
        if round(float(summary.get("average_a", 999)), 2) != avg_a:
            errors.append(f"summary.average_a must be {avg_a}")
        if round(float(summary.get("average_b", 999)), 2) != avg_b:
            errors.append(f"summary.average_b must be {avg_b}")
        if round(float(summary.get("average_delta", 999)), 2) != avg_delta:
            errors.append(f"summary.average_delta must be {avg_delta}")
        improved, regressed, large_regressions = count_improved_and_regressed(numeric_rows)
        if summary.get("dimensions_improved") != improved:
            errors.append(f"summary.dimensions_improved must be {improved}")
        if summary.get("dimensions_regressed") != regressed:
            errors.append(f"summary.dimensions_regressed must be {regressed}")
    else:
        large_regressions = 0

    gate_rows = report.get("gate_changes") if isinstance(report.get("gate_changes"), list) else []
    gate_regressions = sum(
        1 for row in gate_rows if isinstance(row, dict) and row.get("change") == "Regressed"
    )
    if summary.get("gate_regressions") != gate_regressions:
        errors.append(f"summary.gate_regressions must be {gate_regressions}")

    label = summary.get("net_assessment")
    mode = summary.get("mode")
    transformed = bool(summary.get("transformed"))
    avg_delta = float(summary.get("average_delta", 0) or 0)
    improved = int(summary.get("dimensions_improved", 0) or 0)

    if label not in policy["labels"]:
        errors.append(f"summary.net_assessment invalid: {label}")
    if mode == "against-standard" and label != "GAP-TO-STANDARD":
        errors.append("against-standard mode must use GAP-TO-STANDARD")
    if label == "GAP-TO-STANDARD" and gate_regressions:
        errors.append("GAP-TO-STANDARD cannot include gate regressions")
    if label == "TRANSFORMED" and not transformed:
        errors.append("TRANSFORMED requires transformed=true")
    if label == "IMPROVED":
        if avg_delta < 0.5:
            errors.append("IMPROVED requires average_delta >= 0.5")
        if gate_regressions != 0:
            errors.append("IMPROVED requires zero gate regressions")
        if large_regressions != 0:
            errors.append("IMPROVED requires zero rubric regressions of 2+ points")
        if improved < 2:
            errors.append("IMPROVED requires at least two improved dimensions")
    if label == "REGRESSED" and not (avg_delta <= -0.5 or gate_regressions >= 1 or large_regressions >= 2):
        errors.append("REGRESSED requires average drop, gate regression, or large rubric regressions")
    if label == "IDENTICAL" and (avg_delta != 0 or gate_regressions != 0):
        errors.append("IDENTICAL requires zero average delta and zero gate regressions")


def validate_collections(report: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"missing section: {section}")
        elif is_blank(report[section]):
            errors.append(f"empty section: {section}")

    serialized = json.dumps(report, ensure_ascii=False).lower()
    for phrase in contract["blocked_phrases"]:
        if phrase.lower() in serialized:
            errors.append(f"blocked phrase present: {phrase}")
    if not any(tag in serialized for tag in [tag.lower() for tag in contract["required_evidence_tags"]]):
        errors.append("missing evidence tag")


def validate_report(
    rubric: dict[str, Any],
    gates: dict[str, Any],
    policy: dict[str, Any],
    contract: dict[str, Any],
    report: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    validate_collections(report, contract, errors)
    validate_inventory(report, contract, errors)
    validate_scores(report, rubric, errors)
    validate_gates(report, gates, errors)
    validate_summary(report, policy, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate benchmark report JSON")
    parser.add_argument("--rubric", required=True, type=Path)
    parser.add_argument("--gates", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        errors = validate_report(
            rubric=load_json(args.rubric),
            gates=load_json(args.gates),
            policy=load_json(args.policy),
            contract=load_json(args.contract),
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
