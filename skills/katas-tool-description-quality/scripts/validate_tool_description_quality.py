#!/usr/bin/env python3
"""Validate deterministic tool description quality reports."""

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


def non_empty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(non_empty_string(item) for item in value)


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("tool-description-contract.json")
    quality = policy("description-quality-policy.json")
    routing = policy("routing-risk-policy.json")
    action_policy = policy("action-priority-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "katas-tool-description-quality":
        errors.append("skill must be katas-tool-description-quality")
    for field in ["report_id", "scenario"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if not isinstance(report.get("evidence"), list) or not report.get("evidence"):
        errors.append("evidence must be a non-empty list")

    tools = report.get("tools")
    if not isinstance(tools, list) or not tools:
        errors.append("tools must be a non-empty list")
        tools = []
    tool_names = [tool.get("name") for tool in tools if isinstance(tool, dict)]

    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            errors.append(f"tools[{index}] must be an object")
            continue
        name = tool.get("name", f"tools[{index}]")
        for field in quality["required_tool_fields"]:
            if field not in tool:
                errors.append(f"tool {name} missing field {field}")
        if not non_empty_string(tool.get("name")):
            errors.append(f"tool {index} name must be non-empty")
        description = tool.get("description")
        if not non_empty_string(description):
            errors.append(f"tool {name} description must be non-empty")
        else:
            if description in quality["blocked_descriptions"]:
                errors.append(f"tool {name} uses blocked generic description")
            for phrase in quality["required_description_phrases"]:
                if phrase not in description:
                    errors.append(f"tool {name} description must include '{phrase}'")
        if not non_empty_string(tool.get("input_format")):
            errors.append(f"tool {name} input_format must be non-empty")
        if not non_empty_string_list(tool.get("example_queries")):
            errors.append(f"tool {name} example_queries must be a non-empty string list")
        if not non_empty_string(tool.get("boundary")):
            errors.append(f"tool {name} boundary must be non-empty")
        action = tool.get("action")
        if action not in quality["allowed_actions"]:
            errors.append(f"tool {name} action must be one of {quality['allowed_actions']}")
        if action == "rename" and not non_empty_string(tool.get("renamed_from")):
            errors.append(f"tool {name} action rename requires renamed_from")
        if action == "split" and not non_empty_string(tool.get("split_from")):
            errors.append(f"tool {name} action split requires split_from")
        target = tool.get("reciprocal_boundary_to")
        if target is not None and target not in tool_names:
            errors.append(f"tool {name} reciprocal_boundary_to must target an existing tool")

    if routing["reciprocal_boundary_required"]:
        by_name = {tool.get("name"): tool for tool in tools if isinstance(tool, dict)}
        for tool in tools:
            if not isinstance(tool, dict):
                continue
            target = tool.get("reciprocal_boundary_to")
            if target:
                peer = by_name.get(target, {})
                if peer.get("reciprocal_boundary_to") != tool.get("name"):
                    errors.append(f"tool {tool.get('name')} boundary with {target} is not reciprocal")

    findings = report.get("overlap_findings")
    if not isinstance(findings, list):
        errors.append("overlap_findings must be a list")
        findings = []
    risk_order = action_policy["risk_type_order"]
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    expected_actions = []
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append("overlap_findings entries must be objects")
            continue
        risk_type = finding.get("risk_type")
        if risk_type not in routing["risk_types"]:
            errors.append(f"unknown risk_type: {risk_type}")
        if not non_empty_string(finding.get("evidence")):
            errors.append("overlap finding evidence must be non-empty")
        if finding.get("severity") not in severity_rank:
            errors.append("overlap finding severity must be high, medium, or low")
        if risk_type in routing["rename_required_when"] and finding.get("recommended_action") != "rename":
            errors.append(f"risk {risk_type} requires rename")
        if risk_type in routing["split_required_when"] and finding.get("recommended_action") != "split":
            errors.append(f"risk {risk_type} requires split")
        if risk_type in routing["boundary_required_when"] and finding.get("requires_boundary") is not True:
            errors.append(f"risk {risk_type} requires boundary")
        if risk_type in risk_order and finding.get("severity") in severity_rank:
            expected_actions.append(
                {
                    "tool": finding.get("tool"),
                    "action": finding.get("recommended_action"),
                    "severity": finding.get("severity"),
                    "risk_type": risk_type,
                }
            )

    expected_actions.sort(
        key=lambda item: (
            severity_rank[item["severity"]],
            risk_order.index(item["risk_type"]),
            str(item["tool"]),
        )
    )
    expected_pairs = [(item["tool"], item["action"]) for item in expected_actions[: action_policy["max_actions"]]]
    actions = report.get("priority_actions")
    if not isinstance(actions, list):
        errors.append("priority_actions must be a list")
    else:
        if len(actions) > action_policy["max_actions"]:
            errors.append(f"priority_actions must contain at most {action_policy['max_actions']} items")
        actual_pairs = [(item.get("tool"), item.get("action")) for item in actions if isinstance(item, dict)]
        if actual_pairs != expected_pairs:
            errors.append(f"priority_actions order must be {expected_pairs}")
        for index, action in enumerate(actions):
            if not isinstance(action, dict):
                errors.append(f"priority_actions[{index}] must be an object")
                continue
            if not non_empty_string(action.get("reason")):
                errors.append(f"priority_actions[{index}].reason must be non-empty")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("overlapping_contracts_remaining") is not False:
            errors.append("validation.overlapping_contracts_remaining must be false")
        if validation.get("reciprocal_boundaries") is not True:
            errors.append("validation.reciprocal_boundaries must be true")
        rate = validation.get("expected_misroute_rate_pct")
        if not isinstance(rate, (int, float)) or rate > quality["max_expected_misroute_rate_pct"]:
            errors.append(f"validation.expected_misroute_rate_pct must be <= {quality['max_expected_misroute_rate_pct']}")

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
    parser = argparse.ArgumentParser(description="Validate a tool description quality JSON report")
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
