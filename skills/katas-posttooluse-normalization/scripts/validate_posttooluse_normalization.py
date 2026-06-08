#!/usr/bin/env python3
"""Validate deterministic PostToolUse normalization reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def policy(name: str) -> dict[str, Any]:
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

    contract = policy("posttooluse-normalization-contract.json")
    output_policy = policy("updated-output-policy.json")
    normalization_policy = policy("normalization-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "katas-posttooluse-normalization":
        errors.append("skill must be katas-posttooluse-normalization")
    for field in ["report_id", "scenario"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")

    evidence = report.get("evidence")
    accepted_evidence = set(evidence_policy["accepted_evidence_types"])
    if not isinstance(evidence, list) or len(evidence) < evidence_policy["minimum_evidence_items"]:
        errors.append(f"evidence must contain at least {evidence_policy['minimum_evidence_items']} items")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            if item.get("type") not in accepted_evidence:
                errors.append(f"evidence[{index}].type must be accepted")
            if not non_empty_string(item.get("detail")):
                errors.append(f"evidence[{index}].detail must be non-empty")

    hook = report.get("hook")
    if not isinstance(hook, dict):
        errors.append("hook must be an object")
        hook = {}
    if hook.get("event_name") != output_policy["hook_event_name"]:
        errors.append("hook.event_name must be PostToolUse")
    if not non_empty_string(hook.get("matcher")):
        errors.append("hook.matcher must be non-empty")
    if hook.get("registered") is not True:
        errors.append("hook.registered must be true")
    if hook.get("runtime_enforced") is not True:
        errors.append("hook.runtime_enforced must be true")
    hook_output = hook.get("hook_specific_output")
    if not isinstance(hook_output, dict):
        errors.append("hook.hook_specific_output must be an object")
    else:
        for field in output_policy["required_hook_output_fields"]:
            if field not in hook_output:
                errors.append(f"hook.hook_specific_output missing field {field}")
        if hook_output.get("hookEventName") != output_policy["hook_event_name"]:
            errors.append("hook.hook_specific_output.hookEventName must be PostToolUse")
        updated = hook_output.get("updatedMCPToolOutput")
        if not isinstance(updated, dict):
            errors.append("updatedMCPToolOutput must be an object")
        else:
            if updated.get("type") != output_policy["updated_output_type"]:
                errors.append("updatedMCPToolOutput.type must be text")
            text = updated.get("text")
            if not non_empty_string(text):
                errors.append("updatedMCPToolOutput.text must be non-empty")
            else:
                try:
                    parsed = json.loads(text)
                    if not isinstance(parsed, dict):
                        errors.append("updatedMCPToolOutput.text must parse to a JSON object")
                except json.JSONDecodeError:
                    errors.append("updatedMCPToolOutput.text must parse as JSON")
                for marker in output_policy["raw_payload_markers"]:
                    if marker in text:
                        errors.append("updatedMCPToolOutput.text must not contain raw payload markers")
        additional = hook_output.get("additionalContext")
        if not non_empty_string(additional):
            errors.append("additionalContext must be non-empty")
        else:
            for marker in output_policy["raw_payload_markers"]:
                if marker in additional:
                    errors.append("additionalContext must not contain raw payload markers")

    normalization = report.get("normalization")
    if not isinstance(normalization, dict):
        errors.append("normalization must be an object")
        normalization = {}
    status_map = normalization.get("status_map")
    if not isinstance(status_map, dict) or not status_map:
        errors.append("normalization.status_map must be a non-empty object")
    canonical_schema = normalization.get("canonical_schema")
    expected_fields = normalization_policy["canonical_fields"]
    if canonical_schema != expected_fields:
        errors.append(f"normalization.canonical_schema must be {expected_fields}")
    transformations = normalization.get("transformations")
    if not isinstance(transformations, list) or not transformations:
        errors.append("normalization.transformations must be a non-empty list")
        transformations = []
    for index, transform in enumerate(transformations):
        if not isinstance(transform, dict):
            errors.append(f"normalization.transformations[{index}] must be an object")
            continue
        for field in ["tool_name", "raw_payload", "normalized_output", "raw_payload_visible_to_model", "fallback_for_unknown"]:
            if field not in transform:
                errors.append(f"transformation {index} missing field {field}")
        if not non_empty_string(transform.get("tool_name")):
            errors.append(f"transformation {index}.tool_name must be non-empty")
        raw_payload = transform.get("raw_payload")
        if not non_empty_string(raw_payload):
            errors.append(f"transformation {index}.raw_payload must be non-empty")
        normalized = transform.get("normalized_output")
        if not isinstance(normalized, dict):
            errors.append(f"transformation {index}.normalized_output must be an object")
            normalized = {}
        for field in expected_fields:
            if field not in normalized:
                errors.append(f"transformation {index}.normalized_output missing {field}")
        if transform.get("raw_payload_visible_to_model") is not False:
            errors.append(f"transformation {index}.raw_payload_visible_to_model must be false")
        if transform.get("fallback_for_unknown") != normalization_policy["fallback_status"]:
            errors.append(f"transformation {index}.fallback_for_unknown must be unknown")
        normalized_text = json.dumps(normalized, sort_keys=True)
        for marker in output_policy["raw_payload_markers"]:
            if marker in normalized_text:
                errors.append(f"transformation {index}.normalized_output must not contain raw payload markers")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("raw_payload_visible_to_model") is not False:
            errors.append("validation.raw_payload_visible_to_model must be false")
        if validation.get("all_matched_tools_covered") is not True:
            errors.append("validation.all_matched_tools_covered must be true")
        if validation.get("fallback_for_unknown_status") is not True:
            errors.append("validation.fallback_for_unknown_status must be true")
        if validation.get("per_tool_normalization") is not False:
            errors.append("validation.per_tool_normalization must be false")
        if validation.get("additional_context_contains_payload") is not False:
            errors.append("validation.additional_context_contains_payload must be false")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        decisions = set(contract["json_contract"]["guardian_decisions"])
        if guardian.get("decision") not in decisions:
            errors.append(f"guardian.decision must be one of {sorted(decisions)}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PostToolUse normalization JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON report")
    args = parser.parse_args()

    try:
        report = load_json(args.report)
        errors = validate(report)
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
