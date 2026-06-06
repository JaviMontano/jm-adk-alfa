#!/usr/bin/env python3
"""Validate deterministic Workspace Governance JSON reports."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.workspace-governance.report.v1"
REQUIRED_TOP = {"schema", "skill", "workspace_root", "gitignore", "directories", "sessions", "task_bridges", "actions", "validation"}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
DIR_TYPES = {"root", "tasks", "estandares", "session", "task_bridge"}
ACTIONS = {"create", "create_readme", "update_gitignore", "create_task_bridge", "flag_stale", "no_op"}
CHECKS = {"assets", "deterministic_scripts", "quality_criteria", "gitignore_policy", "session_contract", "task_bridge_contract", "stale_review", "evidence_required"}
SESSION_RE = re.compile(r"^workspace/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+/$")
BRIDGE_RE = re.compile(r"^workspace/tasks/TL-[0-9]{3}-[a-z0-9-]+/$")


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


def tag(obj: dict[str, Any], ctx: str, errors: list[str]) -> None:
    require(obj.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")


def text(obj: dict[str, Any], key: str, ctx: str, errors: list[str]) -> None:
    require(isinstance(obj.get(key), str) and bool(obj[key].strip()), errors, f"{ctx}.{key} required")


def validate_gitignore(data: dict[str, Any], errors: list[str]) -> None:
    item = data.get("gitignore")
    require(isinstance(item, dict), errors, "gitignore must be object")
    if not isinstance(item, dict):
        return
    require(item.get("workspace_ignored") is True, errors, "gitignore.workspace_ignored must be true")
    text(item, "source", "gitignore", errors)
    tag(item, "gitignore", errors)


def validate_directories(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("directories"), "directories", errors)
    require(bool(rows), errors, "directories required")
    for i, row in enumerate(rows):
        ctx = f"directories[{i}]"
        path = row.get("path")
        require(isinstance(path, str) and path.startswith("workspace/"), errors, f"{ctx}.path must start with workspace/")
        require(row.get("type") in DIR_TYPES, errors, f"{ctx}.type invalid")
        require(row.get("has_readme") is True, errors, f"{ctx}.has_readme must be true")
        tag(row, ctx, errors)


def validate_sessions(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("sessions"), "sessions", errors)
    for i, row in enumerate(rows):
        ctx = f"sessions[{i}]"
        path = row.get("path")
        require(isinstance(path, str) and bool(SESSION_RE.match(path)), errors, f"{ctx}.path invalid session format")
        require(row.get("has_readme") is True, errors, f"{ctx}.has_readme must be true")
        age = row.get("age_days")
        require(isinstance(age, int) and age >= 0, errors, f"{ctx}.age_days must be non-negative integer")
        require(isinstance(row.get("stale_review_required"), bool), errors, f"{ctx}.stale_review_required must be boolean")
        if isinstance(age, int) and age > 30:
            require(row.get("stale_review_required") is True, errors, f"{ctx}: sessions older than 30 days require stale review")
        tag(row, ctx, errors)


def validate_task_bridges(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("task_bridges"), "task_bridges", errors)
    for i, row in enumerate(rows):
        ctx = f"task_bridges[{i}]"
        path = row.get("path")
        task_id = row.get("task_id")
        require(isinstance(task_id, str) and bool(re.match(r"^TL-[0-9]{3}$", task_id)), errors, f"{ctx}.task_id invalid")
        require(isinstance(path, str) and bool(BRIDGE_RE.match(path)), errors, f"{ctx}.path invalid bridge format")
        require(row.get("matches_tasklog") is True, errors, f"{ctx}.matches_tasklog must be true")
        require(row.get("has_readme") is True, errors, f"{ctx}.has_readme must be true")
        tag(row, ctx, errors)


def validate_actions(data: dict[str, Any], errors: list[str]) -> None:
    rows = objects(data.get("actions"), "actions", errors)
    for i, row in enumerate(rows):
        ctx = f"actions[{i}]"
        target = row.get("target")
        require(row.get("action") in ACTIONS, errors, f"{ctx}.action invalid")
        require(isinstance(target, str) and (target.startswith("workspace/") or target == ".gitignore"), errors, f"{ctx}.target must be workspace/ or .gitignore")
        require(row.get("tracked") is False, errors, f"{ctx}.tracked must be false")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


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
    require(data.get("skill") == "workspace-governance", errors, "skill must be workspace-governance")
    require(data.get("workspace_root") == "workspace/", errors, "workspace_root must be workspace/")
    validate_gitignore(data, errors)
    validate_directories(data, errors)
    validate_sessions(data, errors)
    validate_task_bridges(data, errors)
    validate_actions(data, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_workspace_governance_report.py <report.json>", file=sys.stderr)
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
