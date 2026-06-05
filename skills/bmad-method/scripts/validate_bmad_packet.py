#!/usr/bin/env python3
"""Validate deterministic BMAD method packets."""

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

    if scenario == "greenfield":
        for required in ["Phase 1", "product-brief.md", "PRD.md", "architecture.md", "stories/*.md"]:
            if required not in text:
                errors.append(f"greenfield missing: {required}")
        if "immediate code" in lowered:
            errors.append("greenfield cannot jump to immediate code")
    elif scenario == "gate-fail":
        if "FAIL" not in sections.get("Readiness Gate", ""):
            errors.append("gate-fail scenario must include FAIL")
        if "Phase 4 approved" in text or "Implementation may begin" in text:
            errors.append("gate-fail scenario cannot approve Phase 4")
    elif scenario == "quick-flow":
        for required in ["Barry", "triage", "rapid spec", "test or self-review"]:
            if required not in text:
                errors.append(f"quick-flow missing: {required}")
        if "full PRD" in lowered:
            errors.append("quick-flow must not require full PRD")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate BMAD method packet")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--scenario", choices=["greenfield", "gate-fail", "quick-flow"], required=True)
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
