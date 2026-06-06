#!/usr/bin/env python3
"""Validate Kata 18 persistent scratchpad reports against offline contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = ["Decisiones", "Hallazgos", "Pendientes"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FORBIDDEN = ["monologo interno", "hipotesis sin confirmar", "duda pasajera", "raw transcript"]


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


def validate_path(path: str) -> list[str]:
    errors: list[str] = []
    if not path:
        return ["scratchpad.path is required"]
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append("scratchpad.path must be safe and relative")
    if candidate.suffix != ".md":
        errors.append("scratchpad.path must end with .md")
    if candidate.name != "investigation-scratchpad.md":
        errors.append("scratchpad.path must be investigation-scratchpad.md")
    return errors


def validate_sections(sections: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(sections, dict):
        return ["scratchpad.sections must be an object"]
    if sorted(sections.keys()) != sorted(REQUIRED_SECTIONS):
        errors.append("scratchpad.sections must contain exactly Decisiones, Hallazgos, Pendientes")

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
            for field in ["text", "date", "evidence"]:
                value = entry.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{prefix}.{field} is required")
            date = entry.get("date")
            if isinstance(date, str) and not DATE_RE.match(date):
                errors.append(f"{prefix}.date must use YYYY-MM-DD")
            text = str(entry.get("text", "")).lower()
            if any(marker in text for marker in FORBIDDEN):
                errors.append(f"{prefix}.text contains forbidden scratchpad content")
            if section in {"Decisiones", "Hallazgos"} and entry.get("validated") is not True:
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
        "scratchpad.persistent_on_disk": True,
        "access_policy.read_once_at_start": True,
        "access_policy.reference_after_load": True,
        "access_policy.reread_each_turn": False,
        "write_policy.append_only": True,
        "write_policy.overwrite_existing": False,
        "write_policy.preserve_existing_entries": True,
        "exclusions.internal_monologue": False,
        "exclusions.unconfirmed_hypotheses": False,
        "exclusions.transient_doubts": False,
        "exclusions.raw_transcript": False,
        "validation.survives_compact": True,
        "validation.survives_restart": True,
        "validation.kata10_cache_safe": True,
        "validation.kata11_compaction_linked": True,
        "validation.kata19_adaptive_investigation_linked": True,
    }
    for dotted, expected in required_bools.items():
        errors.extend(require_bool(data, dotted, expected))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate katas-persistent-scratchpad report JSON")
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
