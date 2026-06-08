#!/usr/bin/env python3
"""Validate post-tool-use reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.post-tool-use-validator.report.v1"
SECRET_RE = re.compile(r"(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xoxb-[A-Za-z0-9-]{20,}|AKIA[A-Z0-9]{16})")
PRIVATE_MARKERS = ("user-context/jarvis-os", ".env", "credentials")
STATUSES = {"pass", "warn", "fail", "blocked"}
NEXT_ACTIONS = {"proceed", "retry", "block", "document-risk"}


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


def validate_report(report: Any) -> list[str]:
    errors: list[str] = []
    root = require_object(report, "root", errors)
    if not root:
        return errors
    if root.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if root.get("skill") != "post-tool-use-validator":
        errors.append("skill must be post-tool-use-validator")
    result = require_object(root.get("tool_result"), "tool_result", errors)
    claim = require_object(root.get("claim"), "claim", errors)
    checks = require_object(root.get("checks"), "checks", errors)
    decision = require_object(root.get("decision"), "decision", errors)

    status = decision.get("status")
    if status not in STATUSES:
        errors.append("decision.status is invalid")
    if decision.get("next_action") not in NEXT_ACTIONS:
        errors.append("decision.next_action is invalid")
    if not has_text(decision.get("reason")):
        errors.append("decision.reason is required")

    exit_code = result.get("exit_code")
    if not isinstance(exit_code, int):
        errors.append("tool_result.exit_code must be an integer")
    command_succeeded = exit_code == 0
    if checks.get("command_succeeded") is not command_succeeded:
        errors.append("checks.command_succeeded must match tool_result.exit_code")
    if not command_succeeded and status == "pass":
        errors.append("failed command cannot have decision.status pass")

    evidence_tags = require_list(claim.get("evidence_tags"), "claim.evidence_tags", errors)
    quality_gates = require_list(checks.get("quality_gates"), "checks.quality_gates", errors)
    if status == "pass":
        if checks.get("evidence_present") is not True:
            errors.append("pass requires checks.evidence_present true")
        if not evidence_tags:
            errors.append("pass requires at least one evidence tag")
        if not quality_gates:
            errors.append("pass requires quality gates")
    for index, gate in enumerate(quality_gates):
        if not isinstance(gate, dict):
            errors.append(f"checks.quality_gates[{index}] must be an object")
            continue
        if gate.get("status") not in STATUSES:
            errors.append(f"checks.quality_gates[{index}].status is invalid")
        if gate.get("status") in {"fail", "blocked"} and status == "pass":
            errors.append("failed or blocked quality gate cannot have decision.status pass")

    combined_output = "\n".join([text(result.get("stdout_excerpt")), text(result.get("stderr_excerpt"))])
    secret_exposed = bool(SECRET_RE.search(combined_output)) or checks.get("output_contains_secret") is True
    private_exposed = any(marker in combined_output for marker in PRIVATE_MARKERS) or checks.get("private_output") is True
    if secret_exposed or private_exposed:
        if status != "blocked":
            errors.append("secret or private output exposure requires decision.status blocked")
        if decision.get("next_action") != "block":
            errors.append("secret or private output exposure requires decision.next_action block")
    if checks.get("writes_outside_scope") is True and status == "pass":
        errors.append("out-of-scope writes cannot have decision.status pass")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate post-tool-use report")
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
