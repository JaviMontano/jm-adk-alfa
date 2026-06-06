#!/usr/bin/env python3
"""Validate deterministic Session Protocol JSON reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ["schema_version", "skill", "context_loading", "state_recovery", "pending_closure", "next_steps", "confirmation_gate", "guardian_decision"]
TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
SOURCE_STATUSES = {"loaded", "missing", "skipped"}
RECOMMENDATIONS = {"close", "continue", "defer", "archive"}
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


def context_loading(data: dict, errors: list[str]) -> None:
    rows = data.get("context_loading")
    if not isinstance(rows, list) or not rows:
        errors.append("context_loading: must be a non-empty list")
        return
    orders = []
    for i, row in enumerate(rows):
        ctx = f"context_loading[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        if not isinstance(row.get("order"), int):
            errors.append(f"{ctx}: order must be an integer")
        else:
            orders.append(row["order"])
        text(row, "source", ctx, errors)
        if row.get("status") not in SOURCE_STATUSES:
            errors.append(f"{ctx}: status must be one of {sorted(SOURCE_STATUSES)}")
        tag(row, ctx, errors)
    if orders != sorted(orders):
        errors.append("context_loading: orders must be sorted")


def tagged_list(data: dict, key: str, errors: list[str], allow_empty: bool = True) -> None:
    rows = data.get(key)
    if not isinstance(rows, list):
        errors.append(f"{key}: must be a list")
        return
    if not allow_empty and not rows:
        errors.append(f"{key}: must not be empty")
    for i, row in enumerate(rows):
        ctx = f"{key}[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "description", ctx, errors)
        tag(row, ctx, errors)


def closure(data: dict, errors: list[str]) -> None:
    rows = data.get("pending_closure")
    if not isinstance(rows, list):
        errors.append("pending_closure: must be a list")
        return
    for i, row in enumerate(rows):
        ctx = f"pending_closure[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "item", ctx, errors)
        if row.get("recommendation") not in RECOMMENDATIONS:
            errors.append(f"{ctx}: recommendation must be one of {sorted(RECOMMENDATIONS)}")
        if row.get("applied") is True:
            errors.append(f"{ctx}: recommendations must not be applied before confirmation")
        tag(row, ctx, errors)


def next_steps(data: dict, errors: list[str]) -> None:
    rows = data.get("next_steps")
    if not isinstance(rows, list):
        errors.append("next_steps: must be a list")
        return
    if not (2 <= len(rows) <= 3):
        errors.append("next_steps: expected 2-3 steps")
    for i, row in enumerate(rows):
        ctx = f"next_steps[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "description", ctx, errors)
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


def confirmation(data: dict, errors: list[str]) -> None:
    gate = data.get("confirmation_gate")
    if not isinstance(gate, dict):
        errors.append("confirmation_gate: must be an object")
        return
    if gate.get("user_confirmed") is True and gate.get("work_started") is True:
        return
    if gate.get("work_started") is True:
        errors.append("confirmation_gate: work_started requires user_confirmed=true")
    text(gate, "message", "confirmation_gate", errors)
    tag(gate, "confirmation_gate", errors)


def guardian(data: dict, errors: list[str]) -> None:
    item = data.get("guardian_decision")
    if not isinstance(item, dict):
        errors.append("guardian_decision: must be an object")
        return
    if item.get("decision") not in DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(DECISIONS)}")
    text(item, "rationale", "guardian_decision", errors)
    tag(item, "guardian_decision", errors)
    if item.get("decision") == "pass" and data.get("confirmation_gate", {}).get("work_started") is True and data.get("confirmation_gate", {}).get("user_confirmed") is not True:
        errors.append("guardian_decision: pass cannot allow unconfirmed work")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "session-protocol":
        errors.append("skill must be session-protocol")
    context_loading(data, errors)
    tagged_list(data, "state_recovery", errors)
    closure(data, errors)
    next_steps(data, errors)
    confirmation(data, errors)
    guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Session Protocol JSON report")
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
