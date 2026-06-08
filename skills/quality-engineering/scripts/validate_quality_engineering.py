#!/usr/bin/env python3
"""Validate deterministic quality engineering reports."""

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


def non_empty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(non_empty_string(item) for item in value)


def level_for_score(score: float, levels: list[dict[str, Any]]) -> int | None:
    for item in levels:
        if item["min_score"] <= score <= item["max_score"]:
            return int(item["level"])
    return None


def min_score_for_level(level: int, levels: list[dict[str, Any]]) -> int:
    for item in levels:
        if int(item["level"]) == level:
            return int(item["min_score"])
    raise ValueError(f"unknown maturity level: {level}")


def expected_priority_actions(
    dimensions: list[dict[str, Any]],
    target_level: int,
    levels: list[dict[str, Any]],
    canonical_order: dict[str, int],
    max_actions: int,
) -> list[dict[str, Any]]:
    target_min = min_score_for_level(target_level, levels)
    candidates: list[dict[str, Any]] = []
    for dim in dimensions:
        score = int(dim.get("score", 0))
        gap = max(0, target_min - score)
        if gap == 0:
            continue
        candidates.append(
            {
                "dimension": dim["id"],
                "expected_improvement": gap,
                "score": score,
                "order": canonical_order[str(dim["id"])],
            }
        )
    candidates.sort(key=lambda item: (-item["expected_improvement"], item["score"], item["order"]))
    return candidates[:max_actions]


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("quality-framework-contract.json")
    maturity = policy("maturity-model.json")
    strategy_policy = policy("test-strategy-policy.json")
    gate_policy = policy("gate-policy.json")
    metrics_policy = policy("metrics-policy.json")
    action_policy = policy("action-priority-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")

    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "quality-engineering":
        errors.append("skill must be quality-engineering")
    for field in ["plan_id", "subject"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if not isinstance(report.get("evidence_summary"), list) or not report.get("evidence_summary"):
        errors.append("evidence_summary must be a non-empty list")
    if not isinstance(report.get("assumptions"), list):
        errors.append("assumptions must be a list")

    architecture_type = report.get("architecture_type")
    architecture_map = strategy_policy["architecture_types"]
    if architecture_type not in architecture_map:
        errors.append(f"architecture_type must be one of {sorted(architecture_map)}")

    dimensions = report.get("maturity_assessment")
    levels = maturity["levels"]
    canonical = maturity["dimensions"]
    canonical_ids = [item["id"] for item in canonical]
    canonical_order = {item["id"]: int(item["order"]) for item in canonical}
    dimension_scores: list[int] = []

    if not isinstance(dimensions, list):
        errors.append("maturity_assessment must be a list")
        dimensions = []
    actual_ids = [dim.get("id") for dim in dimensions if isinstance(dim, dict)]
    if actual_ids != canonical_ids:
        errors.append(f"maturity_assessment must appear exactly in canonical order: {canonical_ids}")

    for index, dim in enumerate(dimensions):
        if not isinstance(dim, dict):
            errors.append(f"maturity_assessment[{index}] must be an object")
            continue
        dim_id = dim.get("id", f"maturity_assessment[{index}]")
        score = dim.get("score")
        if not isinstance(score, int) or score < 0 or score > 100:
            errors.append(f"dimension {dim_id} score must be an integer from 0 to 100")
            continue
        expected_level = level_for_score(score, levels)
        if dim.get("level") != expected_level:
            errors.append(f"dimension {dim_id} level must be {expected_level}")
        if not non_empty_string(dim.get("evidence")):
            errors.append(f"dimension {dim_id} evidence must be non-empty")
        dimension_scores.append(score)

    if dimension_scores:
        expected_overall = round(sum(dimension_scores) / len(canonical_ids), 2)
        actual_overall = report.get("overall_score")
        if not isinstance(actual_overall, (int, float)) or not math.isclose(float(actual_overall), expected_overall, abs_tol=0.01):
            errors.append(f"overall_score must be {expected_overall}")
        expected_overall_level = level_for_score(expected_overall, levels)
        if report.get("overall_level") != expected_overall_level:
            errors.append(f"overall_level must be {expected_overall_level}")
        target_level = report.get("target_level")
        if not isinstance(target_level, int) or target_level < int(expected_overall_level or 1) or target_level > 5:
            errors.append("target_level must be an integer from overall_level through 5")

    strategy = report.get("test_strategy")
    if not isinstance(strategy, dict):
        errors.append("test_strategy must be an object")
    elif architecture_type in architecture_map:
        expected = architecture_map[architecture_type]
        if strategy.get("shape") != expected["shape"]:
            errors.append(f"test_strategy.shape must be {expected['shape']}")
        distribution = strategy.get("distribution")
        if distribution != expected["distribution"]:
            errors.append(f"test_strategy.distribution must be {expected['distribution']}")
        if isinstance(distribution, dict) and sum(distribution.values()) != 100:
            errors.append("test_strategy.distribution must sum to 100")
        if not non_empty_string(strategy.get("rationale")):
            errors.append("test_strategy.rationale must be non-empty")
        data_strategy = strategy.get("test_data_strategy")
        if not isinstance(data_strategy, dict):
            errors.append("test_strategy.test_data_strategy must be an object")
        else:
            for field in ["synthetic_data", "masking_policy", "reset_policy"]:
                if not non_empty_string(data_strategy.get(field)):
                    errors.append(f"test_strategy.test_data_strategy.{field} must be non-empty")

    gates = report.get("quality_gates")
    expected_gates = gate_policy["gates"]
    if not isinstance(gates, list):
        errors.append("quality_gates must be a list")
        gates = []
    actual_gate_ids = [gate.get("id") for gate in gates if isinstance(gate, dict)]
    expected_gate_ids = [gate["id"] for gate in expected_gates]
    if actual_gate_ids != expected_gate_ids:
        errors.append(f"quality_gates must appear exactly in canonical order: {expected_gate_ids}")
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"quality_gates[{index}] must be an object")
            continue
        if index >= len(expected_gates):
            continue
        expected_gate = expected_gates[index]
        gate_id = expected_gate["id"]
        if gate.get("mode") != expected_gate["mode"]:
            errors.append(f"gate {gate_id} mode must be {expected_gate['mode']}")
        expected_blocking = expected_gate["mode"] == "blocking"
        if gate.get("blocking") is not expected_blocking:
            errors.append(f"gate {gate_id} blocking must be {expected_blocking}")
        timeout = gate.get("timeout_minutes")
        if not isinstance(timeout, int) or timeout <= 0 or timeout > int(expected_gate["timeout_minutes"]):
            errors.append(f"gate {gate_id} timeout_minutes must be <= {expected_gate['timeout_minutes']}")
        criteria = gate.get("criteria")
        if not non_empty_string_list(criteria):
            errors.append(f"gate {gate_id} criteria must be a non-empty string list")
            criteria = []
        for required in expected_gate["required_criteria"]:
            if required not in criteria:
                errors.append(f"gate {gate_id} missing required criterion {required}")
        bypassable = gate.get("bypassable_criteria", [])
        if not isinstance(bypassable, list):
            errors.append(f"gate {gate_id} bypassable_criteria must be a list")
            bypassable = []
        for security in gate_policy["security_criteria"]:
            if security in bypassable:
                errors.append(f"gate {gate_id} must not bypass security criterion {security}")
        if not non_empty_string(gate.get("on_failure")):
            errors.append(f"gate {gate_id} on_failure must be non-empty")

    metrics = report.get("metrics")
    if not isinstance(metrics, dict):
        errors.append("metrics must be an object")
    else:
        for metric_type in ["leading", "lagging"]:
            actual = metrics.get(metric_type)
            expected = metrics_policy[metric_type]
            if not isinstance(actual, list):
                errors.append(f"metrics.{metric_type} must be a list")
                continue
            actual_ids = [item.get("id") for item in actual if isinstance(item, dict)]
            expected_ids = [item["id"] for item in expected]
            if actual_ids != expected_ids:
                errors.append(f"metrics.{metric_type} must appear exactly in order: {expected_ids}")
            for index, item in enumerate(actual):
                if not isinstance(item, dict):
                    errors.append(f"metrics.{metric_type}[{index}] must be an object")
                    continue
                if index < len(expected) and item.get("target") != expected[index]["target"]:
                    errors.append(f"metric {item.get('id')} target must be {expected[index]['target']}")
                if not non_empty_string(item.get("source")):
                    errors.append(f"metric {item.get('id')} source must be non-empty")

    roadmap = report.get("roadmap")
    if not isinstance(roadmap, list):
        errors.append("roadmap must be a list")
    else:
        expected_phase_ids = ["foundations", "automation", "advanced", "optimization"]
        actual_phase_ids = [phase.get("id") for phase in roadmap if isinstance(phase, dict)]
        if actual_phase_ids != expected_phase_ids:
            errors.append(f"roadmap must contain phases in order: {expected_phase_ids}")
        for index, phase in enumerate(roadmap):
            if not isinstance(phase, dict):
                errors.append(f"roadmap[{index}] must be an object")
                continue
            for field in ["focus", "success_criteria"]:
                if not non_empty_string(phase.get(field)):
                    errors.append(f"roadmap phase {phase.get('id')} {field} must be non-empty")

    priority_actions = report.get("priority_actions")
    target_level = report.get("target_level")
    if not isinstance(priority_actions, list):
        errors.append("priority_actions must be a list")
    elif isinstance(target_level, int) and dimensions:
        expected = expected_priority_actions(dimensions, target_level, levels, canonical_order, action_policy["max_actions"])
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

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        decisions = set(contract["json_contract"]["guardian_decisions"])
        if guardian.get("decision") not in decisions:
            errors.append(f"guardian.decision must be one of {sorted(decisions)}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a quality engineering JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON report")
    args = parser.parse_args()

    try:
        report = load_json(args.report)
        errors = validate(report)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
