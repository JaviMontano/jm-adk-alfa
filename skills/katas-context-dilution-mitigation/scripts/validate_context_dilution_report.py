#!/usr/bin/env python3
"""Validate context dilution mitigation reports against offline contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PRESERVE_REQUIRED = {"rules", "decisions", "escalations"}


def load_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"invalid JSON: {exc}"]


def bool_at(data: dict, dotted: str) -> object:
    current: object = data
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def require_bool(data: dict, dotted: str, expected: bool) -> list[str]:
    actual = bool_at(data, dotted)
    if actual is not expected:
        return [f"{dotted} must be {expected}"]
    return []


def validate_report(path: Path) -> list[str]:
    data, errors = load_json(path)
    if errors:
        return errors
    if not isinstance(data, dict):
        return ["report root must be an object"]

    errors = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")

    critical_rules = data.get("critical_rules")
    if not isinstance(critical_rules, list) or not critical_rules:
        errors.append("critical_rules must be a non-empty list")

    errors.extend(require_bool(data, "placement.rules_at_start", True))
    errors.extend(require_bool(data, "placement.rules_repeated_at_end", True))
    if bool_at(data, "placement.bulk_context_position") != "middle":
        errors.append("placement.bulk_context_position must be middle")
    errors.extend(require_bool(data, "placement.middle_only_critical_rules", False))

    threshold = bool_at(data, "usage.threshold")
    fraction = bool_at(data, "usage.fraction")
    compaction_required = bool_at(data, "usage.compaction_required")
    if not isinstance(threshold, (int, float)) or not 0.5 <= float(threshold) <= 0.6:
        errors.append("usage.threshold must be between 0.5 and 0.6")
    if not isinstance(fraction, (int, float)) or not 0 <= float(fraction) <= 1:
        errors.append("usage.fraction must be between 0 and 1")
    if isinstance(threshold, (int, float)) and isinstance(fraction, (int, float)):
        should_compact = float(fraction) > float(threshold)
        if compaction_required is not should_compact:
            errors.append("usage.compaction_required must match fraction > threshold")

    compaction = data.get("compaction")
    if not isinstance(compaction, dict):
        errors.append("compaction must be an object")
    else:
        preserve = compaction.get("preserve")
        if not isinstance(preserve, list) or not PRESERVE_REQUIRED.issubset(set(preserve)):
            errors.append("compaction.preserve must include rules, decisions, escalations")
        errors.extend(require_bool(data, "compaction.drops_critical_rules", False))
        errors.extend(require_bool(data, "compaction.condenses_not_deletes", True))

    for dotted in [
        "validation.lost_in_middle_addressed",
        "validation.edge_placement_verified",
        "validation.threshold_in_50_60",
        "validation.preservation_verified",
    ]:
        errors.extend(require_bool(data, dotted, True))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate context dilution mitigation report JSON")
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
