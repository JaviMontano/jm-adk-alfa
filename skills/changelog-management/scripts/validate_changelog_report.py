#!/usr/bin/env python3
"""Validate deterministic Changelog Management JSON reports."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


REQUIRED = [
    "schema_version",
    "skill",
    "as_of_date",
    "changelog_snapshot",
    "proposed_entries",
    "duplicate_review",
    "ordering_review",
    "guardian_decision",
]
TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
ENTRY_TYPES = {"decision", "completion", "amendment", "insight", "blocker", "discovery"}
SNAPSHOT_STATUSES = {"present", "missing", "invalid"}
DEDUPE_ACTIONS = {"append", "skip", "revise"}
POSITIONS = {"top", "existing-section", "blocked"}
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


def string_list(obj: dict, key: str, ctx: str, errors: list[str]) -> None:
    value = obj.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{ctx}: {key} must be a non-empty list of strings")


def snapshot(data: dict, errors: list[str]) -> None:
    item = data.get("changelog_snapshot")
    if not isinstance(item, dict):
        errors.append("changelog_snapshot: must be an object")
        return
    text(item, "path", "changelog_snapshot", errors)
    if item.get("status") not in SNAPSHOT_STATUSES:
        errors.append(f"changelog_snapshot: status must be one of {sorted(SNAPSHOT_STATUSES)}")
    if not isinstance(item.get("recent_entries_loaded"), int) or item["recent_entries_loaded"] < 0:
        errors.append("changelog_snapshot: recent_entries_loaded must be a non-negative integer")
    if not isinstance(item.get("newest_first"), bool):
        errors.append("changelog_snapshot: newest_first must be boolean")
    tag(item, "changelog_snapshot", errors)


def proposed_entries(data: dict, as_of: date | None, errors: list[str]) -> None:
    rows = data.get("proposed_entries")
    if not isinstance(rows, list):
        errors.append("proposed_entries: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"proposed_entries[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        entry_date = parse_date(row.get("date"), f"{ctx}.date", errors)
        if as_of and entry_date and entry_date > as_of:
            errors.append(f"{ctx}: entry date cannot be after as_of_date")
        if row.get("type") not in ENTRY_TYPES:
            errors.append(f"{ctx}: type must be one of {sorted(ENTRY_TYPES)}")
        text(row, "description", ctx, errors)
        text(row, "rationale", ctx, errors)
        string_list(row, "principles", ctx, errors)
        string_list(row, "evidence_refs", ctx, errors)
        if row.get("authorized") is not True:
            errors.append(f"{ctx}: write entry requires authorized=true")
        tag(row, ctx, errors)


def duplicate_review(data: dict, errors: list[str]) -> None:
    rows = data.get("duplicate_review")
    if not isinstance(rows, list):
        errors.append("duplicate_review: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"duplicate_review[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "fingerprint", ctx, errors)
        if not isinstance(row.get("duplicate_found"), bool):
            errors.append(f"{ctx}: duplicate_found must be boolean")
        if row.get("action") not in DEDUPE_ACTIONS:
            errors.append(f"{ctx}: action must be one of {sorted(DEDUPE_ACTIONS)}")
        if row.get("duplicate_found") is True and row.get("action") == "append":
            errors.append(f"{ctx}: duplicate entries must not be appended")
        if row.get("duplicate_found") is False and row.get("action") != "append":
            errors.append(f"{ctx}: non-duplicates should append or explain as Guardian block")
        tag(row, ctx, errors)


def ordering_review(data: dict, as_of: date | None, errors: list[str]) -> None:
    item = data.get("ordering_review")
    if not isinstance(item, dict):
        errors.append("ordering_review: must be an object")
        return
    section_date = parse_date(item.get("new_section_date"), "ordering_review.new_section_date", errors)
    if as_of and section_date and section_date > as_of:
        errors.append("ordering_review: new_section_date cannot be after as_of_date")
    if item.get("insertion_position") not in POSITIONS:
        errors.append(f"ordering_review: insertion_position must be one of {sorted(POSITIONS)}")
    if not isinstance(item.get("newest_first"), bool):
        errors.append("ordering_review: newest_first must be boolean")
    tag(item, "ordering_review", errors)


def guardian(data: dict, errors: list[str]) -> None:
    item = data.get("guardian_decision")
    if not isinstance(item, dict):
        errors.append("guardian_decision: must be an object")
        return
    if item.get("decision") not in DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(DECISIONS)}")
    text(item, "rationale", "guardian_decision", errors)
    tag(item, "guardian_decision", errors)
    if item.get("decision") == "pass":
        snapshot_item = data.get("changelog_snapshot", {})
        ordering_item = data.get("ordering_review", {})
        if snapshot_item.get("status") != "present":
            errors.append("guardian_decision: pass requires present changelog.md")
        if ordering_item.get("newest_first") is not True:
            errors.append("guardian_decision: pass requires newest_first ordering")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "changelog-management":
        errors.append("skill must be changelog-management")
    as_of = parse_date(data.get("as_of_date"), "as_of_date", errors)
    snapshot(data, errors)
    proposed_entries(data, as_of, errors)
    duplicate_review(data, errors)
    ordering_review(data, as_of, errors)
    guardian(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Changelog Management JSON report")
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
