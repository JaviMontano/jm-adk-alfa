#!/usr/bin/env python3
"""Validate User Representative Markdown review packets."""

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


def extract_scores(text: str, dimensions: list[str]) -> dict[str, int]:
    scores: dict[str, int] = {}
    for dimension in dimensions:
        pattern = rf"\|\s*{re.escape(dimension)}\s*\|\s*(\d{{1,2}})\s*/\s*10\s*\|"
        match = re.search(pattern, text)
        if match:
            scores[dimension] = int(match.group(1))
    return scores


def expected_verdict(scores: dict[str, int]) -> str:
    values = list(scores.values())
    if any(score < 5 for score in values):
        return "FAIL"
    marginal = sum(1 for score in values if 5 <= score <= 6)
    if marginal >= 3:
        return "FAIL"
    if marginal:
        return "CONDITIONAL"
    return "PASS"


def observed_verdict(text: str) -> str | None:
    match = re.search(r"\bVerdict\s*:\s*(PASS|CONDITIONAL|FAIL)\b", text)
    return match.group(1) if match else None


def validate(contract: dict, review_path: Path) -> list[str]:
    text = review_path.read_text(encoding="utf-8")
    errors: list[str] = []

    found_sections = markdown_sections(text)
    for section in contract["required_sections"]:
        if section not in found_sections:
            errors.append(f"missing section: {section}")

    allowed_tags = list(contract["allowed_evidence_tags"])
    if not any(tag in text for tag in allowed_tags):
        errors.append("missing allowed evidence tag")
    for blocked in contract.get("blocked_evidence_tags", []):
        if blocked in text:
            errors.append(f"blocked evidence tag present: {blocked}")

    dimensions = list(contract["dimensions"])
    scores = extract_scores(text, dimensions)
    missing_scores = [dimension for dimension in dimensions if dimension not in scores]
    for dimension in missing_scores:
        errors.append(f"missing score row: {dimension}")
    for dimension, score in sorted(scores.items()):
        if not 0 <= score <= 10:
            errors.append(f"score out of range for {dimension}: {score}")

    minimum_adjustments = int(contract.get("minimum_micro_adjustments", 5))
    adjustment_ids = sorted(set(re.findall(r"\bMA-\d+\b", text)))
    if len(adjustment_ids) < minimum_adjustments:
        errors.append(f"expected at least {minimum_adjustments} micro-adjustments, found {len(adjustment_ids)}")

    if len(scores) == len(dimensions):
        expected = expected_verdict(scores)
        observed = observed_verdict(text)
        if observed is None:
            errors.append("missing verdict line")
        elif observed != expected:
            errors.append(f"verdict mismatch: expected {expected}, observed {observed}")

    for forbidden in contract.get("must_not_include", []):
        if forbidden in text:
            errors.append(f"forbidden unsupported claim present: {forbidden}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a User Representative Markdown review")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        errors = validate(contract, args.review)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    status = "fail" if errors else "pass"
    print(json.dumps({"status": status, "errors": errors}, indent=2, ensure_ascii=False))
    if args.expect and status != args.expect:
        print(f"ERROR: expected {args.expect}, observed {status}", file=sys.stderr)
        return 1
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
