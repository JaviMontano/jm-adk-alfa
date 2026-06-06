#!/usr/bin/env python3
"""Validate deterministic Tasklog Management JSON reports."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


REQUIRED = [
    "schema_version",
    "skill",
    "as_of_date",
    "tasklog_snapshot",
    "operations",
    "stale_review",
    "bridge_review",
    "archive_review",
    "guardian_decision",
]
TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
TASK_ID = re.compile(r"^TL-[0-9]{3}$")
BRIDGE = re.compile(r"^workspace/tasks/TL-[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*/README\.md$")
STATUSES = {"open", "in-progress", "blocked", "deferred", "completed"}
ACTIVE = {"open", "in-progress", "blocked"}
OPERATIONS = {"add", "update", "close", "block", "defer", "bridge", "archive", "none"}
WRITE_OPERATIONS = OPERATIONS - {"none"}
TRANSITIONS = {
    "none": {"open", "in-progress", "blocked", "deferred"},
    "open": {"in-progress", "blocked", "deferred", "completed"},
    "in-progress": {"blocked", "deferred", "completed"},
    "blocked": {"in-progress", "deferred", "completed"},
    "deferred": {"open", "in-progress", "completed"},
    "completed": set(),
}
SNAPSHOT_STATUSES = {"present", "missing", "invalid"}
DECISIONS = {"pass", "block"}


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def parse_date(value: object, ctx: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{ctx}: date must be YYYY-MM-DD")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{ctx}: date must be YYYY-MM-DD")
        return None


def text(obj: dict, key: str, ctx: str, errors: list[str]) -> None:
    if not isinstance(obj.get(key), str) or not obj[key].strip():
        errors.append(f"{ctx}: missing non-empty {key}")


def tag(obj: dict, ctx: str, errors: list[str]) -> None:
    if obj.get("evidence_tag") not in TAGS:
        errors.append(f"{ctx}: evidence_tag must be one of {sorted(TAGS)}")


def task_id(value: object, ctx: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not TASK_ID.match(value):
        errors.append(f"{ctx}: task_id must match TL-NNN")


def snapshot(data: dict, errors: list[str]) -> None:
    item = data.get("tasklog_snapshot")
    if not isinstance(item, dict):
        errors.append("tasklog_snapshot: must be an object")
        return
    text(item, "path", "tasklog_snapshot", errors)
    if item.get("status") not in SNAPSHOT_STATUSES:
        errors.append(f"tasklog_snapshot: status must be one of {sorted(SNAPSHOT_STATUSES)}")
    if not isinstance(item.get("task_count"), int) or item["task_count"] < 0:
        errors.append("tasklog_snapshot: task_count must be a non-negative integer")
    tag(item, "tasklog_snapshot", errors)


def operations(data: dict, errors: list[str]) -> None:
    rows = data.get("operations")
    if not isinstance(rows, list):
        errors.append("operations: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"operations[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        operation = row.get("operation")
        if operation not in OPERATIONS:
            errors.append(f"{ctx}: operation must be one of {sorted(OPERATIONS)}")
        task_id(row.get("task_id"), ctx, errors)
        from_status = row.get("from_status")
        to_status = row.get("to_status")
        if from_status != "none" and from_status not in STATUSES:
            errors.append(f"{ctx}: from_status must be none or one of {sorted(STATUSES)}")
        if to_status != "none" and to_status not in STATUSES:
            errors.append(f"{ctx}: to_status must be none or one of {sorted(STATUSES)}")
        if from_status in TRANSITIONS and to_status != "none" and to_status not in TRANSITIONS[from_status]:
            errors.append(f"{ctx}: transition {from_status}->{to_status} is not allowed")
        if operation == "close" and to_status != "completed":
            errors.append(f"{ctx}: close operation must transition to completed")
        if operation in WRITE_OPERATIONS and row.get("authorized") is not True:
            errors.append(f"{ctx}: write operation requires authorized=true")
        if not isinstance(row.get("authorized"), bool):
            errors.append(f"{ctx}: authorized must be boolean")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


def stale_review(data: dict, as_of: date | None, errors: list[str]) -> None:
    rows = data.get("stale_review")
    if not isinstance(rows, list):
        errors.append("stale_review: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"stale_review[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        task_id(row.get("task_id"), ctx, errors)
        status = row.get("status")
        if status not in STATUSES:
            errors.append(f"{ctx}: status must be one of {sorted(STATUSES)}")
        last_update = parse_date(row.get("last_update"), f"{ctx}.last_update", errors)
        if not isinstance(row.get("age_days"), int) or row["age_days"] < 0:
            errors.append(f"{ctx}: age_days must be a non-negative integer")
        elif as_of and last_update:
            expected = (as_of - last_update).days
            if row["age_days"] != expected:
                errors.append(f"{ctx}: age_days must equal as_of_date - last_update ({expected})")
        stale = row.get("stale")
        if not isinstance(stale, bool):
            errors.append(f"{ctx}: stale must be boolean")
        elif status in ACTIVE and isinstance(row.get("age_days"), int):
            if row["age_days"] > 14 and stale is not True:
                errors.append(f"{ctx}: active task older than 14 days must be stale")
            if row["age_days"] <= 14 and stale is not False:
                errors.append(f"{ctx}: active task at or below 14 days must not be stale")
        text(row, "action", ctx, errors)
        if stale is True and row.get("action") != "review_required":
            errors.append(f"{ctx}: stale task action must be review_required")
        tag(row, ctx, errors)


def bridge_review(data: dict, errors: list[str]) -> None:
    rows = data.get("bridge_review")
    if not isinstance(rows, list):
        errors.append("bridge_review: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"bridge_review[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        task_id(row.get("task_id"), ctx, errors)
        if not isinstance(row.get("needs_bridge"), bool):
            errors.append(f"{ctx}: needs_bridge must be boolean")
        if not isinstance(row.get("bridge_path"), str):
            errors.append(f"{ctx}: bridge_path must be a string")
        if row.get("needs_bridge") is True and not BRIDGE.match(str(row.get("bridge_path", ""))):
            errors.append(f"{ctx}: bridge_path must match workspace/tasks/TL-NNN-slug/README.md")
        if not isinstance(row.get("exists"), bool):
            errors.append(f"{ctx}: exists must be boolean")
        text(row, "action", ctx, errors)
        tag(row, ctx, errors)


def archive_review(data: dict, as_of: date | None, errors: list[str]) -> None:
    rows = data.get("archive_review")
    if not isinstance(rows, list):
        errors.append("archive_review: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"archive_review[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        task_id(row.get("task_id"), ctx, errors)
        completed_date = parse_date(row.get("completed_date"), f"{ctx}.completed_date", errors)
        if not isinstance(row.get("age_days"), int) or row["age_days"] < 0:
            errors.append(f"{ctx}: age_days must be a non-negative integer")
        elif as_of and completed_date:
            expected = (as_of - completed_date).days
            if row["age_days"] != expected:
                errors.append(f"{ctx}: age_days must equal as_of_date - completed_date ({expected})")
        eligible = row.get("archive_eligible")
        if not isinstance(eligible, bool):
            errors.append(f"{ctx}: archive_eligible must be boolean")
        elif isinstance(row.get("age_days"), int):
            if row["age_days"] > 30 and eligible is not True:
                errors.append(f"{ctx}: completed task older than 30 days must be archive_eligible")
            if row["age_days"] <= 30 and eligible is not False:
                errors.append(f"{ctx}: completed task at or below 30 days must not be archive_eligible")
        text(row, "action", ctx, errors)
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
    if item.get("decision") == "pass" and data.get("tasklog_snapshot", {}).get("status") != "present":
        errors.append("guardian_decision: pass requires present tasklog.md")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "tasklog-management":
        errors.append("skill must be tasklog-management")
    as_of = parse_date(data.get("as_of_date"), "as_of_date", errors)
    snapshot(data, errors)
    operations(data, errors)
    stale_review(data, as_of, errors)
    bridge_review(data, errors)
    archive_review(data, as_of, errors)
    guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Tasklog Management JSON report")
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
