#!/usr/bin/env python3
"""Validate deterministic workflow-creator specs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def as_workflow(data: Any) -> dict[str, Any]:
    if isinstance(data, dict) and isinstance(data.get("workflow"), dict):
        return data["workflow"]
    if isinstance(data, dict):
        return data
    raise ValueError("workflow spec must be a JSON object")


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def word_count(value: str) -> int:
    return len([part for part in re.split(r"\s+", value.strip()) if part])


def contains_blocked(value: Any, blocked: list[str]) -> str | None:
    text = json.dumps(value, ensure_ascii=False).lower() if not isinstance(value, str) else value.lower()
    for phrase in blocked:
        if phrase.lower() in text:
            return phrase
    return None


def has_signal(value: str, signals: list[str]) -> bool:
    lowered = value.lower()
    return any(signal.lower() in lowered for signal in signals)


def validate_list(workflow: dict[str, Any], field: str, minimum: int, errors: list[str]) -> None:
    value = workflow.get(field)
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{field} must be a list with at least {minimum} item(s)")


def validate_inputs(workflow: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    inputs = workflow.get("inputs")
    if not isinstance(inputs, list):
        return
    allowed_types = set(contract["input_types"])
    required_fields = contract["input_fields"]
    for index, item in enumerate(inputs, start=1):
        if not isinstance(item, dict):
            errors.append(f"inputs[{index}] must be an object")
            continue
        for field in required_fields:
            if is_blank(item.get(field)):
                errors.append(f"inputs[{index}] missing {field}")
        if item.get("type") not in allowed_types:
            errors.append(f"inputs[{index}].type must be one of {sorted(allowed_types)}")
        if item.get("required") is not True:
            errors.append(f"inputs[{index}].required must be true")


def validate_steps(workflow: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    rules = contract["rules"]
    steps = workflow.get("steps")
    if not isinstance(steps, list):
        return
    if len(steps) < rules["min_steps"] or len(steps) > rules["max_steps"]:
        errors.append(f"steps must contain {rules['min_steps']}-{rules['max_steps']} items")

    step_fields = contract["step_fields"]
    signal_words = contract["required_signal_words"]
    for expected_number, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            errors.append(f"steps[{expected_number}] must be an object")
            continue
        for field in step_fields:
            if is_blank(step.get(field)):
                errors.append(f"steps[{expected_number}] missing {field}")
        if step.get("stepNumber") != expected_number:
            errors.append(f"steps[{expected_number}].stepNumber must be {expected_number}")
        title = str(step.get("title", ""))
        if title and not (
            rules["step_title_min_words"] <= word_count(title) <= rules["step_title_max_words"]
        ):
            errors.append(f"steps[{expected_number}].title must be 2-5 words")
        for field in ["validationRule", "failureSignal", "recoveryAction"]:
            value = str(step.get(field, ""))
            if value and not has_signal(value, signal_words[field]):
                errors.append(f"steps[{expected_number}].{field} lacks observable signal")
        why = str(step.get("whyThisMatters", "")).strip().lower()
        if why and title and why == title.strip().lower():
            errors.append(f"steps[{expected_number}].whyThisMatters restates title")


def validate_raci(workflow: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    raci = workflow.get("raci")
    if not isinstance(raci, dict):
        errors.append("raci must be an object")
        return
    for field in contract["raci_fields"]:
        value = raci.get(field)
        if is_blank(value):
            errors.append(f"raci.{field} is required")


def validate_kpis(workflow: dict[str, Any], contract: dict[str, Any], errors: list[str]) -> None:
    kpis = workflow.get("kpis")
    if not isinstance(kpis, list):
        return
    allowed_units = set(contract["kpi_units"])
    for index, item in enumerate(kpis, start=1):
        if not isinstance(item, dict):
            errors.append(f"kpis[{index}] must be an object")
            continue
        for field in contract["kpi_fields"]:
            if is_blank(item.get(field)):
                errors.append(f"kpis[{index}] missing {field}")
        if item.get("unit") not in allowed_units:
            errors.append(f"kpis[{index}].unit must be one of {sorted(allowed_units)}")


def validate_workflow(contract: dict[str, Any], workflow: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rules = contract["rules"]
    blocked = contract["blocked_phrases"]

    for field in contract["top_level_fields"]:
        if field not in workflow:
            errors.append(f"missing top-level field: {field}")
        elif is_blank(workflow[field]):
            errors.append(f"empty top-level field: {field}")

    if workflow.get("id") and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(workflow["id"])):
        errors.append("id must be kebab-case")

    title = str(workflow.get("title", ""))
    if title and word_count(title) > rules["title_max_words"]:
        errors.append(f"title must be at most {rules['title_max_words']} words")

    objective = str(workflow.get("objective", ""))
    if objective and word_count(objective) < rules["objective_min_words"]:
        errors.append(f"objective must be at least {rules['objective_min_words']} words")

    for field, minimum in [
        ("preconditions", rules["min_preconditions"]),
        ("inputs", rules["min_inputs"]),
        ("secondaryOutputs", rules["min_secondary_outputs"]),
        ("DoD", rules["min_dod"]),
        ("qaChecklist", rules["min_qa_checks"]),
        ("kpis", rules["min_kpis"])
    ]:
        validate_list(workflow, field, minimum, errors)

    if workflow.get("cadence") not in contract["cadence_allowed"]:
        errors.append(f"cadence must be one of {contract['cadence_allowed']}")

    found_blocked = contains_blocked(workflow, blocked)
    if found_blocked:
        errors.append(f"blocked phrase present: {found_blocked}")

    validate_inputs(workflow, contract, errors)
    validate_steps(workflow, contract, errors)
    validate_raci(workflow, contract, errors)
    validate_kpis(workflow, contract, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate workflow-creator JSON spec")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        spec = as_workflow(load_json(args.spec))
        errors = validate_workflow(contract, spec)
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
