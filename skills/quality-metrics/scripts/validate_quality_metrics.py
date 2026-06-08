#!/usr/bin/env python3
"""Validate deterministic quality metrics reports."""

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


def metric_policy(metric_id: str, thresholds: dict[str, Any]) -> dict[str, Any]:
    for item in thresholds["metrics"]:
        if item["id"] == metric_id:
            return item
    raise KeyError(metric_id)


def canonical_ids(thresholds: dict[str, Any]) -> list[str]:
    return [item["id"] for item in thresholds["metrics"]]


def expected_status(metric: dict[str, Any], thresholds: dict[str, Any]) -> str:
    metric_id = str(metric.get("id"))
    if metric.get("measured") is False or metric.get("status") == "na":
        return "na"
    values = metric.get("values")
    if not isinstance(values, dict):
        return "fail"
    cfg = metric_policy(metric_id, thresholds)
    if metric_id == "coverage":
        scores = [float(values.get(field, -1)) for field in cfg["fields"]]
        if all(score >= cfg["pass_min"] for score in scores):
            return "pass"
        if all(score >= cfg["warn_min"] for score in scores):
            return "warn"
        return "fail"
    if metric_id == "complexity":
        value = float(values.get("max_cyclomatic", 10**9))
        if value <= cfg["pass_max"]:
            return "pass"
        if value <= cfg["warn_max"]:
            return "warn"
        return "fail"
    if metric_id == "duplication":
        value = float(values.get("percent", 10**9))
        if value < cfg["pass_max_exclusive"]:
            return "pass"
        if value < cfg["warn_max_exclusive"]:
            return "warn"
        return "fail"
    if metric_id == "lighthouse":
        deltas = []
        for field, minimum in cfg["pass_min"].items():
            deltas.append(float(values.get(field, -1)) - float(minimum))
        if all(delta >= 0 for delta in deltas):
            return "pass"
        if all(delta >= -float(cfg["warn_delta"]) for delta in deltas):
            return "warn"
        return "fail"
    if metric_id == "bundle_size":
        value = float(values.get("initial_gzip_kb", 10**9))
        if value <= cfg["pass_max_kb"]:
            return "pass"
        if value <= cfg["warn_max_kb"]:
            return "warn"
        return "fail"
    if metric_id == "firestore_io":
        reads = float(values.get("reads_per_day", 10**9))
        spike = float(values.get("read_spike_multiplier", 10**9))
        if reads > cfg["fail_max_reads_per_day"] or spike >= cfg["fail_spike_multiplier"]:
            return "fail"
        if reads > cfg["pass_max_reads_per_day"] or spike >= cfg["warn_spike_multiplier"]:
            return "warn"
        return "pass"
    return "fail"


