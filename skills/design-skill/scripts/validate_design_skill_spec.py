#!/usr/bin/env python3
"""Validate deterministic design-skill specification fixtures."""

from __future__ import annotations

import argparse
import json
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


def validate_date(value: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"reference_date must be ISO date: {value}")


def validate_frontmatter(spec: dict[str, Any], policy: dict[str, Any], tool_policy: dict[str, Any], errors: list[str]) -> None:
    frontmatter = spec.get("frontmatter")
    if not isinstance(frontmatter, dict):
        errors.append("frontmatter must be an object")
        return
    require_fields(frontmatter, policy["required_fields"], "frontmatter", errors)
    if not re.match(policy["skill_name_pattern"], str(frontmatter.get("name", ""))):
        errors.append("frontmatter name must be kebab-case")
    if frontmatter.get("name") != spec.get("designed_skill"):
        errors.append("frontmatter name must match designed_skill")
    for field in frontmatter:
        if field not in policy["supported_fields"]:
            errors.append(f"unsupported frontmatter field: {field}")
    if "$0" in str(frontmatter.get("argument-hint", "")):
        errors.append("argument-hint cannot use $0")
    tools = frontmatter.get("allowed-tools", [])
    if not isinstance(tools, list) or not tools:
        errors.append("frontmatter allowed-tools must be a non-empty list")
        return
    for tool in tools:
        if tool not in tool_policy["known_tools"]:
            errors.append(f"unknown tool: {tool}")


def validate_body(spec: dict[str, Any], body: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    procedure = spec.get("procedure")
    if not isinstance(procedure, list) or not (body["procedure_min"] <= len(procedure) <= body["procedure_max"]):
        errors.append("procedure must contain 5 to 10 steps")
    else:
        seen = []
        for step in procedure:
            if not isinstance(step, dict):
                errors.append("procedure step must be an object")
                continue
            require_fields(step, contract["required_step_fields"], "procedure step", errors)
            seen.append(step.get("step"))
            if step.get("action") not in body["allowed_action_verbs"]:
                errors.append(f"invalid action verb: {step.get('action')}")
            if step.get("evidence_tag") not in allowed:
                errors.append(f"invalid procedure evidence_tag: {step.get('evidence_tag')}")
        if seen != sorted(seen):
            errors.append("procedure steps must be ordered")

    quality = spec.get("quality_criteria")
    generic = re.compile(r"\b(high quality|works well|good output|be useful)\b", re.IGNORECASE)
    if not isinstance(quality, list) or not (body["quality_min"] <= len(quality) <= body["quality_max"]):
        errors.append("quality_criteria must contain 4 to 6 items")
    else:
        for item in quality:
            if generic.search(str(item)):
                errors.append(f"quality criterion is too generic: {item}")
            if not has_evidence(item, allowed):
                errors.append("quality criterion missing evidence tag")

    anti = spec.get("anti_patterns")
    if not isinstance(anti, list) or not (body["anti_pattern_min"] <= len(anti) <= body["anti_pattern_max"]):
        errors.append("anti_patterns must contain 4 to 6 items")
    edge = spec.get("edge_cases")
    if not isinstance(edge, list) or not (body["edge_case_min"] <= len(edge) <= body["edge_case_max"]):
        errors.append("edge_cases must contain 3 to 5 items")
    elif not has_evidence(edge, allowed):
        errors.append("edge_cases expected behavior must include evidence tags")


def validate_tools(spec: dict[str, Any], tool_policy: dict[str, Any], errors: list[str]) -> None:
    frontmatter = spec.get("frontmatter", {})
    tools = frontmatter.get("allowed-tools", [])
    profile = spec.get("tool_profile")
    if profile not in tool_policy["profiles"]:
        errors.append("tool_profile is invalid")
        return
    expected = set(tool_policy["profiles"][profile])
    if set(tools) != expected:
        errors.append("allowed-tools must match declared tool_profile")
    rationale = spec.get("tool_rationale")
    if not isinstance(rationale, list) or {item.get("tool") for item in rationale if isinstance(item, dict)} != set(tools):
        errors.append("tool_rationale must cover every allowed tool exactly")


def validate_moat(spec: dict[str, Any], body: dict[str, Any], errors: list[str]) -> None:
    moat = spec.get("moat_score")
    if not isinstance(moat, dict):
        errors.append("moat_score must be an object")
        return
    total = moat.get("total")
    expected = sum(int(moat.get(key, 0)) for key in ["completeness", "accuracy", "actionability", "maintainability"])
    if total != expected:
        errors.append("moat_score total must equal component sum")
    if not isinstance(total, int) or total < body["moat_min_total"]:
        errors.append("moat_score total is below threshold")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a design-skill specification JSON file")
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "report-contract.json")
    frontmatter_policy = load_json(ASSETS / "frontmatter-policy.json")
    body_policy = load_json(ASSETS / "body-policy.json")
    tool_policy = load_json(ASSETS / "tool-policy.json")
    allowed = set(contract["allowed_evidence_tags"])

    spec = load_json(args.spec)
    errors: list[str] = []
    if not isinstance(spec, dict):
        errors.append("spec root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in spec:
                errors.append(f"missing top-level field: {field}")
        if spec.get("skill") != "design-skill":
            errors.append("skill must be design-skill")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_date(str(spec["reference_date"]), errors)
    body = json.dumps(spec, ensure_ascii=False)
    for term in contract["moving_time_terms"]:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"spec must avoid moving time term: {term}")
    for section in ("summary", "guiding_principle", "validation", "risks"):
        if not has_evidence(spec.get(section), allowed):
            errors.append(f"{section} must include evidence tag")

    validate_frontmatter(spec, frontmatter_policy, tool_policy, errors)
    validate_body(spec, body_policy, contract, allowed, errors)
    validate_tools(spec, tool_policy, errors)
    validate_moat(spec, body_policy, errors)

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.spec.name}: steps={len(spec['procedure'])} moat={spec['moat_score']['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
