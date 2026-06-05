#!/usr/bin/env python3
"""Validate deterministic triad composition packets."""

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

    selected = sections.get("Selected Triad", "")
    classification = sections.get("Input Classification", "")
    execution = sections.get("Execution Mode", "")
    validation = sections.get("Validation Gates", "")

    if "guardian" not in selected.lower():
        errors.append("selected triad must name guardian")
    if "G0" not in validation or "G3" not in validation:
        errors.append("validation gates must include G0 through G3")

    if scenario == "requirements":
        for required in ["Requirements", "requirements-analyst", "domain-modeler", "quality-guardian", "0.85"]:
            if required not in text:
                errors.append(f"requirements scenario missing: {required}")
    elif scenario == "ambiguous":
        for required in ["0.60-0.84", "top 3", "needs_disambiguation"]:
            if required not in text:
                errors.append(f"ambiguous scenario missing: {required}")
        if "Execute sequentially" in execution:
            errors.append("ambiguous scenario must not execute")
    elif scenario == "missing-context":
        for required in ["Goal", "Context", "Constraints", "Definition of done", "[OPEN]"]:
            if required not in text:
                errors.append(f"missing-context scenario missing: {required}")
        if "auto_select" in classification:
            errors.append("missing-context scenario must not auto-select")
    elif scenario == "false-positive":
        if "expected_activation: false" not in text:
            errors.append("false-positive scenario must mark expected_activation: false")
        if any(agent in text for agent in ["requirements-analyst", "frontend-craftsman", "quality-guardian"]):
            errors.append("false-positive scenario must not return orchestration triad agents")
    elif scenario == "invalid-no-guardian":
        if "guardian" in selected.lower():
            errors.append("invalid-no-guardian fixture unexpectedly names guardian")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate triad composition packet")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument(
        "--scenario",
        choices=["requirements", "ambiguous", "missing-context", "false-positive", "invalid-no-guardian"],
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