def expected_actions(metrics: list[dict[str, Any]], thresholds: dict[str, Any], max_actions: int) -> list[dict[str, Any]]:
    order = {item["id"]: int(item["order"]) for item in thresholds["metrics"]}
    severity = {"fail": 0, "warn": 1}
    improvement = {"fail": 8, "warn": 4}
    candidates = []
    for metric in metrics:
        status = metric.get("status")
        if status not in improvement:
            continue
        candidates.append(
            {
                "metric": metric["id"],
                "expected_improvement": improvement[status],
                "severity": severity[status],
                "order": order[metric["id"]],
            }
        )
    candidates.sort(key=lambda item: (item["severity"], -item["expected_improvement"], item["order"]))
    return candidates[:max_actions]


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("quality-metrics-contract.json")
    thresholds = policy("metrics-thresholds.json")
    gates_policy = policy("gate-policy.json")
    trend_policy = policy("trend-policy.json")
    action_policy = policy("action-priority-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "quality-metrics":
        errors.append("skill must be quality-metrics")
    for field in ["report_id", "subject", "scope"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if not isinstance(report.get("evidence_summary"), list) or not report.get("evidence_summary"):
        errors.append("evidence_summary must be a non-empty list")
    if not isinstance(report.get("exclusions"), list):
        errors.append("exclusions must be a list")

    metrics = report.get("metrics")
    ids = canonical_ids(thresholds)
    if not isinstance(metrics, list):
        errors.append("metrics must be a list")
        metrics = []
    actual_ids = [item.get("id") for item in metrics if isinstance(item, dict)]
    if actual_ids != ids:
        errors.append(f"metrics must appear exactly in canonical order: {ids}")

    total = 0
    evaluated = 0
    statuses: list[str] = []
    for index, metric in enumerate(metrics):
        if not isinstance(metric, dict):
            errors.append(f"metrics[{index}] must be an object")
            continue
        metric_id = metric.get("id", f"metrics[{index}]")
        if metric_id not in ids:
            errors.append(f"unknown metric id: {metric_id}")
            continue
        expected = expected_status(metric, thresholds)
        status = metric.get("status")
        if status != expected:
            errors.append(f"metric {metric_id} status must be {expected}")
        if status == "na":
            if metric.get("measured") is not False:
                errors.append(f"metric {metric_id} status na requires measured=false")
            if not non_empty_string(metric.get("reason")):
                errors.append(f"metric {metric_id} status na requires reason")
            statuses.append("na")
            continue
        if metric.get("measured") is not True:
            errors.append(f"metric {metric_id} must set measured=true")
        if not isinstance(metric.get("values"), dict):
            errors.append(f"metric {metric_id} values must be an object")
        if not non_empty_string(metric.get("evidence")):
            errors.append(f"metric {metric_id} evidence must be non-empty")
        points = thresholds["score_points"].get(str(status))
        if metric.get("score") != points:
            errors.append(f"metric {metric_id} score must be {points}")
        total += int(points or 0)
        evaluated += 1
        statuses.append(str(status))

    expected_score = round((total / (evaluated * thresholds["score_points"]["pass"])) * 100, 2) if evaluated else 0.0
    actual_score = report.get("quality_score")
    if not isinstance(actual_score, (int, float)) or not math.isclose(float(actual_score), expected_score, abs_tol=0.01):
        errors.append(f"quality_score must be {expected_score}")
    expected_overall = "fail" if "fail" in statuses else "warn" if "warn" in statuses or "na" in statuses else "pass"
    if report.get("overall_status") != expected_overall:
        errors.append(f"overall_status must be {expected_overall}")

    gates = report.get("gates")
    if not isinstance(gates, list):
        errors.append("gates must be a list")
        gates = []
    gate_ids = [gate.get("id") for gate in gates if isinstance(gate, dict)]
    if gate_ids != gates_policy["required_gate_ids"]:
        errors.append(f"gates must appear exactly in canonical order: {gates_policy['required_gate_ids']}")
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"gates[{index}] must be an object")
            continue
        for field in gates_policy["required_fields"]:
            if field not in gate:
                errors.append(f"gate {gate.get('id')} missing field {field}")
        if gate.get("enforced") is not True:
            errors.append(f"gate {gate.get('id')} enforced must be true")
        for field in ["tool", "threshold", "on_failure"]:
            if not non_empty_string(gate.get(field)):
                errors.append(f"gate {gate.get('id')} {field} must be non-empty")

    window = report.get("trend_window")
    if not isinstance(window, int) or window < trend_policy["default_window"]:
        errors.append(f"trend_window must be >= {trend_policy['default_window']}")
    trend = report.get("trend_assessment")
    if not isinstance(trend, dict):
        errors.append("trend_assessment must be an object")
    else:
        if trend.get("status") not in trend_policy["allowed_statuses"]:
            errors.append(f"trend_assessment.status must be one of {trend_policy['allowed_statuses']}")
        if trend.get("status") == "unknown" and not non_empty_string(trend.get("reason")):
            errors.append("trend_assessment.reason must be non-empty when status is unknown")
        if not isinstance(trend.get("snapshots"), int) or trend.get("snapshots") < 0:
            errors.append("trend_assessment.snapshots must be a non-negative integer")

    priority_actions = report.get("priority_actions")
    if not isinstance(priority_actions, list):
        errors.append("priority_actions must be a list")
    else:
        expected = expected_actions(metrics, thresholds, action_policy["max_actions"])
        if len(priority_actions) > action_policy["max_actions"]:
            errors.append(f"priority_actions must contain at most {action_policy['max_actions']} items")
        expected_pairs = [(item["metric"], item["expected_improvement"]) for item in expected]
        actual_pairs = [
            (item.get("metric"), item.get("expected_improvement"))
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
    parser = argparse.ArgumentParser(description="Validate a quality metrics JSON report")
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
