#!/usr/bin/env python3
"""Validate deterministic DSVSR packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def markdown_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def validate_packet(contract: dict, text: str, scenario: str) -> list[str]:
    errors: list[str] = []
    sections = markdown_sections(text)
    lowered = text.lower()

    for section in contract["required_sections"]:
        if section not in sections:
            errors.append(f"missing section: {section}")
        elif not sections[section]:
            errors.append(f"empty section: {section}")

    if not any(tag in text for tag in contract["allowed_evidence_tags"]):
        errors.append("missing evidence tag")

    for phrase in contract.get("blocked_phrases", []):
        if phrase.lower() in lowered:
            errors.append(f"blocked phrase present: {phrase}")

    for required in ["Global confidence", "Sources reviewed", "Information gaps"]:
        if required not in sections.get("Reasoning Metadata", ""):
            errors.append(f"metadata missing: {required}")

    if scenario == "full-dsvsr":
        for required in ["SP-1", "SP-2", "Confidence:", "LOGIC", "FACTS", "Global confidence: 0.86"]:
            if required not in text:
                errors.append(f"full-dsvsr missing: {required}")
    elif scenario == "missing-context":
        for required in ["[OPEN]", "core problem", "clarify", "Global confidence: 0.00"]:
            if required not in text:
                errors.append(f"missing-context missing: {required}")
    elif scenario == "low-confidence":
        for required in ["below target", "weakest sub-problem", "missing evidence", "not executive"]:
            if required not in lowered:
                errors.append(f"low-confidence missing: {required}")
    elif scenario == "false-positive":
        if "expected_activation: false" not in text:
            errors.append("false-positive must mark expected_activation: false")
        if "Full DSVSR" in text:
            errors.append("false-positive must not run full DSVSR")
    elif scenario == "invalid-no-verify":
        if sections.get("Verify", "").strip():
            errors.append("invalid-no-verify fixture unexpectedly has Verify content")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DSVSR packet")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument(
        "--scenario",
        choices=["full-dsvsr", "missing-context", "low-confidence", "false-positive", "invalid-no-verify"],
        required=True,
    )
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        text = args.packet.read_text(encoding="utf-8")
        errors = validate_packet(contract, text, args.scenario)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    status = "fail" if errors else "pass"
    print(json.dumps({"status": status, "errors": errors}, indent=2, ensure_ascii=False))
    if args.expect:
        if status != args.expect:
            print(f"ERROR: expected {args.expect}, observed {status}", file=sys.stderr)
            return 1
        return 0
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
