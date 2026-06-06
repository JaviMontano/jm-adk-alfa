#!/usr/bin/env python3
"""Validate deterministic Context Window Management JSON reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = [
    "schema_version",
    "skill",
    "token_budget",
    "context_items",
    "compression_plan",
    "eviction_plan",
    "guardian_decision",
]
TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
ACTIONS = {"keep", "compress", "evict", "reference-only", "structured-summary"}
METHODS = {"extractive-summary", "structured-summary", "reference-only"}
REQUIRED_PRESERVE = {"ids", "paths", "decisions", "blockers", "validation_evidence", "open_questions"}
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


def nonnegative_int(obj: dict, key: str, ctx: str, errors: list[str]) -> int | None:
    value = obj.get(key)
    if not isinstance(value, int) or value < 0:
        errors.append(f"{ctx}: {key} must be a non-negative integer")
        return None
    return value


def budget(data: dict, errors: list[str]) -> None:
    item = data.get("token_budget")
    if not isinstance(item, dict):
        errors.append("token_budget: must be an object")
        return
    max_tokens = nonnegative_int(item, "max_context_tokens", "token_budget", errors)
    reserve = nonnegative_int(item, "reserved_response_tokens", "token_budget", errors)
    available = nonnegative_int(item, "available_context_tokens", "token_budget", errors)
    nonnegative_int(item, "current_estimated_tokens", "token_budget", errors)
    post = nonnegative_int(item, "post_plan_estimated_tokens", "token_budget", errors)
    if max_tokens is not None and reserve is not None and available is not None:
        expected = max_tokens - reserve
        if expected < 0 or available != expected:
            errors.append(f"token_budget: available_context_tokens must equal max_context_tokens - reserved_response_tokens ({expected})")
    if available is not None and post is not None and post > available:
        errors.append("token_budget: post_plan_estimated_tokens exceeds available_context_tokens")
    tag(item, "token_budget", errors)


def context_items(data: dict, errors: list[str]) -> None:
    rows = data.get("context_items")
    if not isinstance(rows, list) or not rows:
        errors.append("context_items: must be a non-empty list")
        return
    for index, row in enumerate(rows):
        ctx = f"context_items[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "id", ctx, errors)
        text(row, "source", ctx, errors)
        if row.get("priority") not in PRIORITIES:
            errors.append(f"{ctx}: priority must be one of {sorted(PRIORITIES)}")
        nonnegative_int(row, "estimated_tokens", ctx, errors)
        if row.get("retention_action") not in ACTIONS:
            errors.append(f"{ctx}: retention_action must be one of {sorted(ACTIONS)}")
        if row.get("priority") == "P0" and row.get("retention_action") == "evict":
            errors.append(f"{ctx}: P0 context must not be evicted")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


def compression_plan(data: dict, errors: list[str]) -> None:
    rows = data.get("compression_plan")
    if not isinstance(rows, list):
        errors.append("compression_plan: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"compression_plan[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "source_id", ctx, errors)
        if row.get("method") not in METHODS:
            errors.append(f"{ctx}: method must be one of {sorted(METHODS)}")
        before = nonnegative_int(row, "estimated_tokens_before", ctx, errors)
        after = nonnegative_int(row, "estimated_tokens_after", ctx, errors)
        if before is not None and after is not None and after > before:
            errors.append(f"{ctx}: compression must not increase token estimate")
        preserves = row.get("preserves")
        if not isinstance(preserves, list) or not set(preserves).issuperset(REQUIRED_PRESERVE):
            errors.append(f"{ctx}: preserves must include {sorted(REQUIRED_PRESERVE)}")
        tag(row, ctx, errors)


def eviction_plan(data: dict, errors: list[str]) -> None:
    rows = data.get("eviction_plan")
    if not isinstance(rows, list):
        errors.append("eviction_plan: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"eviction_plan[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "source_id", ctx, errors)
        if row.get("priority") not in PRIORITIES:
            errors.append(f"{ctx}: priority must be one of {sorted(PRIORITIES)}")
        if row.get("priority") == "P0":
            errors.append(f"{ctx}: P0 context must not be evicted")
        text(row, "reason", ctx, errors)
        tag(row, ctx, errors)


def guardian(data: dict, errors: list[str]) -> None:
    item = data.get("guardian_decision")
    if not isinstance(item, dict):
        errors.append("guardian_decision: must be an object")
        return
    if item.get("decision") not in DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(DECISIONS)}")
    text(item, "rationale", "guardian_decision", errors)
    tag(item, "guardian_decision", errors)
    budget_item = data.get("token_budget", {})
    if item.get("decision") == "pass" and isinstance(budget_item, dict):
        available = budget_item.get("available_context_tokens")
        post = budget_item.get("post_plan_estimated_tokens")
        if isinstance(available, int) and isinstance(post, int) and post > available:
            errors.append("guardian_decision: pass requires post-plan tokens to fit")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "context-window-management":
        errors.append("skill must be context-window-management")
    budget(data, errors)
    context_items(data, errors)
    compression_plan(data, errors)
    eviction_plan(data, errors)
    guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Context Window Management JSON report")
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
