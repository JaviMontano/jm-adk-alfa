#!/usr/bin/env python3
"""Validate persistent-memory-design reports against offline contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = ["Hypotheses", "Decisions", "Findings", "Open"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FORBIDDEN_MARKERS = [
    "raw transcript",
    "raw tool dump",
    "chain-of-thought",
    "unverified tool output",
]


def load_json(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except Exception as exc:  # noqa: BLE001
        return None, [f"invalid JSON: {exc}"]


def require_bool(data: dict, dotted: str, expected: bool) -> list[str]:
    current: object = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return [f"missing boolean: {dotted}"]
        current = current[part]
    if current is not expected:
        return [f"{dotted} must be {expected}"]
    return []


def validate_path(path: str) -> list[str]:
    errors: list[str] = []
    if not path:
        return ["scratchpad.path is required"]
    candidate = Path(path)
    if candidate.is_absolute():
        errors.append("scratchpad.path must be relative")
    if ".." in candidate.parts:
        errors.append("scratchpad.path must not contain parent traversal")
    if not path.startswith(".agent/"):
        errors.append("scratchpad.path must start with .agent/")
    if candidate.suffix != ".md":
        errors.append("scratchpad.path must end with .md")
    return errors


def validate_sections(sections: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(sections, dict):
        return ["scratchpad.sections must be an object"]

    keys = sorted(sections.keys())
    if keys != sorted(REQUIRED_SECTIONS):
        errors.append("scratchpad.sections must contain exactly Hypotheses, Decisions, Findings, Open")

    for section in REQUIRED_SECTIONS:
        entries = sections.get(section)
        if not isinstance(entries, list):
            errors.append(f"{section} must be a list")
            continue
        for index, entry in enumerate(entries):
            prefix = f"{section}[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for field in ["text", "source", "date"]:
                value = entry.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{prefix}.{field} is required")
            date = entry.get("date")
            if isinstance(date, str) and not DATE_RE.match(date):
                errors.append(f"{prefix}.date must use YYYY-MM-DD")
            text = str(entry.get("text", "")).lower()
            if any(marker in text for marker in FORBIDDEN_MARKERS):
                errors.append(f"{prefix}.text contains forbidden raw-memory marker")
            if section in {"Decisions", "Findings"} and entry.get("validated") is not True:
                errors.append(f"{prefix}.validated must be true")
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

    scratchpad = data.get("scratchpad")
    if not isinstance(scratchpad, dict):
        errors.append("scratchpad must be an object")
    else:
        errors.extend(validate_path(str(scratchpad.get("path", ""))))
        errors.extend(validate_sections(scratchpad.get("sections")))

    required_bools = {
        "access_policy.read_once": True,
        "access_policy.reference_after_bootstrap": True,
        "access_policy.reread_each_turn": False,
        "write_policy.full_rewrite_allowed": False,
        "write_policy.idempotent_upsert": True,
        "compact_recovery.reconstruct_from_file_only": True,
        "compact_recovery.conversation_dependency": False,
        "exclusions.raw_transcript": False,
        "exclusions.raw_tool_dump": False,
        "exclusions.chain_of_thought": False,
        "validation.survives_compact": True,
        "validation.read_once_verified": True,
        "validation.evidence_checked": True,
    }
    for dotted, expected in required_bools.items():
        errors.extend(require_bool(data, dotted, expected))

    write_policy = data.get("write_policy")
    if not isinstance(write_policy, dict):
        errors.append("write_policy must be an object")
    elif write_policy.get("mode") != "append_or_upsert":
        errors.append("write_policy.mode must be append_or_upsert")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate persistent memory design report JSON")
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
