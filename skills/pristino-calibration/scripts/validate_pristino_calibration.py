#!/usr/bin/env python3
"""Validate deterministic Pristino calibration reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SKILL = "pristino-calibration"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("pristino-calibration-contract.json")["json_contract"]
    mode_policy = asset("mode-output-policy.json")
    precedence_policy = asset("precedence-policy.json")
    evidence_policy = asset("evidence-tag-policy.json")
    canvas_policy = asset("canvas-contract-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("calibration_id")):
        errors.append("calibration_id must be non-empty")

    block = report.get("injected_block")
    if not isinstance(block, dict):
        errors.append("injected_block must be an object")
        block = {}
    mode = block.get("mode")
    complexity = block.get("complexity")
    confidence = block.get("confidence")
    if mode not in mode_policy["allowed_modes"]:
        errors.append("injected_block.mode is not allowed")
    if complexity not in mode_policy["allowed_complexities"]:
        errors.append("injected_block.complexity is not allowed")
    if not non_empty_string(block.get("persona")):
        errors.append("injected_block.persona must be non-empty")
    if not non_empty_string(block.get("persona_id")):
        errors.append("injected_block.persona_id must be non-empty")
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        errors.append("injected_block.confidence must be between 0 and 1")
    delegates = block.get("delegate")
    if not isinstance(delegates, list):
        errors.append("injected_block.delegate must be a list")
        delegates = []
    unknown_delegates = sorted(set(delegates) - set(mode_policy["known_delegate_agents"]))
    if unknown_delegates:
        errors.append(f"unknown delegate agents: {unknown_delegates}")

    persona_output = report.get("persona_output")
    if not isinstance(persona_output, dict):
        errors.append("persona_output must be an object")
        persona_output = {}
    if mode == "bypass":
        if non_empty_string(persona_output.get("line_1")):
            errors.append("bypass mode must not declare persona line")
    elif persona_output.get("line_1") != block.get("persona"):
        errors.append("persona_output.line_1 must match injected persona")
    if persona_output.get("declared_confidence") != confidence:
        errors.append("persona_output.declared_confidence must match injected confidence")

    optimizer = report.get("optimizer")
    if not isinstance(optimizer, dict):
        errors.append("optimizer must be an object")
        optimizer = {}
    key = mode
    if mode == "full":
        key = "full_substantive" if complexity == "substantive" else "full_trivial"
    required_sections = set(mode_policy["optimizer_requirements"].get(key, []))
    allowed_sections = required_sections
    present_sections = {name for name in ["original_prompt", "optimized_prompt", "response"] if non_empty_string(optimizer.get(name))}
    missing = required_sections - present_sections
    extra = present_sections - allowed_sections
    if missing:
        errors.append(f"optimizer missing required sections: {sorted(missing)}")
    if extra:
        errors.append(f"optimizer has sections forbidden for mode: {sorted(extra)}")

    if report.get("precedence") != precedence_policy["order"]:
        errors.append("precedence order is invalid")

    evidence_tags = report.get("evidence_tags")
    if not isinstance(evidence_tags, list):
        errors.append("evidence_tags must be a list")
        evidence_tags = []
    if complexity == "substantive":
        if len(set(evidence_tags) & set(evidence_policy["required_tags"])) < evidence_policy["minimum_tags_for_substantive"]:
            errors.append("substantive output requires at least three evidence tags")

    canvas = report.get("canvas")
    if not isinstance(canvas, dict):
        errors.append("canvas must be an object")
        canvas = {}
    canvas_required = complexity == "substantive" and mode == "full"
    if canvas.get("required") is not canvas_required:
        errors.append(f"canvas.required must be {canvas_required}")
    sections = set(canvas.get("sections", [])) if isinstance(canvas.get("sections"), list) else set()
    if canvas_required and not set(canvas_policy["required_sections"]).issubset(sections):
        errors.append("canvas.sections missing required Canvas contract sections")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    expected = {
        "persona_line_valid": mode == "bypass" or persona_output.get("line_1") == block.get("persona"),
        "mode_shape_valid": not missing and not extra,
        "precedence_valid": report.get("precedence") == precedence_policy["order"],
        "evidence_tags_present": complexity != "substantive" or len(set(evidence_tags) & set(evidence_policy["required_tags"])) >= evidence_policy["minimum_tags_for_substantive"],
        "canvas_contract_present": not canvas_required or set(canvas_policy["required_sections"]).issubset(sections),
        "delegate_agents_known": not unknown_delegates,
        "deterministic_script_passed": True,
    }
    for field, value in expected.items():
        if validation.get(field) is not value:
            errors.append(f"validation.{field} must be {value}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
        guardian = {}
    decision = guardian.get("decision")
    if decision not in contract["guardian_decisions"]:
        errors.append("guardian.decision is not allowed")
    if not non_empty_string(guardian.get("reason")):
        errors.append("guardian.reason must be non-empty")
    blocking_needed = any(value is False for value in expected.values())
    if decision == "pass" and blocking_needed:
        errors.append("guardian pass requires all validation flags true")
    if decision == "block" and not blocking_needed:
        errors.append("guardian block requires a validation failure")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Pristino calibration JSON report")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(load_json(args.report))
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
