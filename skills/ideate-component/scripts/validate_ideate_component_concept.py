#!/usr/bin/env python3
"""Validate deterministic ideate-component concept-card fixtures."""

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


def validate_plugin_context(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    if spec.get("source_mode") not in contract["source_modes"]:
        errors.append("source_mode is invalid")
    context = spec.get("plugin_context")
    if not isinstance(context, dict):
        errors.append("plugin_context must be an object")
        return
    require_fields(context, ["path_or_brief", "evidence_tag"], "plugin_context", errors)
    if context.get("evidence_tag") not in allowed:
        errors.append("plugin_context evidence_tag is invalid")

    existing = spec.get("existing_components")
    if not isinstance(existing, list):
        errors.append("existing_components must be a list")
        return
    for item in existing:
        if not isinstance(item, dict):
            errors.append("existing component must be an object")
            continue
        require_fields(item, ["name", "type", "evidence_tag"], "existing component", errors)
        if item.get("evidence_tag") not in allowed:
            errors.append(f"existing component evidence_tag is invalid: {item.get('name')}")


def validate_candidates(spec: dict[str, Any], contract: dict[str, Any], allowed_types: set[str], allowed: set[str], errors: list[str]) -> None:
    component_type = spec.get("component_type")
    candidates = spec.get("candidates")
    if component_type not in allowed_types:
        errors.append("component_type is invalid")
    if not isinstance(candidates, list) or not (contract["candidate_min"] <= len(candidates) <= contract["candidate_max"]):
        errors.append("candidates must contain 2 to 3 items")
        return

    pattern = re.compile(contract["name_pattern"])
    existing_names = {
        item.get("name")
        for item in spec.get("existing_components", [])
        if isinstance(item, dict)
    }
    candidate_names: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append("candidate must be an object")
            continue
        require_fields(candidate, contract["required_candidate_fields"], "candidate", errors)
        name = str(candidate.get("name", ""))
        candidate_names.append(name)
        if not pattern.match(name):
            errors.append(f"candidate name must be kebab-case: {name}")
        if name in existing_names:
            errors.append(f"candidate duplicates existing component: {name}")
        if candidate.get("component_type") != component_type:
            errors.append(f"candidate component_type mismatch: {name}")
        responsibility = str(candidate.get("responsibility", ""))
        if component_type in allowed_types and not responsibility.startswith(f"This {component_type} "):
            errors.append(f"responsibility must start with 'This {component_type} ': {name}")
        if responsibility.count(".") != 1 or not responsibility.endswith("."):
            errors.append(f"responsibility must be one sentence: {name}")
        if candidate.get("evidence_tag") not in allowed:
            errors.append(f"candidate evidence_tag is invalid: {name}")

    if len(set(candidate_names)) != len(candidate_names):
        errors.append("candidate names must be unique")
    if spec.get("recommended_candidate") not in candidate_names:
        errors.append("recommended_candidate must match one candidate name")


def validate_relationships(spec: dict[str, Any], type_policy: dict[str, Any], errors: list[str]) -> None:
    component_type = spec.get("component_type")
    relationships = spec.get("relationships")
    if not isinstance(relationships, dict):
        errors.append("relationships must be an object")
        return
    require_fields(relationships, ["direct_dependencies", "downstream_consumers", "diagram"], "relationships", errors)
    if not isinstance(relationships.get("direct_dependencies"), list):
        errors.append("relationships direct_dependencies must be a list")
    if not isinstance(relationships.get("downstream_consumers"), list):
        errors.append("relationships downstream_consumers must be a list")
    if component_type not in type_policy["component_types"]:
        return
    for field in type_policy["type_requirements"][component_type]:
        if relationships.get(field) in ("", [], None):
            errors.append(f"relationships missing {field} for {component_type}")
    if component_type == "agent" and len(relationships.get("managed_skills", [])) < 2:
        errors.append("agent concepts must manage at least two skills")
    if component_type == "hook":
        hook_type = relationships.get("hook_type")
        event = relationships.get("event")
        compatibility = type_policy["hook_event_compatibility"]
        if hook_type not in compatibility:
            errors.append(f"unsupported hook_type: {hook_type}")
        elif event not in compatibility[hook_type]:
            errors.append(f"hook event is incompatible with hook_type: {hook_type}/{event}")


def validate_conflict(spec: dict[str, Any], policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    conflict = spec.get("conflict_analysis")
    if not isinstance(conflict, dict):
        errors.append("conflict_analysis must be an object")
        return
    require_fields(conflict, ["status", "resolution", "rationale", "evidence_tag"], "conflict_analysis", errors)
    status = conflict.get("status")
    resolution = conflict.get("resolution")
    if status not in policy["statuses"]:
        errors.append(f"conflict status is invalid: {status}")
    if resolution not in policy["resolutions"]:
        errors.append(f"conflict resolution is invalid: {resolution}")
    if status == "none" and resolution != "none":
        errors.append("conflict resolution must be none when status is none")
    if status != "none" and resolution == "none":
        errors.append("conflict resolution cannot be none when status is not none")
    if conflict.get("evidence_tag") not in allowed or not has_evidence(conflict, allowed):
        errors.append("conflict_analysis missing valid evidence")


def validate_moat(spec: dict[str, Any], policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    moat = spec.get("moat_depth")
    if not isinstance(moat, dict):
        errors.append("moat_depth must be an object")
        return
    require_fields(moat, ["level", "complexity_score", "required_assets", "rationale", "evidence_tag"], "moat_depth", errors)
    level = moat.get("level")
    if level not in policy["levels"]:
        errors.append(f"moat depth level is invalid: {level}")
        return
    depth = policy["levels"][level]
    score = moat.get("complexity_score")
    if not isinstance(score, int) or not (depth["complexity_min"] <= score <= depth["complexity_max"]):
        errors.append("moat complexity_score does not fit the selected depth")
    if moat.get("required_assets") != depth["required_assets"]:
        errors.append("moat required_assets do not match selected depth")
    if moat.get("evidence_tag") not in allowed or not has_evidence(moat, allowed):
        errors.append("moat_depth missing valid evidence")


def validate_tools_and_size(spec: dict[str, Any], contract: dict[str, Any], moat_policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    tools = spec.get("tools_needed")
    if not isinstance(tools, list) or not tools:
        errors.append("tools_needed must be a non-empty list")
    else:
        seen = set()
        for item in tools:
            if not isinstance(item, dict):
                errors.append("tool entry must be an object")
                continue
            require_fields(item, ["tool", "reason"], "tool entry", errors)
            tool = item.get("tool")
            if tool not in contract["known_tools"]:
                errors.append(f"unknown tool: {tool}")
            if tool in seen:
                errors.append(f"duplicate tool: {tool}")
            seen.add(tool)
            if not has_evidence(item, allowed):
                errors.append(f"tool rationale missing evidence: {tool}")

    estimated = spec.get("estimated_lines")
    component_type = spec.get("component_type")
    if not isinstance(estimated, dict):
        errors.append("estimated_lines must be an object")
        return
    require_fields(estimated, ["min", "max"], "estimated_lines", errors)
    min_lines = estimated.get("min")
    max_lines = estimated.get("max")
    if not isinstance(min_lines, int) or not isinstance(max_lines, int) or min_lines > max_lines:
        errors.append("estimated_lines min/max are invalid")
        return
    if component_type in moat_policy["line_ranges"]:
        line_policy = moat_policy["line_ranges"][component_type]
        if min_lines < line_policy["min"] or max_lines > line_policy["max"]:
            errors.append("estimated_lines outside component type range")


def validate_output_sections(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    decision = spec.get("output_decision")
    if not isinstance(decision, dict):
        errors.append("output_decision must be an object")
    else:
        require_fields(decision, ["status", "next_action", "evidence_tag"], "output_decision", errors)
        if decision.get("status") not in contract["output_statuses"]:
            errors.append(f"output_decision status is invalid: {decision.get('status')}")
        if decision.get("next_action") not in contract["next_actions"]:
            errors.append(f"output_decision next_action is invalid: {decision.get('next_action')}")
        if decision.get("evidence_tag") not in allowed or not has_evidence(decision, allowed):
            errors.append("output_decision missing valid evidence")
    for section in ("validation", "risks"):
        if not has_evidence(spec.get(section), allowed):
            errors.append(f"{section} must include evidence tag")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an ideate-component concept-card JSON file")
    parser.add_argument("concept", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "concept-card-contract.json")
    type_policy = load_json(ASSETS / "component-type-policy.json")
    moat_policy = load_json(ASSETS / "moat-depth-policy.json")
    conflict_policy = load_json(ASSETS / "conflict-policy.json")
    allowed = set(contract["allowed_evidence_tags"])

    spec = load_json(args.concept)
    errors: list[str] = []
    if not isinstance(spec, dict):
        errors.append("concept root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in spec:
                errors.append(f"missing top-level field: {field}")
        if spec.get("skill") != "ideate-component":
            errors.append("skill must be ideate-component")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_date(str(spec["reference_date"]), errors)
    body = json.dumps(spec, ensure_ascii=False)
    for term in contract["moving_time_terms"]:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"concept must avoid moving time term: {term}")

    validate_plugin_context(spec, contract, allowed, errors)
    validate_candidates(spec, contract, set(type_policy["component_types"]), allowed, errors)
    validate_relationships(spec, type_policy, errors)
    validate_conflict(spec, conflict_policy, allowed, errors)
    validate_moat(spec, moat_policy, allowed, errors)
    validate_tools_and_size(spec, contract, moat_policy, allowed, errors)
    validate_output_sections(spec, contract, allowed, errors)

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(
        f"PASS {args.concept.name}: type={spec['component_type']} "
        f"candidate={spec['recommended_candidate']} moat={spec['moat_depth']['level']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
