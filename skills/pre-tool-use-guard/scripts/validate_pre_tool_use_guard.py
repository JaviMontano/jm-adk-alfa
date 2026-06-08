#!/usr/bin/env python3
"""Validate pre-tool-use guard decision reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.pre-tool-use-guard.decision.v1"
DANGEROUS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bgit\s+reset\s+--hard\b",
        r"\bgit\s+clean\s+-f[dDxX]*\b",
        r"\brm\s+-rf\b",
        r"\bsudo\b",
        r"\bchmod\s+-R\s+777\b",
    ]
]
PRIVATE_MARKERS = ("user-context/jarvis-os", ".env", ".pem", ".key", "credentials")


def require_object(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(f"{name} must be an object")
    return {}


def require_list(value: Any, name: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{name} must be a list")
    return []


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def has_text(value: Any) -> bool:
    return bool(text(value).strip())


def contains_private_marker(command: str) -> bool:
    return any(marker in command for marker in PRIVATE_MARKERS)


def validate_report(report: Any) -> list[str]:
    errors: list[str] = []
    root = require_object(report, "root", errors)
    if not root:
        return errors
    if root.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if root.get("skill") != "pre-tool-use-guard":
        errors.append("skill must be pre-tool-use-guard")
    tool_call = require_object(root.get("tool_call"), "tool_call", errors)
    scope = require_object(root.get("scope"), "scope", errors)
    checks = require_object(root.get("checks"), "checks", errors)
    decision = require_object(root.get("decision"), "decision", errors)

    command = text(tool_call.get("command"))
    if tool_call.get("tool") == "Bash" and not has_text(command):
        errors.append("tool_call.command is required for Bash")
    evidence = require_list(decision.get("evidence"), "decision.evidence", errors)
    if not evidence or not all(has_text(item) for item in evidence):
        errors.append("decision.evidence must contain non-empty strings")
    action = decision.get("action")
    if action not in {"allow", "block", "require-approval"}:
        errors.append("decision.action is invalid")

    command_is_dangerous = any(pattern.search(command) for pattern in DANGEROUS)
    private_touch = contains_private_marker(command) or checks.get("private_path_touch") is True
    outside_scope = checks.get("writes_outside_scope") is True
    secret_risk = checks.get("secrets_exposure") is True
    hard_blocker = command_is_dangerous or private_touch or outside_scope or secret_risk

    if command_is_dangerous and checks.get("destructive_command") is not True:
        errors.append("checks.destructive_command must be true for destructive commands")
    if hard_blocker:
        if action != "block":
            errors.append("hard blockers require decision.action block")
        if decision.get("exit_code") != 2:
            errors.append("hard blockers require decision.exit_code 2")
    if action == "allow":
        if decision.get("exit_code") != 0:
            errors.append("allow decisions require exit_code 0")
        allowed_roots = require_list(scope.get("allowed_write_roots"), "scope.allowed_write_roots", errors)
        if checks.get("may_write") is True and not allowed_roots:
            errors.append("write-capable allow decisions require allowed_write_roots")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pre-tool-use guard decision report")
    parser.add_argument("reports", nargs="+")
    args = parser.parse_args()
    all_errors: list[str] = []
    for item in args.reports:
        path = Path(item)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            all_errors.append(f"{path}: invalid JSON: {exc}")
            continue
        for error in validate_report(data):
            all_errors.append(f"{path}: {error}")
    for error in all_errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
