#!/usr/bin/env python3
"""Validate structure audit reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.validate-structure.report.v1"
PRIVATE = ("user-context/jarvis-os", ".env", "credentials")
TRANSIENT = ("workspace/", ".local/tmp/")


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


def sensitive(path: str) -> bool:
    return any(marker in path for marker in PRIVATE) or any(path.startswith(marker) for marker in TRANSIENT)


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    root = obj(report, "root", errors)
    if not root:
        return errors
    if root.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if root.get("skill") != "validate-structure":
        errors.append("skill must be validate-structure")
    validation = obj(root.get("validation"), "validation", errors)
    findings = arr(root.get("findings"), "findings", errors)
    unresolved_critical = False
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        severity = finding.get("severity")
        status = finding.get("status")
        path = str(finding.get("path", ""))
        handling = finding.get("handling")
        if severity not in {"info", "warn", "error", "critical"}:
            errors.append(f"findings[{index}].severity is invalid")
        if severity == "critical" and status != "resolved":
            unresolved_critical = True
        if sensitive(path) and handling not in {"excluded", "inventory-only", "blocked"}:
            errors.append(f"findings[{index}] sensitive path must be excluded, inventory-only, or blocked")
    if root.get("clean_claim") is True:
        if validation.get("status") != "pass" or not validation.get("evidence"):
            errors.append("clean_claim requires passing validation evidence")
        if unresolved_critical:
            errors.append("clean_claim cannot be true with unresolved critical findings")
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
