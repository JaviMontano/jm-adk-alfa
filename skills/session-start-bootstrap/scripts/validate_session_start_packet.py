#!/usr/bin/env python3
"""Validate deterministic Session Start Bootstrap JSON packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_KEYS = [
    "schema_version",
    "skill",
    "environment",
    "context_sources_loaded",
    "active_guardrails",
    "current_state",
    "blockers_and_gaps",
    "validation_baseline",
    "first_action",
    "guardian_decision",
]
ALLOWED_TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
ENV_STATUSES = {"clean", "dirty", "unknown"}
VALIDATION_STATUSES = {"pass", "fail", "skipped", "unknown"}
GUARDIAN_DECISIONS = {"pass", "block"}


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
    if item.get("evidence_tag") not in ALLOWED_TAGS:
        errors.append(f"{context}: evidence_tag must be one of {sorted(ALLOWED_TAGS)}")


def validate_environment(data: dict, errors: list[str]) -> None:
    env = data.get("environment")
    if not isinstance(env, dict):
        errors.append("environment: must be an object")
        return
    for key in ["repo", "branch", "git_status"]:
        require_text(env, key, "environment", errors)
    if env.get("status") not in ENV_STATUSES:
        errors.append(f"environment: status must be one of {sorted(ENV_STATUSES)}")
    validate_tag(env, "environment", errors)


def validate_tagged_list(data: dict, key: str, errors: list[str], allow_empty: bool = True) -> None:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}: must be a list")
        return
    if not allow_empty and not value:
        errors.append(f"{key}: must not be empty")
    for index, item in enumerate(value):
        context = f"{key}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{context}: must be an object")
            continue
        require_text(item, "description", context, errors)
        validate_tag(item, context, errors)


def validate_validation(data: dict, errors: list[str]) -> None:
    entries = data.get("validation_baseline")
    if not isinstance(entries, list):
        errors.append("validation_baseline: must be a list")
        return
    for index, entry in enumerate(entries):
        context = f"validation_baseline[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{context}: must be an object")
            continue
        require_text(entry, "command", context, errors)
        require_text(entry, "evidence", context, errors)
        if entry.get("status") not in VALIDATION_STATUSES:
            errors.append(f"{context}: status must be one of {sorted(VALIDATION_STATUSES)}")
        validate_tag(entry, context, errors)


def validate_guardian(data: dict, errors: list[str]) -> None:
    guardian = data.get("guardian_decision")
    if not isinstance(guardian, dict):
        errors.append("guardian_decision: must be an object")
        return
    decision = guardian.get("decision")
    if decision not in GUARDIAN_DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(GUARDIAN_DECISIONS)}")
    require_text(guardian, "rationale", "guardian_decision", errors)
    validate_tag(guardian, "guardian_decision", errors)
    env = data.get("environment", {})
    if decision == "pass" and isinstance(env, dict) and env.get("status") != "clean":
        errors.append("guardian_decision: pass requires clean environment")
    if decision == "pass":
        blockers = data.get("blockers_and_gaps", [])
        blocking_items = [
            item for item in blockers
            if isinstance(item, dict) and item.get("blocking") is True
        ]
        if blocking_items:
            errors.append("guardian_decision: pass cannot include blocking gaps")


def validate_packet(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "session-start-bootstrap":
        errors.append("skill must be session-start-bootstrap")
    validate_environment(data, errors)
    validate_tagged_list(data, "context_sources_loaded", errors, allow_empty=False)
    validate_tagged_list(data, "active_guardrails", errors, allow_empty=False)
    validate_tagged_list(data, "current_state", errors)
    validate_tagged_list(data, "blockers_and_gaps", errors)
    validate_validation(data, errors)
    if not isinstance(data.get("first_action"), str) or not data["first_action"].strip():
        errors.append("first_action: missing non-empty text")
    validate_guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Session Start Bootstrap JSON packet")
    parser.add_argument("packet", help="Path to packet JSON")
    args = parser.parse_args()
    path = Path(args.packet)
    try:
        data = load_json(path)
    except ValueError as exc:
        print(f"ERROR: {path}: {exc}")
        return 1
    errors = validate_packet(data)
    for error in errors:
        print(f"ERROR: {path}: {error}")
    print(f"packet={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
