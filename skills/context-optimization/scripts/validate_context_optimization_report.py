#!/usr/bin/env python3
"""Validate deterministic Context Optimization JSON reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ["schema_version", "skill", "optimization_target", "skill_loading_plan", "pruning_plan", "session_state_plan", "metrics", "guardian_decision"]
TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
LEVELS = {"L1", "L2", "L3"}
PRUNE_ACTIONS = {"keep", "compress", "prune", "lazy-load"}
PERSIST_LEVELS = {"none", "minimal", "essential", "full"}
DECISIONS = {"pass", "block"}


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def text(obj: dict, key: str, ctx: str, errors: list[str]) -> None:
    if not isinstance(obj.get(key), str) or not obj[key].strip():
        errors.append(f"{ctx}: missing non-empty {key}")


def tag(obj: dict, ctx: str, errors: list[str]) -> None:
    if obj.get("evidence_tag") not in TAGS:
        errors.append(f"{ctx}: evidence_tag must be one of {sorted(TAGS)}")


def int_range(obj: dict, key: str, ctx: str, low: int, high: int, errors: list[str]) -> int | None:
    value = obj.get(key)
    if not isinstance(value, int) or value < low or value > high:
        errors.append(f"{ctx}: {key} must be {low}..{high}")
        return None
    return value


def target(data: dict, errors: list[str]) -> None:
    item = data.get("optimization_target")
    if not isinstance(item, dict):
        errors.append("optimization_target: must be an object")
        return
    text(item, "task", "optimization_target", errors)
    text(item, "phase", "optimization_target", errors)
    int_range(item, "max_context_tokens", "optimization_target", 1, 1000000, errors)
    int_range(item, "target_utilization_percent", "optimization_target", 1, 85, errors)
    tag(item, "optimization_target", errors)


def loading(data: dict, errors: list[str]) -> None:
    rows = data.get("skill_loading_plan")
    if not isinstance(rows, list) or not rows:
        errors.append("skill_loading_plan: must be a non-empty list")
        return
    l3_count = 0
    for index, row in enumerate(rows):
        ctx = f"skill_loading_plan[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "skill", ctx, errors)
        if row.get("level") not in LEVELS:
            errors.append(f"{ctx}: level must be one of {sorted(LEVELS)}")
        score = int_range(row, "relevance_score", ctx, 0, 100, errors)
        if row.get("level") == "L3":
            l3_count += 1
            if score is not None and score < 80:
                errors.append(f"{ctx}: L3 requires relevance_score >= 80")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)
    if l3_count > 1:
        errors.append("skill_loading_plan: at most one L3 skill is allowed")


def pruning(data: dict, errors: list[str]) -> None:
    rows = data.get("pruning_plan")
    if not isinstance(rows, list):
        errors.append("pruning_plan: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"pruning_plan[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "source_id", ctx, errors)
        if row.get("action") not in PRUNE_ACTIONS:
            errors.append(f"{ctx}: action must be one of {sorted(PRUNE_ACTIONS)}")
        score = int_range(row, "relevance_score", ctx, 0, 100, errors)
        if not isinstance(row.get("risk_flag"), bool):
            errors.append(f"{ctx}: risk_flag must be boolean")
        if row.get("action") == "prune":
            if row.get("risk_flag") is True:
                errors.append(f"{ctx}: risk-flagged sources must not be pruned")
            if score is not None and score > 24:
                errors.append(f"{ctx}: prune requires relevance_score <= 24")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


def session_state(data: dict, errors: list[str]) -> None:
    item = data.get("session_state_plan")
    if not isinstance(item, dict):
        errors.append("session_state_plan: must be an object")
        return
    if item.get("persist_level") not in PERSIST_LEVELS:
        errors.append(f"session_state_plan: persist_level must be one of {sorted(PERSIST_LEVELS)}")
    text(item, "target_path", "session_state_plan", errors)
    if not isinstance(item.get("authorized"), bool):
        errors.append("session_state_plan: authorized must be boolean")
    fields = item.get("fields")
    if item.get("persist_level") != "none":
        if item.get("authorized") is not True:
            errors.append("session_state_plan: persistence requires authorized=true")
        if not isinstance(fields, list) or not fields:
            errors.append("session_state_plan: persisted state requires non-empty fields")
    tag(item, "session_state_plan", errors)


def metrics(data: dict, errors: list[str]) -> None:
    item = data.get("metrics")
    target_item = data.get("optimization_target", {})
    if not isinstance(item, dict):
        errors.append("metrics: must be an object")
        return
    naive = int_range(item, "naive_tokens", "metrics", 1, 1000000, errors)
    optimized = int_range(item, "optimized_tokens", "metrics", 0, 1000000, errors)
    improvement = int_range(item, "improvement_percent", "metrics", 0, 100, errors)
    utilization = int_range(item, "utilization_percent", "metrics", 0, 100, errors)
    if naive is not None and optimized is not None and improvement is not None:
        expected = round(((naive - optimized) * 100) / naive)
        if improvement != expected:
            errors.append(f"metrics: improvement_percent must equal rounded reduction ({expected})")
        if improvement < 20:
            errors.append("metrics: improvement_percent must be at least 20")
    max_tokens = target_item.get("max_context_tokens")
    target_util = target_item.get("target_utilization_percent")
    if optimized is not None and isinstance(max_tokens, int) and utilization is not None:
        expected_util = round((optimized * 100) / max_tokens)
        if utilization != expected_util:
            errors.append(f"metrics: utilization_percent must equal rounded optimized/max ({expected_util})")
        if isinstance(target_util, int) and utilization > target_util:
            errors.append("metrics: utilization_percent exceeds target")
    tag(item, "metrics", errors)


def guardian(data: dict, errors: list[str]) -> None:
    item = data.get("guardian_decision")
    if not isinstance(item, dict):
        errors.append("guardian_decision: must be an object")
        return
    if item.get("decision") not in DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(DECISIONS)}")
    text(item, "rationale", "guardian_decision", errors)
    tag(item, "guardian_decision", errors)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "context-optimization":
        errors.append("skill must be context-optimization")
    target(data, errors)
    loading(data, errors)
    pruning(data, errors)
    session_state(data, errors)
    metrics(data, errors)
    guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Context Optimization JSON report")
    parser.add_argument("report")
    args = parser.parse_args()
    path = Path(args.report)
    try:
        data = load(path)
    except ValueError as exc:
        print(f"ERROR: {path}: {exc}")
        return 1
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {path}: {error}")
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
