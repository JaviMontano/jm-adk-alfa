#!/usr/bin/env python3
"""Validate deterministic Session End Cleanup JSON reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_KEYS = [
    "schema_version",
    "skill",
    "session",
    "summary",
    "changes_completed",
    "decisions",
    "open_tasks",
    "insights",
    "risks",
    "validation",
    "durable_updates",
    "next_handoff",
    "guardian_decision",
]
ALLOWED_TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
ALLOWED_TASK_STATUSES = {"done", "open", "blocked", "proposed"}
ALLOWED_VALIDATION_STATUSES = {"pass", "fail", "skipped", "unknown"}
ALLOWED_GUARDIAN_DECISIONS = {"pass", "block"}


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def require_text(item: dict, key: str, context: str, errors: list[str]) -> None:
    if not isinstance(item.get(key), str) or not item[key].strip():
        errors.append(f"{context}: missing non-empty {key}")


def validate_tag(item: dict, context: str, errors: list[str]) -> None:
    tag = item.get("evidence_tag")
    if tag not in ALLOWED_TAGS:
        errors.append(f"{context}: evidence_tag must be one of {sorted(ALLOWED_TAGS)}")


def validate_tagged_list(data: dict, key: str, errors: list[str]) -> None:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}: must be a list")
        return
    for index, item in enumerate(value):
        context = f"{key}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{context}: must be an object")
            continue
        require_text(item, "description", context, errors)
        validate_tag(item, context, errors)


def validate_open_tasks(data: dict, errors: list[str]) -> None:
    tasks = data.get("open_tasks")
    if not isinstance(tasks, list):
        errors.append("open_tasks: must be a list")
        return
    for index, task in enumerate(tasks):
        context = f"open_tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{context}: must be an object")
            continue
        require_text(task, "description", context, errors)
        status = task.get("status")
        if status not in ALLOWED_TASK_STATUSES:
            errors.append(f"{context}: status must be one of {sorted(ALLOWED_TASK_STATUSES)}")
        validate_tag(task, context, errors)
        require_text(task, "next_action", context, errors)
        if status == "done":
            require_text(task, "completion_evidence", context, errors)
            if task.get("evidence_tag") in {"[ASSUMPTION]", "[OPEN]"}:
                errors.append(f"{context}: done task cannot rely on assumption/open evidence")


def validate_validation(data: dict, errors: list[str]) -> None:
    entries = data.get("validation")
    if not isinstance(entries, list):
        errors.append("validation: must be a list")
        return
    for index, entry in enumerate(entries):
        context = f"validation[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{context}: must be an object")
            continue
        require_text(entry, "command", context, errors)
        status = entry.get("status")
        if status not in ALLOWED_VALIDATION_STATUSES:
            errors.append(f"{context}: status must be one of {sorted(ALLOWED_VALIDATION_STATUSES)}")
        require_text(entry, "evidence", context, errors)
        validate_tag(entry, context, errors)


def validate_guardian(data: dict, errors: list[str]) -> None:
    guardian = data.get("guardian_decision")
    if not isinstance(guardian, dict):
        errors.append("guardian_decision: must be an object")
        return
    decision = guardian.get("decision")
    if decision not in ALLOWED_GUARDIAN_DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(ALLOWED_GUARDIAN_DECISIONS)}")
    require_text(guardian, "rationale", "guardian_decision", errors)
    validate_tag(guardian, "guardian_decision", errors)
    if decision == "pass" and not data.get("validation"):
        errors.append("guardian_decision: pass requires at least one validation entry")
    if decision == "pass":
        failed = [
            entry
            for entry in data.get("validation", [])
            if isinstance(entry, dict) and entry.get("status") == "fail"
        ]
        if failed:
            errors.append("guardian_decision: pass cannot include failed validation entries")


def validate_report(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "session-end-cleanup":
        errors.append("skill must be session-end-cleanup")

    session = data.get("session")
    if not isinstance(session, dict):
        errors.append("session: must be an object")
    else:
        require_text(session, "objective", "session", errors)
        require_text(session, "scope", "session", errors)
        validate_tag(session, "session", errors)

    require_text(data, "summary", "summary", errors)
    require_text(data, "next_handoff", "next_handoff", errors)

    for key in ["changes_completed", "decisions", "insights", "risks", "durable_updates"]:
        validate_tagged_list(data, key, errors)
    validate_open_tasks(data, errors)
    validate_validation(data, errors)
    validate_guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Session End Cleanup JSON report")
    parser.add_argument("report", help="Path to report JSON")
    args = parser.parse_args()
    path = Path(args.report)
    try:
        data = load_json(path)
    except ValueError as exc:
        print(f"ERROR: {path}: {exc}")
        return 1
    errors = validate_report(data)
    for error in errors:
        print(f"ERROR: {path}: {error}")
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
