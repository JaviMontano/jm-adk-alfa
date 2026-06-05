#!/usr/bin/env python3
"""Validate Prompt Forge JSON packets deterministically."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "assets" / "playbook-contract.json"

BANNED_PATTERNS = [
    re.compile(r"reveal hidden reasoning", re.IGNORECASE),
    re.compile(r"show hidden reasoning", re.IGNORECASE),
    re.compile(r"hidden chain-of-thought transcript", re.IGNORECASE),
    re.compile(r"secretly use outside knowledge", re.IGNORECASE),
    re.compile(r"invent citations", re.IGNORECASE),
]


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def as_list(value: object) -> list:
    return value if isinstance(value, list) else []


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate_packet(packet: dict, contract: dict) -> list[str]:
    errors: list[str] = []
    modes = set(contract["modes"])
    platforms = set(contract["target_platforms"])
    sections = set(contract["playbook_sections"])
    criteria = set(contract["rubric_criteria"])
    test_types = set(contract["required_test_types"])

    require(packet.get("mode") in modes, errors, "mode must be a supported Prompt Forge mode")
    require(packet.get("target_platform") in platforms, errors, "target_platform must be supported or unknown")

    source = packet.get("source_boundary")
    require(isinstance(source, dict), errors, "source_boundary must be an object")
    if isinstance(source, dict):
        require(bool(as_list(source.get("allowed_sources"))), errors, "source_boundary.allowed_sources is required")
        unsupported = str(source.get("unsupported_behavior", "")).lower()
        require(
            "coverage_gap" in unsupported or "refuse" in unsupported,
            errors,
            "source_boundary.unsupported_behavior must include coverage_gap or refusal",
        )

    playbook = packet.get("playbook")
    require(isinstance(playbook, dict), errors, "playbook must be an object")
    if isinstance(playbook, dict):
        missing = sorted(sections - set(playbook))
        require(not missing, errors, f"playbook missing sections: {', '.join(missing)}")

    constraints = " ".join(str(x).lower() for x in as_list(packet.get("constraints")))
    require("invent" in constraints or "unsupported" in constraints, errors, "constraints must include no-invention control")
    require("hidden reasoning" in constraints or "concise rationale" in constraints, errors, "constraints must protect hidden reasoning")

    output_contract = packet.get("output_contract")
    require(isinstance(output_contract, dict), errors, "output_contract must be an object")
    if isinstance(output_contract, dict):
        require(bool(str(output_contract.get("format", "")).strip()), errors, "output_contract.format is required")
        require(bool(as_list(output_contract.get("required_fields"))), errors, "output_contract.required_fields is required")

    rubric = as_list(packet.get("rubric_scores"))
    seen = {str(item.get("criterion", "")) for item in rubric if isinstance(item, dict)}
    missing_criteria = sorted(criteria - seen)
    require(not missing_criteria, errors, f"rubric_scores missing criteria: {', '.join(missing_criteria)}")
    for item in rubric:
        if not isinstance(item, dict):
            errors.append("rubric_scores entries must be objects")
            continue
        score = item.get("score")
        require(isinstance(score, int) and 1 <= score <= 10, errors, f"invalid score for {item.get('criterion')}")
        if isinstance(score, int) and score < 8:
            require(bool(str(item.get("repair", "")).strip()), errors, f"score below 8 lacks repair: {item.get('criterion')}")

    tests = as_list(packet.get("test_cases"))
    seen_types = {str(item.get("type", "")) for item in tests if isinstance(item, dict)}
    require(test_types <= seen_types, errors, "test_cases must include happy_path, edge_case, and adversarial")
    ids = [str(item.get("id", "")) for item in tests if isinstance(item, dict)]
    require(ids == sorted(ids), errors, "test_cases must be sorted by id for deterministic review")

    if packet.get("mode") == "port":
        notes = packet.get("porting_notes")
        require(isinstance(notes, dict), errors, "port mode requires porting_notes")
        if isinstance(notes, dict):
            require(bool(str(notes.get("source_platform", "")).strip()), errors, "porting_notes.source_platform is required")
            require(bool(str(notes.get("target_platform", "")).strip()), errors, "porting_notes.target_platform is required")
            require(bool(as_list(notes.get("unsupported_features"))), errors, "porting_notes.unsupported_features is required")
            require(bool(as_list(notes.get("losses"))), errors, "porting_notes.losses is required")

    serialized = json.dumps(packet, ensure_ascii=False)
    for pattern in BANNED_PATTERNS:
        require(not pattern.search(serialized), errors, f"banned hidden/invention pattern found: {pattern.pattern}")

    require(bool(as_list(packet.get("risks"))), errors, "risks list is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Prompt Forge packet JSON file")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()

    try:
        contract = load_json(CONTRACT)
        packet = load_json(args.packet)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}")
        return 2

    errors = validate_packet(packet, contract)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: prompt-forge packet valid: {args.packet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
