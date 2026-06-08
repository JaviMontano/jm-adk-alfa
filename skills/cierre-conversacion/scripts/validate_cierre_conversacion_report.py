#!/usr/bin/env python3
"""Validate deterministic cierre-conversacion JSON reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_KEYS = [
    "schema_version",
    "skill",
    "trigger",
    "conversation",
    "summary",
    "completed_work",
    "decisions",
    "open_tasks",
    "learnings",
    "risks",
    "validation",
    "durable_update_plan",
    "handoff",
    "guardian_decision",
]
ALLOWED_TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]", "[POR_CONFIRMAR]"}
ALLOWED_TRIGGERS = {"explicit", "threshold", "session-audit", "manual"}
ALLOWED_TASK_STATUSES = {"done", "open", "blocked", "proposed"}
ALLOWED_VALIDATION_STATUSES = {"pass", "fail", "skipped", "unknown"}
ALLOWED_UPDATE_TARGETS = {"tasklog", "changelog", "memory", "review_doc", "ledger", "none"}
ALLOWED_UPDATE_ACTIONS = {"append", "propose", "skip"}
ALLOWED_AUTHORITY = {"confirmed", "pending", "not-applicable"}
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


def validate_tagged_item(item: dict, context: str, errors: list[str]) -> None:
    require_text(item, "description", context, errors)
    validate_tag(item, context, errors)


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
        validate_tagged_item(item, context, errors)


def validate_trigger(data: dict, errors: list[str]) -> None:
    trigger = data.get("trigger")
    if not isinstance(trigger, dict):
        errors.append("trigger: must be an object")
        return
    if trigger.get("source") not in ALLOWED_TRIGGERS:
        errors.append(f"trigger: source must be one of {sorted(ALLOWED_TRIGGERS)}")
    require_text(trigger, "reason", "trigger", errors)
    validate_tag(trigger, "trigger", errors)


def validate_conversation(data: dict, errors: list[str]) -> None:
    conversation = data.get("conversation")
    if not isinstance(conversation, dict):
        errors.append("conversation: must be an object")
        return
    require_text(conversation, "objective", "conversation", errors)
    require_text(conversation, "scope", "conversation", errors)
    turns = conversation.get("turns_observed")
    if not isinstance(turns, int) or turns < 0:
        errors.append("conversation: turns_observed must be a non-negative integer")
    validate_tag(conversation, "conversation", errors)


def validate_completed_work(data: dict, errors: list[str]) -> None:
    items = data.get("completed_work")
    if not isinstance(items, list):
        errors.append("completed_work: must be a list")
        return
    for index, item in enumerate(items):
        context = f"completed_work[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{context}: must be an object")
            continue
        validate_tagged_item(item, context, errors)
        require_text(item, "completion_evidence", context, errors)
        if item.get("evidence_tag") in {"[SUPUESTO]", "[POR_CONFIRMAR]"}:
            errors.append(f"{context}: completed work cannot rely on assumption or open evidence")


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
        validate_tagged_item(task, context, errors)
        if task.get("status") not in ALLOWED_TASK_STATUSES:
            errors.append(f"{context}: status must be one of {sorted(ALLOWED_TASK_STATUSES)}")
        require_text(task, "next_action", context, errors)
        if task.get("status") == "done":
            require_text(task, "completion_evidence", context, errors)
            if task.get("evidence_tag") in {"[SUPUESTO]", "[POR_CONFIRMAR]"}:
                errors.append(f"{context}: done task cannot rely on assumption or open evidence")


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
        if entry.get("status") not in ALLOWED_VALIDATION_STATUSES:
            errors.append(f"{context}: status must be one of {sorted(ALLOWED_VALIDATION_STATUSES)}")
        require_text(entry, "evidence", context, errors)
        validate_tag(entry, context, errors)


def validate_durable_updates(data: dict, errors: list[str]) -> None:
    entries = data.get("durable_update_plan")
    if not isinstance(entries, list):
        errors.append("durable_update_plan: must be a list")
        return
    for index, entry in enumerate(entries):
        context = f"durable_update_plan[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{context}: must be an object")
            continue
        if entry.get("target") not in ALLOWED_UPDATE_TARGETS:
            errors.append(f"{context}: target must be one of {sorted(ALLOWED_UPDATE_TARGETS)}")
        action = entry.get("action")
        authority = entry.get("authority")
        if action not in ALLOWED_UPDATE_ACTIONS:
            errors.append(f"{context}: action must be one of {sorted(ALLOWED_UPDATE_ACTIONS)}")
        if authority not in ALLOWED_AUTHORITY:
            errors.append(f"{context}: authority must be one of {sorted(ALLOWED_AUTHORITY)}")
        require_text(entry, "content_summary", context, errors)
        validate_tag(entry, context, errors)
        if action == "append" and authority != "confirmed":
            errors.append(f"{context}: append requires confirmed authority")
        if action == "skip" and authority != "not-applicable":
            errors.append(f"{context}: skip requires not-applicable authority")


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
    if decision == "pass":
        failed = [
            entry
            for entry in data.get("validation", [])
            if isinstance(entry, dict) and entry.get("status") == "fail"
        ]
        if failed:
            errors.append("guardian_decision: pass cannot include failed validation entries")
        unsafe_appends = [
            entry
            for entry in data.get("durable_update_plan", [])
            if isinstance(entry, dict)
            and entry.get("action") == "append"
            and entry.get("authority") != "confirmed"
        ]
        if unsafe_appends:
            errors.append("guardian_decision: pass cannot include unapproved durable append")


def validate_report(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "cierre-conversacion":
        errors.append("skill must be cierre-conversacion")

    validate_trigger(data, errors)
    validate_conversation(data, errors)
    summary = data.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary: must be an object")
    else:
        validate_tagged_item(summary, "summary", errors)
    validate_completed_work(data, errors)
    for key in ["decisions", "learnings", "risks"]:
        validate_tagged_list(data, key, errors)
    validate_open_tasks(data, errors)
    validate_validation(data, errors)
    validate_durable_updates(data, errors)
    handoff = data.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("handoff: must be an object")
    else:
        require_text(handoff, "next_action", "handoff", errors)
        validate_tag(handoff, "handoff", errors)
    validate_guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a cierre-conversacion JSON closeout report")
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
