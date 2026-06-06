#!/usr/bin/env python3
"""Validate input-analysis reports against offline contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_TAGS = {"CODE", "CONFIG", "DOC", "INFERENCE", "ASSUMPTION"}
ALLOWED_TYPES = {"requirement", "constraint", "contradiction", "gap", "ambiguity", "risk"}


def load_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"invalid JSON: {exc}"]


def require_bool(data: dict, dotted: str, expected: bool) -> list[str]:
    current: object = data
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return [f"{dotted} must be {expected}"]
        current = current.get(part)
    if current is not expected:
        return [f"{dotted} must be {expected}"]
    return []


def validate_findings(findings: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(findings, list) or not findings:
        return ["findings must be a non-empty list"]
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if finding.get("type") not in ALLOWED_TYPES:
            errors.append(f"{prefix}.type is invalid")
        if finding.get("evidence_tag") not in ALLOWED_TAGS:
            errors.append(f"{prefix}.evidence_tag is invalid")
        for field in ["text", "evidence", "action"]:
            value = finding.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} is required")
    return errors


def validate_report(path: Path) -> list[str]:
    data, errors = load_json(path)
    if errors:
        return errors
    if not isinstance(data, dict):
        return ["report root must be an object"]
    errors = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if not isinstance(data.get("input_type"), str) or not data["input_type"].strip():
        errors.append("input_type is required")
    errors.extend(validate_findings(data.get("findings")))

    completeness = data.get("completeness")
    if not isinstance(completeness, dict):
        errors.append("completeness must be an object")
    else:
        score = completeness.get("score")
        if not isinstance(score, int) or not 0 <= score <= 100:
            errors.append("completeness.score must be an integer between 0 and 100")
        ratio = completeness.get("assumption_ratio")
        warning = completeness.get("warning_banner")
        if not isinstance(ratio, (int, float)) or not 0 <= float(ratio) <= 1:
            errors.append("completeness.assumption_ratio must be between 0 and 1")
        elif float(ratio) > 0.3 and warning is not True:
            errors.append("warning_banner is required when assumption_ratio exceeds 0.3")

    if not isinstance(data.get("evidence_tag_summary"), dict):
        errors.append("evidence_tag_summary must be an object")

    for dotted in [
        "validation.all_findings_tagged",
        "validation.firebase_feasibility_assessed",
        "validation.phase_separation",
        "validation.actionable_recommendations",
    ]:
        errors.extend(require_bool(data, dotted, True))
    errors.extend(require_bool(data, "validation.includes_implementation_details", False))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate input-analysis report JSON")
    parser.add_argument("reports", nargs="+", help="Report JSON file(s)")
    args = parser.parse_args()

    failed = False
    for report in args.reports:
        path = Path(report)
        errors = validate_report(path)
        if errors:
            failed = True
            print(f"report={path.name} status=fail errors={len(errors)}")
            for error in errors:
                print(f"ERROR: {error}")
        else:
            print(f"report={path.name} status=pass errors=0")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
