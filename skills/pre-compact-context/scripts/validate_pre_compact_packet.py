#!/usr/bin/env python3
"""Validate deterministic Pre Compact Context JSON packets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_KEYS = [
    "schema_version",
    "skill",
    "compaction_trigger",
    "preserve_verbatim",
    "compressed_summary",
    "discard_list",
    "open_questions",
    "risks",
    "validation",
    "rehydration_prompt",
    "guardian_decision",
]
ALLOWED_TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
ALLOWED_PRIORITIES = {"P0", "P1", "P2", "DROP"}
ALLOWED_VALIDATION_STATUSES = {"pass", "fail", "skipped", "unknown"}
ALLOWED_GUARDIAN_DECISIONS = {"pass", "block"}
UNSAFE_DROP_TERMS = {"hard rule", "blocker", "validation failure", "branch", "pr", "ci", "next action"}
SECRET_PATTERNS = ("sk-", "ghp_", "xoxb-", "AKIA", "BEGIN PRIVATE KEY")


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


def contains_secret(value: object) -> bool:
    if isinstance(value, str):
        return any(pattern in value for pattern in SECRET_PATTERNS)
    if isinstance(value, list):
        return any(contains_secret(item) for item in value)
    if isinstance(value, dict):
        return any(contains_secret(item) for item in value.values())
    return False


def validate_preserve(data: dict, errors: list[str]) -> None:
    items = data.get("preserve_verbatim")
    if not isinstance(items, list) or not items:
        errors.append("preserve_verbatim: must be a non-empty list")
        return
    has_p0 = False
    for index, item in enumerate(items):
        context = f"preserve_verbatim[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{context}: must be an object")
            continue
        priority = item.get("priority")
        if priority not in ALLOWED_PRIORITIES - {"DROP"}:
            errors.append(f"{context}: priority must be P0, P1, or P2")
        if priority == "P0":
            has_p0 = True
        for key in ["item", "source", "reason"]:
            require_text(item, key, context, errors)
        validate_tag(item, context, errors)
    if not has_p0:
        errors.append("preserve_verbatim: at least one P0 item is required")


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


def validate_discard(data: dict, errors: list[str]) -> None:
    items = data.get("discard_list")
    if not isinstance(items, list):
        errors.append("discard_list: must be a list")
        return
    for index, item in enumerate(items):
        context = f"discard_list[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{context}: must be an object")
            continue
        require_text(item, "description", context, errors)
        require_text(item, "reason", context, errors)
        validate_tag(item, context, errors)
        text = f"{item.get('description', '')} {item.get('reason', '')}".lower()
        for term in UNSAFE_DROP_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", text):
                errors.append(f"{context}: DROP contains unsafe active context term: {term}")


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


def validate_rehydration(data: dict, errors: list[str]) -> None:
    prompt = data.get("rehydration_prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        errors.append("rehydration_prompt: missing non-empty text")
        return
    lower = prompt.lower()
    for term in ["repo", "branch", "objective", "next action"]:
        if term not in lower:
            errors.append(f"rehydration_prompt: missing {term}")


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


def validate_packet(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "pre-compact-context":
        errors.append("skill must be pre-compact-context")
    validate_tagged_list(data, "compaction_trigger", errors, allow_empty=False)
    validate_preserve(data, errors)
    validate_tagged_list(data, "compressed_summary", errors)
    validate_discard(data, errors)
    validate_tagged_list(data, "open_questions", errors)
    validate_tagged_list(data, "risks", errors)
    validate_validation(data, errors)
    validate_rehydration(data, errors)
    validate_guardian(data, errors)
    if contains_secret(data):
        errors.append("packet contains an unredacted secret-like token")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Pre Compact Context JSON packet")
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
