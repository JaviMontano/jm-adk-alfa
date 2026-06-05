#!/usr/bin/env python3
"""Validate UX Writing Markdown audit packets."""

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


def markdown_sections(text: str) -> set[str]:
    sections: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            sections.add(match.group(1).strip())
    return sections


def after_column_values(text: str) -> list[str]:
    values: list[str] = []
    for line in text.splitlines():
        if not line.startswith("| RW-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 4:
            values.append(cells[3])
    return values


def contains_forbidden_claim(text: str, claim: str) -> bool:
    escaped = re.escape(claim)
    if re.fullmatch(r"[A-Za-z0-9]+", claim):
        return bool(re.search(rf"\b{escaped}\b", text, flags=re.IGNORECASE))
    return bool(re.search(escaped, text, flags=re.IGNORECASE))


def validate(contract: dict, packet_path: Path) -> list[str]:
    text = packet_path.read_text(encoding="utf-8")
    errors: list[str] = []

    sections = markdown_sections(text)
    for section in contract["required_sections"]:
        if section not in sections:
            errors.append(f"missing section: {section}")

    allowed_tags = list(contract["allowed_evidence_tags"])
    if not any(tag in text for tag in allowed_tags):
        errors.append("missing allowed evidence tag")
    for blocked in contract.get("blocked_evidence_tags", []):
        if blocked in text:
            errors.append(f"blocked evidence tag present: {blocked}")

    rewrite_ids = sorted(set(re.findall(r"\bRW-\d+\b", text)))
    minimum_rewrites = int(contract.get("minimum_rewrites", 3))
    if len(rewrite_ids) < minimum_rewrites:
        errors.append(f"expected at least {minimum_rewrites} rewrites, found {len(rewrite_ids)}")

    after_values = after_column_values(text)
    blocked_phrases = list(contract.get("blocked_after_phrases", []))
    for value in after_values:
        for blocked in blocked_phrases:
            if blocked.lower() == value.lower():
                errors.append(f"blocked after-copy phrase present: {blocked}")

    for claim in contract.get("forbidden_claims", []):
        if contains_forbidden_claim(text, claim):
            errors.append(f"forbidden unsupported claim present: {claim}")

    if "Before" not in text or "After" not in text:
        errors.append("missing before/after rewrite table")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a UX Writing Audit Markdown packet")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        errors = validate(contract, args.packet)
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
