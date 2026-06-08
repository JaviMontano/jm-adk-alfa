#!/usr/bin/env python3
"""Validate repository organization safety reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.repository-organization.report.v1"
SHA_RE = re.compile(r"^[A-Fa-f0-9]{64}$")
PRIVATE = ("user-context/jarvis-os", ".env", "credentials")
MANIFEST_ACTIONS = {"move", "archive", "delete", "rename"}


def obj(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(f"{name} must be an object")
    return {}


def arr(value: Any, name: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{name} must be a list")
    return []


def private_path(path: str) -> bool:
    return any(marker in path for marker in PRIVATE)


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    root = obj(report, "root", errors)
    if not root:
        return errors
    if root.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if root.get("skill") != "repository-organization":
        errors.append("skill must be repository-organization")
    scan = obj(root.get("scan"), "scan", errors)
    if not scan.get("root") or not scan.get("evidence"):
        errors.append("scan.root and scan.evidence are required")
    findings = arr(root.get("findings"), "findings", errors)
    actions = arr(root.get("actions"), "actions", errors)
    unresolved = False
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        severity = finding.get("severity")
        status = finding.get("status")
        path = str(finding.get("path", ""))
        if severity not in {"info", "warn", "error", "critical"}:
            errors.append(f"findings[{index}].severity is invalid")
        if status != "resolved" and severity in {"error", "critical"}:
            unresolved = True
        if private_path(path) and finding.get("handling") not in {"inventory-only", "excluded"}:
            errors.append(f"findings[{index}] private path must be inventory-only or excluded")
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            errors.append(f"actions[{index}] must be an object")
            continue
        action_name = action.get("action")
        source = str(action.get("source_path", ""))
        destination = str(action.get("destination_path", ""))
        if private_path(source) or private_path(destination):
            errors.append(f"actions[{index}] references private path")
        if action_name in MANIFEST_ACTIONS:
            if not action.get("manifest_path"):
                errors.append(f"actions[{index}] requires manifest_path")
            if not SHA_RE.match(str(action.get("sha256", ""))):
                errors.append(f"actions[{index}] requires sha256")
    decision = obj(root.get("decision"), "decision", errors)
    if root.get("clean_claim") is True and unresolved:
        errors.append("clean_claim cannot be true with unresolved error or critical findings")
    if root.get("clean_claim") is True and decision.get("validated") is not True:
        errors.append("clean_claim requires decision.validated true")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+")
    args = parser.parse_args()
    errors: list[str] = []
    for report in args.reports:
        path = Path(report)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        errors.extend(f"{path}: {error}" for error in validate(data))
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
