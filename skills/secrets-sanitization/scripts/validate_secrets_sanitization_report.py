#!/usr/bin/env python3
"""Validate Gate G0 secrets reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.secrets-sanitization.report.v1"
TOKEN_RE = re.compile(r"(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xoxb-[A-Za-z0-9-]{20,}|AKIA[A-Z0-9]{16})")


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
    if root.get("skill") != "secrets-sanitization":
        errors.append("skill must be secrets-sanitization")
    if root.get("gate") != "G0":
        errors.append("gate must be G0")
    scan = obj(root.get("scan"), "scan", errors)
    if not scan.get("evidence"):
        errors.append("scan.evidence is required")
    findings = arr(root.get("findings"), "findings", errors)
    critical_open = False
    unmasked = False
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        excerpt = str(finding.get("excerpt", ""))
        if TOKEN_RE.search(excerpt):
            unmasked = True
        if finding.get("value_masked") is not True and finding.get("severity") in {"high", "critical"}:
            unmasked = True
        if finding.get("severity") == "critical" and finding.get("status") != "resolved":
            critical_open = True
    decision = obj(root.get("decision"), "decision", errors)
    if (critical_open or unmasked) and root.get("status") != "blocked":
        errors.append("critical or unmasked secret findings require status blocked")
    if (critical_open or unmasked) and decision.get("next_action") != "mask-or-rotate":
        errors.append("critical or unmasked secret findings require next_action mask-or-rotate")
    if root.get("status") == "pass" and findings:
        errors.append("status pass cannot include findings")
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
