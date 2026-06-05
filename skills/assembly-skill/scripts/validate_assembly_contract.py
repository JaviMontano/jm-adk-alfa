#!/usr/bin/env python3
"""Validate assembly-skill mode selection and report contracts."""

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


def observed_field(text: str, field: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(field)}:\*\*\s*(.+?)\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def select_mode(scorecard: dict) -> str:
    explicit = scorecard.get("requested_mode")
    if explicit:
        return str(explicit)
    if scorecard.get("context_pressure"):
        return "standard"
    score = float(scorecard.get("score", 0))
    gate_passed = bool(scorecard.get("gate_passed", False))
    user_requested_changes = bool(scorecard.get("user_requested_changes", False))
    if score < 5:
        return "standard"
    if score < 7:
        return "standard"
    if score < 8:
        return "deep"
    if gate_passed and not user_requested_changes:
        return "quick"
    return "standard"


def validate_report(contract: dict, report_path: Path, mode: str) -> list[str]:
    text = report_path.read_text(encoding="utf-8")
    lowered = text.lower()
    sections = markdown_sections(text)
    errors: list[str] = []

    for section in contract["required_sections"]:
        if section not in sections:
            errors.append(f"missing section: {section}")
        elif not sections[section]:
            errors.append(f"empty section: {section}")

    observed_mode = observed_field(text, "Mode")
    if observed_mode != mode:
        errors.append(f"mode mismatch: expected {mode}, observed {observed_mode}")

    result = observed_field(text, "Result")
    if result not in contract["allowed_results"]:
        errors.append(f"invalid result: {result}")

    if not any(tag in text for tag in contract["allowed_evidence_tags"]):
        errors.append("missing evidence tag")

    for phrase in contract.get("blocked_phrases", []):
        if phrase.lower() in lowered:
            errors.append(f"blocked phrase present: {phrase}")

    mode_contract = contract["mode_requirements"][mode]
    for item in mode_contract.get("must_include", []):
        if item not in text:
            errors.append(f"mode {mode} missing required text: {item}")
    for item in mode_contract.get("must_not_include", []):
        if item in text:
            errors.append(f"mode {mode} includes forbidden text: {item}")

    if mode in {"standard", "deep"} and "Gate B" not in text:
        errors.append(f"mode {mode} must record Gate B")
    if result == "CERTIFIED" and "Formula Source" not in text:
        errors.append("CERTIFIED result requires Formula Source")
    if "Files Modified" in sections and mode in {"standard", "deep"}:
        if "No files modified" in sections["Files Modified"]:
            errors.append(f"mode {mode} cannot claim no files modified")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate assembly-skill contracts")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--mode", choices=["quick", "standard", "deep"])
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--scorecard", type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    parser.add_argument("--expect-mode", choices=["quick", "standard", "deep"])
    args = parser.parse_args()

    try:
        errors: list[str] = []
        payload: dict[str, object] = {}
        if args.scorecard:
            scorecard = load_json(args.scorecard)
            if args.policy:
                load_json(args.policy)
            mode = select_mode(scorecard)
            payload["mode"] = mode
            if args.expect_mode and mode != args.expect_mode:
                errors.append(f"mode mismatch: expected {args.expect_mode}, observed {mode}")
        if args.report:
            if not args.contract or not args.mode:
                raise ValueError("--report requires --contract and --mode")
            contract = load_json(args.contract)
            errors.extend(validate_report(contract, args.report, args.mode))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    status = "fail" if errors else "pass"
    payload.update({"status": status, "errors": errors})
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    if args.expect:
        if status != args.expect:
            print(f"ERROR: expected {args.expect}, observed {status}", file=sys.stderr)
            return 1
        return 0
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
