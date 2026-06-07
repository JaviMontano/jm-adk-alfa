#!/usr/bin/env python3
"""Validate deterministic AI CONOPS report packets offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.ai-conops.report.v1"
REQUIRED_TOP = {
    "schema",
    "system",
    "evidence",
    "vision",
    "stakeholders",
    "interaction_design",
    "business_value",
    "success_metrics",
    "operational_modes",
    "assumptions",
    "validation",
    "risks",
}
TAGS = {"[EXPLICIT]", "[INFERRED]", "[OPEN]"}
LEVEL_NAMES = {
    1: "Manual Operation",
    2: "Decision Support",
    3: "Shared Control",
    4: "Supervised Autonomy",
    5: "Full Autonomy",
}
PILLARS = {"technical", "business", "ux-ethics"}
REQUIRED_MODES = {"Startup", "Executing", "Degraded", "Recovery"}
ALLOWED_MODES = {"Configuration", "Startup", "Executing", "Monitoring", "Learning", "Shadow", "Degraded", "Recovery"}
CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "stakeholder_coverage",
    "metric_coverage",
    "mode_transitions",
}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def objects(value: Any, name: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for i, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{name}[{i}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def non_empty_strings(value: Any, name: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out = [item for item in value if isinstance(item, str) and item]
    require(len(out) == len(value), errors, f"{name} must contain only non-empty strings")
    return out


def validate_refs(refs: Any, known: set[str], owner: str, errors: list[str]) -> None:
    if refs is None:
        return
    ids = non_empty_strings(refs, f"{owner}.evidence_ids", errors)
    for ref in ids:
        require(ref in known, errors, f"{owner} references unknown evidence {ref}")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> set[str]:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    ids: set[str] = set()
    for item in evidence:
        eid = item.get("id")
        require(isinstance(eid, str) and bool(eid), errors, "evidence id required")
        if isinstance(eid, str):
            require(eid not in ids, errors, f"duplicate evidence id {eid}")
            ids.add(eid)
        require(item.get("tag") in TAGS, errors, f"evidence {eid} invalid tag")
        require(bool(item.get("source")), errors, f"evidence {eid} source required")
        require(bool(item.get("summary")), errors, f"evidence {eid} summary required")
    return ids


def validate_system(data: dict[str, Any], errors: list[str]) -> None:
    system = data.get("system")
    require(isinstance(system, dict), errors, "system must be object")
    if not isinstance(system, dict):
        return
    for field in ("name", "domain", "purpose"):
        require(isinstance(system.get(field), str) and bool(system.get(field)), errors, f"system.{field} required")
    scope = system.get("scope")
    require(isinstance(scope, dict), errors, "system.scope must be object")
    if isinstance(scope, dict):
        require(bool(non_empty_strings(scope.get("includes"), "system.scope.includes", errors)), errors, "system.scope.includes required")
        require(isinstance(scope.get("excludes"), list), errors, "system.scope.excludes must be list")


def validate_vision(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    vision = data.get("vision")
    require(isinstance(vision, dict), errors, "vision must be object")
    if not isinstance(vision, dict):
        return
    require(bool(vision.get("problem_statement")), errors, "vision.problem_statement required")
    require(bool(non_empty_strings(vision.get("objectives"), "vision.objectives", errors)), errors, "vision.objectives required")
    require(bool(non_empty_strings(vision.get("success_criteria"), "vision.success_criteria", errors)), errors, "vision.success_criteria required")
    validate_refs(vision.get("evidence_ids"), evidence_ids, "vision", errors)


def validate_stakeholders(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    stakeholders = objects(data.get("stakeholders"), "stakeholders", errors)
    require(len(stakeholders) >= 3, errors, "at least 3 stakeholders required")
    seen: set[str] = set()
    for stakeholder in stakeholders:
        sid = stakeholder.get("id")
        require(isinstance(sid, str) and bool(sid), errors, "stakeholder id required")
        if isinstance(sid, str):
            require(sid not in seen, errors, f"duplicate stakeholder id {sid}")
            seen.add(sid)
        for field in ("name", "role"):
            require(isinstance(stakeholder.get(field), str) and bool(stakeholder.get(field)), errors, f"stakeholder {sid} missing {field}")
        require(bool(non_empty_strings(stakeholder.get("concerns"), f"stakeholder {sid}.concerns", errors)), errors, f"stakeholder {sid} concerns required")
        require(bool(non_empty_strings(stakeholder.get("decision_rights"), f"stakeholder {sid}.decision_rights", errors)), errors, f"stakeholder {sid} decision_rights required")
        validate_refs(stakeholder.get("evidence_ids"), evidence_ids, f"stakeholder {sid}", errors)


def normalize(values: Any) -> set[str]:
    if not isinstance(values, list):
        return set()
    return {str(item).strip().lower() for item in values}


def validate_interaction(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    interaction = data.get("interaction_design")
    require(isinstance(interaction, dict), errors, "interaction_design must be object")
    if not isinstance(interaction, dict):
        return
    level = interaction.get("default_level")
    require(isinstance(level, int) and level in LEVEL_NAMES, errors, "interaction_design.default_level must be 1..5")
    if isinstance(level, int) and level in LEVEL_NAMES:
        require(interaction.get("level_name") == LEVEL_NAMES[level], errors, "interaction_design.level_name mismatch")
    require(interaction.get("decision_stakes") in {"low", "medium", "high"}, errors, "interaction_design.decision_stakes invalid")
    require(bool(interaction.get("rationale")), errors, "interaction_design.rationale required")
    controls = normalize(interaction.get("controls"))
    require(bool(controls), errors, "interaction_design.controls required")
    require(bool(non_empty_strings(interaction.get("escalation_conditions"), "interaction_design.escalation_conditions", errors)), errors, "interaction_design.escalation_conditions required")
    if interaction.get("decision_stakes") == "high":
        require({"human override", "audit trail"}.issubset(controls), errors, "high-stakes interaction requires human override and audit trail")
    if isinstance(level, int) and level >= 4:
        require({"monitoring", "rollback", "audit trail"}.issubset(controls), errors, "Level 4/5 requires monitoring, rollback, and audit trail")
    validate_refs(interaction.get("evidence_ids"), evidence_ids, "interaction_design", errors)


def expected_quadrant(value_score: int, effort_score: int) -> str:
    if value_score >= 4 and effort_score <= 2:
        return "Quick Wins"
    if value_score >= 4 and effort_score >= 3:
        return "Strategic Investments"
    if value_score <= 3 and effort_score <= 2:
        return "Low Priority"
    return "Avoid/Reconsider"


def validate_business_value(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    value = data.get("business_value")
    require(isinstance(value, dict), errors, "business_value must be object")
    if not isinstance(value, dict):
        return
    value_score = value.get("value_score")
    effort_score = value.get("effort_score")
    require(isinstance(value_score, int) and 1 <= value_score <= 5, errors, "business_value.value_score must be 1..5")
    require(isinstance(effort_score, int) and 1 <= effort_score <= 5, errors, "business_value.effort_score must be 1..5")
    require(value.get("quadrant") in {"Quick Wins", "Strategic Investments", "Low Priority", "Avoid/Reconsider"}, errors, "business_value.quadrant invalid")
    if isinstance(value_score, int) and isinstance(effort_score, int):
        require(value.get("quadrant") == expected_quadrant(value_score, effort_score), errors, "business_value.quadrant does not match value/effort scores")
    require(bool(value.get("rationale")), errors, "business_value.rationale required")
    validate_refs(value.get("evidence_ids"), evidence_ids, "business_value", errors)


def validate_metrics(data: dict[str, Any], errors: list[str]) -> None:
    metrics = objects(data.get("success_metrics"), "success_metrics", errors)
    pillars = {metric.get("pillar") for metric in metrics}
    require(PILLARS.issubset(pillars), errors, "success_metrics must cover technical, business, and ux-ethics")
    seen: set[str] = set()
    for metric in metrics:
        mid = metric.get("id")
        require(isinstance(mid, str) and bool(mid), errors, "metric id required")
        if isinstance(mid, str):
            require(mid not in seen, errors, f"duplicate metric id {mid}")
            seen.add(mid)
        require(metric.get("pillar") in PILLARS, errors, f"metric {mid} invalid pillar")
        for field in ("name", "threshold", "objective", "frequency", "owner"):
            require(isinstance(metric.get(field), str) and bool(metric.get(field)), errors, f"metric {mid} missing {field}")


def validate_modes(data: dict[str, Any], errors: list[str]) -> None:
    modes = objects(data.get("operational_modes"), "operational_modes", errors)
    names = {mode.get("mode") for mode in modes}
    require(REQUIRED_MODES.issubset(names), errors, "operational_modes missing required modes")
    for mode in modes:
        name = mode.get("mode")
        require(name in ALLOWED_MODES, errors, f"operational mode {name} invalid")
        require(bool(non_empty_strings(mode.get("triggers"), f"mode {name}.triggers", errors)), errors, f"mode {name} triggers required")
        require(bool(non_empty_strings(mode.get("exit_criteria"), f"mode {name}.exit_criteria", errors)), errors, f"mode {name} exit_criteria required")
        require(isinstance(mode.get("owner"), str) and bool(mode.get("owner")), errors, f"mode {name} owner required")


def validate_assumptions(data: dict[str, Any], errors: list[str]) -> None:
    assumptions = objects(data.get("assumptions"), "assumptions", errors)
    require(bool(assumptions), errors, "assumptions required")
    for item in assumptions:
        aid = item.get("id")
        require(isinstance(aid, str) and bool(aid), errors, "assumption id required")
        require(bool(item.get("statement")), errors, f"assumption {aid} statement required")
        require(item.get("status") in {"open", "validated", "rejected"}, errors, f"assumption {aid} status invalid")
        require(bool(item.get("owner")), errors, f"assumption {aid} owner required")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if not isinstance(validation, dict):
        return
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    checks = validation.get("checks")
    require(isinstance(checks, list), errors, "validation.checks must be list")
    if isinstance(checks, list):
        require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    evidence_ids = validate_evidence(data, errors)
    validate_system(data, errors)
    validate_vision(data, evidence_ids, errors)
    validate_stakeholders(data, evidence_ids, errors)
    validate_interaction(data, evidence_ids, errors)
    validate_business_value(data, evidence_ids, errors)
    validate_metrics(data, errors)
    validate_modes(data, errors)
    validate_assumptions(data, errors)
    validate_validation(data, errors)
    require(isinstance(data.get("risks"), list), errors, "risks must be list")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_ai_conops_report.py <report.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data if isinstance(data, dict) else {})
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
