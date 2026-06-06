#!/usr/bin/env python3
"""Validate deterministic design-agent specification fixtures."""

from __future__ import annotations

import argparse
import json
import math
import re
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def has_evidence(value: Any, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item, allowed) for item in value.values())
    return False


def require_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if obj.get(field) in ("", [], None):
            errors.append(f"{label} missing {field}")


def validate_date(value: str, field: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must be ISO date: {value}")


def round_up_to_5(value: int) -> int:
    return int(math.ceil(value / 5) * 5)


def validate_frontmatter(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    frontmatter = spec.get("frontmatter")
    if not isinstance(frontmatter, dict):
        errors.append("frontmatter must be an object")
        return
    require_fields(frontmatter, policy["required_fields"], "frontmatter", errors)
    pattern = re.compile(policy["agent_name_pattern"])
    if not pattern.match(str(frontmatter.get("name", ""))):
        errors.append("frontmatter name must be kebab-case")
    if frontmatter.get("name") != spec.get("agent_name"):
        errors.append("frontmatter name must match agent_name")
    for field in frontmatter:
        if field not in policy["supported_fields"]:
            errors.append(f"frontmatter field is not supported: {field}")
    for field in policy["forbidden_fields"]:
        if field in frontmatter:
            errors.append(f"frontmatter contains forbidden field: {field}")
    for pair in policy["mutually_exclusive"]:
        if all(field in frontmatter for field in pair):
            errors.append(f"frontmatter fields are mutually exclusive: {', '.join(pair)}")
    tools = frontmatter.get("tools", [])
    if tools and not isinstance(tools, list):
        errors.append("frontmatter tools must be a list")
    for tool in tools if isinstance(tools, list) else []:
        if tool not in policy["known_tools"]:
            errors.append(f"frontmatter tool is unknown: {tool}")


def validate_assignments(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    assignments = spec.get("skill_assignments")
    if not isinstance(assignments, list) or not assignments:
        errors.append("skill_assignments must be a non-empty list")
        return
    for item in assignments:
        if not isinstance(item, dict):
            errors.append("each skill assignment must be an object")
            continue
        require_fields(item, contract["required_assignment_fields"], "skill_assignment", errors)
        if item.get("evidence_tag") not in allowed:
            errors.append(f"skill assignment {item.get('skill')} has invalid evidence_tag")


def validate_flows(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    flows = spec.get("execution_flows")
    if not isinstance(flows, list) or not flows:
        errors.append("execution_flows must be a non-empty list")
        return
    for flow in flows:
        if not isinstance(flow, dict):
            errors.append("each execution flow must be an object")
            continue
        require_fields(flow, contract["required_flow_fields"], "execution_flow", errors)
        if not isinstance(flow.get("steps"), list) or len(flow.get("steps", [])) < 2:
            errors.append(f"execution flow {flow.get('command')} requires at least two steps")
        if not has_evidence(flow.get("steps"), allowed):
            errors.append(f"execution flow {flow.get('command')} steps need evidence tags")
        if not has_evidence(flow.get("quality_gate"), allowed):
            errors.append(f"execution flow {flow.get('command')} quality_gate needs evidence tag")


def validate_principles(spec: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    principles = spec.get("operating_principles")
    if not isinstance(principles, list) or len(principles) < 4 or len(principles) > 7:
        errors.append("operating_principles must contain 4 to 7 items")
        return
    generic = re.compile(r"\b(be helpful|be careful|ensure quality|do your best|communicate clearly)\b", re.IGNORECASE)
    for principle in principles:
        if not isinstance(principle, str):
            errors.append("operating principles must be strings")
            continue
        if generic.search(principle):
            errors.append(f"operating principle is too generic: {principle}")
        if len(principle.split()) < 6:
            errors.append(f"operating principle is not specific enough: {principle}")
        if not has_evidence(principle, allowed):
            errors.append("operating principle missing evidence tag")


def validate_maxturns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    rationale = spec.get("max_turns_rationale")
    frontmatter = spec.get("frontmatter", {})
    if not isinstance(rationale, dict):
        errors.append("max_turns_rationale must be an object")
        return
    require_fields(rationale, policy["required_fields"], "max_turns_rationale", errors)
    try:
        skills_count = int(rationale["skills_count"])
        complexity_bonus = int(rationale["complexity_bonus"])
        interaction_points = int(rationale["interaction_points"])
        formula_result = int(rationale["formula_result"])
        rounded = int(rationale["rounded_maxTurns"])
    except (KeyError, TypeError, ValueError):
        errors.append("max_turns_rationale values must be integers")
        return
    expected = (skills_count * 4) + complexity_bonus + (interaction_points * 2)
    if formula_result != expected:
        errors.append("max_turns_rationale formula_result is incorrect")
    if rounded != round_up_to_5(expected):
        errors.append("max_turns_rationale rounded_maxTurns is incorrect")
    if rounded < policy["min"] or rounded > policy["max"]:
        errors.append("max_turns_rationale rounded_maxTurns out of policy range")
    if frontmatter.get("maxTurns") != rounded:
        errors.append("frontmatter maxTurns must match rounded_maxTurns")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a design-agent specification JSON file")
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "report-contract.json")
    frontmatter_policy = load_json(ASSETS / "frontmatter-policy.json")
    maxturns_policy = load_json(ASSETS / "maxturns-policy.json")
    allowed = set(contract["allowed_evidence_tags"])

    spec = load_json(args.spec)
    errors: list[str] = []
    if not isinstance(spec, dict):
        errors.append("spec root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in spec:
                errors.append(f"missing top-level field: {field}")
        if spec.get("skill") != "design-agent":
            errors.append("skill must be design-agent")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_date(str(spec["reference_date"]), "reference_date", errors)
    body = json.dumps(spec, ensure_ascii=False)
    for term in contract["moving_time_terms"]:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"spec must avoid moving time term: {term}")
    for section in ("summary", "validation", "risks"):
        if not has_evidence(spec.get(section), allowed):
            errors.append(f"{section} must include evidence tag")

    role_boundary = spec.get("role_boundary")
    if not isinstance(role_boundary, dict):
        errors.append("role_boundary must be an object")
    elif not has_evidence(role_boundary.get("role"), allowed):
        errors.append("role_boundary role must include evidence tag")

    validate_frontmatter(spec, frontmatter_policy, errors)
    validate_assignments(spec, contract, allowed, errors)
    validate_flows(spec, contract, allowed, errors)
    validate_principles(spec, allowed, errors)
    validate_maxturns(spec, maxturns_policy, errors)

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.spec.name}: assignments={len(spec['skill_assignments'])} flows={len(spec['execution_flows'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
