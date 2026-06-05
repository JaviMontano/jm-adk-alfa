#!/usr/bin/env python3
"""Validate deterministic prompt engineering packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


VALID_PATTERNS = {
    "zero_shot",
    "few_shot",
    "reasoning_scaffold",
    "system_instruction",
    "structured_output",
    "rag_grounded",
    "meta_prompt",
    "constitutional_self_critique",
}
REQUIRED_TOP_LEVEL = {
    "task",
    "target_model",
    "pattern",
    "prompt",
    "guardrails",
    "output_contract",
    "test_cases",
    "metrics",
    "risks",
}
REQUIRED_TEST_TYPES = {"happy_path", "edge_case", "adversarial"}


def load_packet(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("packet root must be an object")
    return data


def non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_test_cases(packet: dict) -> list[str]:
    errors: list[str] = []
    cases = packet.get("test_cases")
    if not isinstance(cases, list) or len(cases) < 3:
        return ["test_cases must contain at least three cases"]

    ids = []
    types = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("every test case must be an object")
            continue
        case_id = str(case.get("id", ""))
        ids.append(case_id)
        if not re.fullmatch(r"PE-\d{3}", case_id):
            errors.append(f"invalid test case id: {case_id}")
        case_type = str(case.get("type", ""))
        types.add(case_type)
        if case_type not in REQUIRED_TEST_TYPES:
            errors.append(f"invalid test case type for {case_id}: {case_type}")
        for field in ["input", "expected_checks"]:
            if field not in case:
                errors.append(f"{case_id}: missing {field}")
        checks = case.get("expected_checks")
        if not isinstance(checks, list) or not checks:
            errors.append(f"{case_id}: expected_checks must be non-empty list")

    if ids != sorted(ids):
        errors.append("test case ids must be sorted")
    missing_types = sorted(REQUIRED_TEST_TYPES - types)
    if missing_types:
        errors.append(f"missing test case types: {', '.join(missing_types)}")
    return errors


def validate_packet(packet: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(packet))
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    if packet.get("pattern") not in VALID_PATTERNS:
        errors.append(f"invalid pattern: {packet.get('pattern')}")
    if not non_empty_string(packet.get("task")):
        errors.append("task must be non-empty")
    if not non_empty_string(packet.get("target_model")):
        errors.append("target_model must be non-empty or explicit 'model_unspecified'")
    prompt = packet.get("prompt")
    if not non_empty_string(prompt):
        errors.append("prompt must be non-empty")
    elif "ignore previous instructions" in prompt.lower():
        errors.append("prompt must not include jailbreak instructions as instructions")

    guardrails = packet.get("guardrails")
    if not isinstance(guardrails, list) or len(guardrails) < 2:
        errors.append("guardrails must contain at least two entries")
    else:
        joined = " ".join(str(item).lower() for item in guardrails)
        for required in ["injection", "unsupported"]:
            if required not in joined:
                errors.append(f"guardrails must cover {required}")

    output_contract = packet.get("output_contract")
    if not isinstance(output_contract, dict):
        errors.append("output_contract must be an object")
    else:
        for field in ["format", "validation_criteria", "refusal_policy"]:
            if field not in output_contract:
                errors.append(f"output_contract missing {field}")

    metrics = packet.get("metrics")
    if not isinstance(metrics, dict):
        errors.append("metrics must be an object")
    else:
        for field in ["accuracy_target", "format_compliance_target", "injection_resistance_required"]:
            if field not in metrics:
                errors.append(f"metrics missing {field}")

    risks = packet.get("risks")
    if not isinstance(risks, list):
        errors.append("risks must be a list")

    errors.extend(validate_test_cases(packet))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a prompt engineering packet")
    parser.add_argument("packet", help="JSON packet path")
    args = parser.parse_args()

    try:
        errors = validate_packet(load_packet(Path(args.packet)))
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    for error in errors:
        print(f"ERROR: {error}")
    print(f"prompt_packet={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
