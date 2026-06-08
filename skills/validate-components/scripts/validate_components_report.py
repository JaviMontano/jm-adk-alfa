#!/usr/bin/env python3
"""Validate component audit reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.validate-components.report.v1"
REQUIRED_COUNTS = ("skills", "agents", "commands", "prompts", "components")
PRIVATE = ("user-context/jarvis-os", ".env", "credentials")


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


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    root = obj(report, "root", errors)
    if not root:
        return errors
    if root.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if root.get("skill") != "validate-components":
        errors.append("skill must be validate-components")
    counts = obj(root.get("counts"), "counts", errors)
    for key in REQUIRED_COUNTS:
        if not isinstance(counts.get(key), int) or counts.get(key) < 0:
            errors.append(f"counts.{key} must be a non-negative integer")
    validation = obj(root.get("validation"), "validation", errors)
    if root.get("status") == "pass":
        if root.get("docs_aligned") is not True:
            errors.append("status pass requires docs_aligned true")
        if validation.get("status") != "pass" or not validation.get("evidence"):
            errors.append("status pass requires validation evidence")
    for index, finding in enumerate(arr(root.get("findings"), "findings", errors)):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        severity = finding.get("severity")
        path = str(finding.get("path", ""))
        if any(marker in path for marker in PRIVATE):
            errors.append(f"findings[{index}] references private path")
        if severity in {"error", "critical"} and root.get("status") == "pass":
            errors.append("status pass cannot include error or critical findings")
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
