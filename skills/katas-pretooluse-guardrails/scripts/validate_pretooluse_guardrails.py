#!/usr/bin/env python3
"""Validate deterministic PreToolUse guardrail reports."""

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

    contract = policy("pretooluse-guardrail-contract.json")
    source_policy = policy("policy-source-policy.json")
    decision_policy = policy("permission-decision-policy.json")
    side_effect_policy = policy("side-effect-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "katas-pretooluse-guardrails":
        errors.append("skill must be katas-pretooluse-guardrails")
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

    policy_block = report.get("policy")
    if not isinstance(policy_block, dict):
        errors.append("policy must be an object")
        policy_block = {}
    if policy_block.get("source") not in source_policy["allowed_sources"]:
        errors.append(f"policy.source must be one of {source_policy['allowed_sources']}")
    if policy_block.get("hot_reload") is not True:
        errors.append("policy.hot_reload must be true")
    if policy_block.get("system_prompt_only") is not False:
        errors.append("policy.system_prompt_only must be false")
    rules = policy_block.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append("policy.rules must be a non-empty list")
        rules = []
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"policy.rules[{index}] must be an object")
            continue
        for field in source_policy["required_rule_fields"]:
            if field not in rule:
                errors.append(f"policy rule {index} missing field {field}")
        if rule.get("operator") not in source_policy["allowed_operators"]:
            errors.append(f"policy rule {index} operator must be allowed")
        if rule.get("decision") not in decision_policy["allowed_decisions"]:
            errors.append(f"policy rule {index} decision must be allowed")
        if not non_empty_string(rule.get("id")):
            errors.append(f"policy rule {index} id must be non-empty")
        if not non_empty_string(rule.get("target_tool")):
            errors.append(f"policy rule {index} target_tool must be non-empty")

    hook = report.get("hook")
    if not isinstance(hook, dict):
        errors.append("hook must be an object")
        hook = {}
    if hook.get("event_name") != decision_policy["hook_event_name"]:
        errors.append("hook.event_name must be PreToolUse")
    if not non_empty_string(hook.get("matcher")):
        errors.append("hook.matcher must be non-empty")
    if hook.get("registered") is not True:
        errors.append("hook.registered must be true")
    if hook.get("blocks_before_execution") is not True:
        errors.append("hook.blocks_before_execution must be true")
    output = hook.get("denial_output")
    if not isinstance(output, dict):
        errors.append("hook.denial_output must be an object")
    else:
        for field in decision_policy["required_hook_output_fields"]:
            if field not in output:
                errors.append(f"hook.denial_output missing field {field}")
        if output.get("hookEventName") != decision_policy["hook_event_name"]:
            errors.append("hook.denial_output.hookEventName must be PreToolUse")
        if output.get("permissionDecision") != "deny":
            errors.append("hook.denial_output.permissionDecision must be deny")
        if not non_empty_string(output.get("permissionDecisionReason")):
            errors.append("hook.denial_output.permissionDecisionReason must be non-empty")

    decisions = report.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append("decisions must be a non-empty list")
        decisions = []
    has_deny = False
    has_allow = False
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            errors.append(f"decisions[{index}] must be an object")
            continue
        if not non_empty_string(decision.get("tool_name")):
            errors.append(f"decisions[{index}].tool_name must be non-empty")
        if not isinstance(decision.get("tool_input"), dict):
            errors.append(f"decisions[{index}].tool_input must be an object")
        expected = decision.get("expected_decision")
        if expected not in decision_policy["allowed_decisions"]:
            errors.append(f"decisions[{index}].expected_decision must be allowed")
        if expected == "deny":
            has_deny = True
            if decision.get("expected_side_effects") is not False:
                errors.append(f"decisions[{index}] deny must have expected_side_effects false")
            if not non_empty_string(decision.get("reason")):
                errors.append(f"decisions[{index}] deny requires reason")
        if expected == "ask":
            if not non_empty_string(decision.get("reason")):
                errors.append(f"decisions[{index}] ask requires reason")
        if expected == "allow":
            has_allow = True
            if decision.get("expected_side_effects") is not True:
                errors.append(f"decisions[{index}] allow must have expected_side_effects true")

    if side_effect_policy["requires_deny_case"] and not has_deny:
        errors.append("decisions must include at least one deny case")
    if side_effect_policy["requires_allow_case"] and not has_allow:
        errors.append("decisions must include at least one allow case")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("denied_tool_executed") is not side_effect_policy["denied_tool_executed_must_be"]:
            errors.append("validation.denied_tool_executed must be false")
        if validation.get("allowed_tool_executed") is not side_effect_policy["allowed_tool_executed_must_be"]:
            errors.append("validation.allowed_tool_executed must be true")
        if validation.get("system_prompt_only") is not False:
            errors.append("validation.system_prompt_only must be false")
        if validation.get("prompt_injection_bypassed") is not side_effect_policy["prompt_injection_bypassed_must_be"]:
            errors.append("validation.prompt_injection_bypassed must be false")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        decisions_allowed = set(contract["json_contract"]["guardian_decisions"])
        if guardian.get("decision") not in decisions_allowed:
            errors.append(f"guardian.decision must be one of {sorted(decisions_allowed)}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PreToolUse guardrail JSON report")
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
