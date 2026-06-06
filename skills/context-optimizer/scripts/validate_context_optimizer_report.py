#!/usr/bin/env python3
"""Validate deterministic Context Optimizer JSON reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.context-optimizer.report.v1"
REQUIRED_TOP = {
    "schema",
    "skill",
    "context_snapshot",
    "loading_plan",
    "compression_plan",
    "eviction_plan",
    "metrics",
    "validation",
}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
LEVELS = {"L1", "L2", "L3"}
COMPRESSION_ACTIONS = {"keep", "compress", "summarize", "defer"}
EVICTION_ACTIONS = {"keep", "compress", "defer", "evict"}
CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "lazy_loading",
    "compression_contract",
    "eviction_safety",
    "metrics",
    "evidence_required",
}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def objects(value: Any, name: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for i, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{name}[{i}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def int_range(value: Any, low: int, high: int) -> bool:
    return isinstance(value, int) and low <= value <= high


def text(obj: dict[str, Any], key: str, ctx: str, errors: list[str]) -> None:
    require(isinstance(obj.get(key), str) and bool(obj[key].strip()), errors, f"{ctx}.{key} required")


def tag(obj: dict[str, Any], ctx: str, errors: list[str]) -> None:
    require(obj.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")


def validate_snapshot(data: dict[str, Any], errors: list[str]) -> None:
    snapshot = data.get("context_snapshot")
    require(isinstance(snapshot, dict), errors, "context_snapshot must be object")
    if not isinstance(snapshot, dict):
        return
    text(snapshot, "active_task", "context_snapshot", errors)
    require(int_range(snapshot.get("max_context_tokens"), 1, 1000000), errors, "context_snapshot.max_context_tokens must be 1..1000000")
    require(int_range(snapshot.get("current_tokens"), 1, 1000000), errors, "context_snapshot.current_tokens must be 1..1000000")
    require(int_range(snapshot.get("target_utilization_percent"), 1, 85), errors, "context_snapshot.target_utilization_percent must be 1..85")
    tag(snapshot, "context_snapshot", errors)


def validate_loading(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("loading_plan"), "loading_plan", errors)
    require(bool(rows), errors, "loading_plan required")
    l3_count = 0
    active_l3 = False
    for i, row in enumerate(rows):
        ctx = f"loading_plan[{i}]"
        text(row, "source_id", ctx, errors)
        require(row.get("level") in LEVELS, errors, f"{ctx}.level invalid")
        score = row.get("relevance_score")
        require(int_range(score, 0, 100), errors, f"{ctx}.relevance_score must be 0..100")
        require(isinstance(row.get("active"), bool), errors, f"{ctx}.active must be boolean")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)
        if row.get("level") == "L3":
            l3_count += 1
            active_l3 = active_l3 or row.get("active") is True
            if isinstance(score, int):
                require(score >= 80, errors, f"{ctx}: L3 requires relevance_score >= 80")
    require(l3_count <= 1, errors, "loading_plan allows at most one L3 source")
    require(active_l3, errors, "loading_plan requires active source at L3")


def validate_compression(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("compression_plan"), "compression_plan", errors)
    for i, row in enumerate(rows):
        ctx = f"compression_plan[{i}]"
        text(row, "artifact_id", ctx, errors)
        require(row.get("action") in COMPRESSION_ACTIONS, errors, f"{ctx}.action invalid")
        current = row.get("current_tokens")
        optimized = row.get("optimized_tokens")
        require(int_range(current, 0, 1000000), errors, f"{ctx}.current_tokens must be 0..1000000")
        require(int_range(optimized, 0, 1000000), errors, f"{ctx}.optimized_tokens must be 0..1000000")
        if row.get("action") in {"compress", "summarize"}:
            require(bool(row.get("retention_summary")), errors, f"{ctx}.retention_summary required for compression")
            if isinstance(current, int) and isinstance(optimized, int):
                require(optimized < current, errors, f"{ctx}: optimized_tokens must be lower than current_tokens")
        tag(row, ctx, errors)


def validate_eviction(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("eviction_plan"), "eviction_plan", errors)
    for i, row in enumerate(rows):
        ctx = f"eviction_plan[{i}]"
        text(row, "source_id", ctx, errors)
        require(row.get("action") in EVICTION_ACTIONS, errors, f"{ctx}.action invalid")
        require(isinstance(row.get("active"), bool), errors, f"{ctx}.active must be boolean")
        require(isinstance(row.get("risk_flag"), bool), errors, f"{ctx}.risk_flag must be boolean")
        score = row.get("relevance_score")
        require(int_range(score, 0, 100), errors, f"{ctx}.relevance_score must be 0..100")
        if row.get("action") == "evict":
            require(row.get("active") is False, errors, f"{ctx}: active source must not be evicted")
            require(row.get("risk_flag") is False, errors, f"{ctx}: risk-flagged source must not be evicted")
            if isinstance(score, int):
                require(score <= 24, errors, f"{ctx}: evict requires relevance_score <= 24")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


def validate_metrics(data: dict[str, Any], errors: list[str]) -> None:
    metrics = data.get("metrics")
    snapshot = data.get("context_snapshot", {})
    require(isinstance(metrics, dict), errors, "metrics must be object")
    if not isinstance(metrics, dict):
        return
    naive = metrics.get("naive_tokens")
    optimized = metrics.get("optimized_tokens")
    reduction = metrics.get("reduction_percent")
    utilization = metrics.get("utilization_percent")
    require(int_range(naive, 1, 1000000), errors, "metrics.naive_tokens must be 1..1000000")
    require(int_range(optimized, 0, 1000000), errors, "metrics.optimized_tokens must be 0..1000000")
    require(int_range(reduction, 0, 100), errors, "metrics.reduction_percent must be 0..100")
    require(int_range(utilization, 0, 100), errors, "metrics.utilization_percent must be 0..100")
    if isinstance(naive, int) and isinstance(optimized, int) and isinstance(reduction, int):
        expected = round(((naive - optimized) * 100) / naive)
        require(reduction == expected, errors, f"metrics.reduction_percent must equal rounded reduction ({expected})")
        require(reduction >= 20, errors, "metrics.reduction_percent must be at least 20")
    max_tokens = snapshot.get("max_context_tokens")
    target_util = snapshot.get("target_utilization_percent")
    if isinstance(max_tokens, int) and isinstance(optimized, int) and isinstance(utilization, int):
        expected_util = round((optimized * 100) / max_tokens)
        require(utilization == expected_util, errors, f"metrics.utilization_percent must equal rounded optimized/max ({expected_util})")
        if isinstance(target_util, int):
            require(utilization <= target_util, errors, "metrics.utilization_percent exceeds target")
    tag(metrics, "metrics", errors)


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if not isinstance(validation, dict):
        return
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    checks = validation.get("checks")
    require(isinstance(checks, list), errors, "validation.checks must be list")
    if isinstance(checks, list):
        require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "context-optimizer", errors, "skill must be context-optimizer")
    validate_snapshot(data, errors)
    validate_loading(data, errors)
    validate_compression(data, errors)
    validate_eviction(data, errors)
    validate_metrics(data, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_context_optimizer_report.py <report.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data if isinstance(data, dict) else {})
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
