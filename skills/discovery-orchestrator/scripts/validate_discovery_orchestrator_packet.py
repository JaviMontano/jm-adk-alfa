#!/usr/bin/env python3
"""Validate deterministic discovery-orchestrator packet fixtures."""

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


def add_if(condition: bool, errors: list[str], message: str) -> None:
    if condition:
        errors.append(message)


def has_evidence(value: Any, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item, allowed) for item in value.values())
    return False


def iter_values(value: Any) -> list[Any]:
    values: list[Any] = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(iter_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(iter_values(item))
    return values


def iter_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            keys.append(str(key))
            keys.extend(iter_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.extend(iter_keys(item))
    return keys


def require_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if obj.get(field) in ("", [], None):
            errors.append(f"{label} missing {field}")


def validate_reference_date(packet: dict[str, Any], errors: list[str]) -> None:
    value = str(packet.get("reference_date", ""))
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"reference_date must be ISO date: {value}")


def validate_no_moving_terms(packet: dict[str, Any], terms: list[str], errors: list[str]) -> None:
    body = json.dumps(packet, ensure_ascii=False)
    for term in terms:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"packet must avoid moving time term: {term}")


def validate_no_prices(packet: dict[str, Any], boundary: dict[str, Any], errors: list[str]) -> None:
    forbidden_keys = {str(key).lower() for key in boundary["forbidden_price_fields"]}
    for key in iter_keys(packet):
        if key.lower() in forbidden_keys:
            errors.append(f"forbidden price field: {key}")
    body = json.dumps(packet, ensure_ascii=False)
    for pattern in boundary["forbidden_price_patterns"]:
        if re.search(pattern, body, flags=re.IGNORECASE):
            errors.append(f"forbidden price pattern: {pattern}")


def validate_phase_plan(
    packet: dict[str, Any],
    phase_contract: dict[str, Any],
    allowed_tags: set[str],
    errors: list[str],
) -> set[str]:
    phases = packet.get("phase_plan")
    if not isinstance(phases, list) or not phases:
        errors.append("phase_plan must be a non-empty list")
        return set()

    required_ids = list(phase_contract["required_phase_ids"])
    rank = {phase: index for index, phase in enumerate(phase_contract["phase_order"])}
    seen: list[str] = []
    for phase in phases:
        if not isinstance(phase, dict):
            errors.append("each phase_plan entry must be an object")
            continue
        phase_id = str(phase.get("id", ""))
        require_fields(phase, phase_contract["required_phase_fields"], f"phase {phase_id or '<missing-id>'}", errors)
        if phase_id not in rank:
            errors.append(f"phase {phase_id} is not canonical")
        if phase.get("status") not in phase_contract["statuses"]:
            errors.append(f"phase {phase_id} invalid status")
        if phase.get("evidence_tag") not in allowed_tags:
            errors.append(f"phase {phase_id} invalid evidence_tag")
        if not has_evidence(phase.get("purpose"), allowed_tags):
            errors.append(f"phase {phase_id} purpose must include evidence tag")
        seen.append(phase_id)

    missing = [phase_id for phase_id in required_ids if phase_id not in seen]
    if missing:
        errors.append(f"phase_plan missing required phases: {', '.join(missing)}")
    ordered = [rank[phase_id] for phase_id in seen if phase_id in rank]
    if ordered != sorted(ordered):
        errors.append("phase_plan must follow canonical phase order")
    return set(seen)


def validate_skill_sequence(
    packet: dict[str, Any],
    sequence_contract: dict[str, Any],
    phase_ids: set[str],
    allowed_tags: set[str],
    errors: list[str],
) -> set[str]:
    sequence = packet.get("skill_sequence")
    if not isinstance(sequence, list) or not sequence:
        errors.append("skill_sequence must be a non-empty list")
        return set()

    canonical = {
        str(item["skill"]): set(item["allowed_phases"])
        for item in sequence_contract["canonical_skills"]
    }
    seen_ids: set[str] = set()
    for item in sequence:
        if not isinstance(item, dict):
            errors.append("each skill_sequence entry must be an object")
            continue
        skill_id = str(item.get("id", ""))
        skill = str(item.get("skill", ""))
        phase = str(item.get("phase", ""))
        required_sequence_fields = [
            field for field in sequence_contract["required_sequence_fields"] if field != "depends_on"
        ]
        require_fields(item, required_sequence_fields, f"skill_sequence {skill or '<missing-skill>'}", errors)
        if "depends_on" not in item:
            errors.append(f"skill_sequence {skill or '<missing-skill>'} missing depends_on")
        if skill_id in seen_ids:
            errors.append(f"duplicate skill_sequence id: {skill_id}")
        seen_ids.add(skill_id)
        if skill not in canonical:
            errors.append(f"skill_sequence {skill} is not canonical")
        elif phase not in canonical[skill]:
            errors.append(f"skill_sequence {skill} cannot run in phase {phase}")
        if phase not in phase_ids:
            errors.append(f"skill_sequence {skill} references unknown phase {phase}")
        if item.get("operation") not in sequence_contract["operations"]:
            errors.append(f"skill_sequence {skill} invalid operation")
        if item.get("status") not in sequence_contract["statuses"]:
            errors.append(f"skill_sequence {skill} invalid status")
        if item.get("evidence_tag") not in allowed_tags:
            errors.append(f"skill_sequence {skill} invalid evidence_tag")
        if not isinstance(item.get("depends_on"), list):
            errors.append(f"skill_sequence {skill} depends_on must be a list")
        if not isinstance(item.get("produces"), list) or not item.get("produces"):
            errors.append(f"skill_sequence {skill} produces must be a non-empty list")
        for forbidden in ("analysis_output", "domain_findings", "implementation_steps"):
            if forbidden in item:
                errors.append(f"skill_sequence {skill} contains forbidden field {forbidden}")

    for item in sequence:
        if not isinstance(item, dict):
            continue
        for dep in item.get("depends_on", []):
            if dep not in seen_ids:
                errors.append(f"skill_sequence {item.get('id')} depends on unknown id {dep}")
    return seen_ids


def validate_g1(gate: dict[str, Any], errors: list[str]) -> None:
    criteria = gate.get("criteria") if isinstance(gate.get("criteria"), dict) else {}
    status = gate.get("status")
    ratio = criteria.get("assumption_ratio")
    if isinstance(ratio, (int, float)) and ratio > 0.30 and criteria.get("warning_banner") is not True:
        errors.append("G1 assumption_ratio above 0.30 requires warning_banner")

    if status == "pass":
        add_if(criteria.get("scenario_count", 0) < 3, errors, "G1 pass requires at least 3 scenarios")
        add_if(criteria.get("scoring_complete") is not True, errors, "G1 pass requires complete scoring")
        add_if(criteria.get("decision_tree_present") is not True, errors, "G1 pass requires decision tree")
        add_if(not criteria.get("recommended_scenario_id"), errors, "G1 pass requires recommended_scenario_id")
        add_if(criteria.get("assumption_count", 0) < 3, errors, "G1 pass requires at least 3 assumptions")
        approval = criteria.get("approval")
        approved = isinstance(approval, dict) and approval.get("status") == "approved"
        add_if(not approved, errors, "G1 pass requires explicit approval")
    elif status == "block":
        add_if(not gate.get("blockers"), errors, "G1 block requires blockers")
        add_if(not gate.get("next_action"), errors, "G1 block requires next_action")


def validate_feasibility_checkpoint(gate: dict[str, Any], errors: list[str]) -> None:
    if gate.get("status") != "pass":
        return
    criteria = gate.get("criteria") if isinstance(gate.get("criteria"), dict) else {}
    technical = criteria.get("technical_verdict")
    software = criteria.get("software_verdict")
    if technical not in {"FEASIBLE", "FEASIBLE_WITH_CONDITIONS"}:
        errors.append("G1B pass requires feasible technical verdict")
    if software not in {"SUBSTANCIA", "PROMESA_VIABLE"}:
        errors.append("G1B pass requires viable software verdict")


def validate_later_gate(gate: dict[str, Any], errors: list[str]) -> None:
    if gate.get("status") != "pass":
        return
    criteria = gate.get("criteria") if isinstance(gate.get("criteria"), dict) else {}
    gate_id = gate.get("gate_id")
    if gate_id == "G2":
        add_if(criteria.get("roadmap_present") is not True, errors, "G2 pass requires roadmap")
        add_if(criteria.get("prerequisites_present") is not True, errors, "G2 pass requires prerequisites")
        add_if(criteria.get("effort_model") != "fte_months", errors, "G2 pass requires effort_model fte_months")
        approval = criteria.get("sponsor_approval")
        add_if(not isinstance(approval, dict) or approval.get("status") != "approved", errors, "G2 pass requires sponsor approval")
    if gate_id == "G3":
        add_if(criteria.get("proposal_qa_passed") is not True, errors, "G3 pass requires proposal QA")
        add_if(criteria.get("risk_review_complete") is not True, errors, "G3 pass requires risk review")
        add_if(criteria.get("deliverable_register_complete") is not True, errors, "G3 pass requires deliverable register")
        approval = criteria.get("client_approval")
        add_if(not isinstance(approval, dict) or approval.get("status") != "approved", errors, "G3 pass requires client approval")


def validate_gates(
    packet: dict[str, Any],
    gate_policy: dict[str, Any],
    phase_ids: set[str],
    allowed_tags: set[str],
    errors: list[str],
) -> None:
    gates = packet.get("gates")
    if not isinstance(gates, list) or not gates:
        errors.append("gates must be a non-empty list")
        return
    seen = set()
    for gate in gates:
        if not isinstance(gate, dict):
            errors.append("each gate must be an object")
            continue
        gate_id = str(gate.get("gate_id", ""))
        seen.add(gate_id)
        require_fields(gate, gate_policy["required_gate_fields"], f"gate {gate_id or '<missing-id>'}", errors)
        if gate.get("status") not in gate_policy["gate_statuses"]:
            errors.append(f"gate {gate_id} invalid status")
        if gate.get("after_phase") not in phase_ids or gate.get("before_phase") not in phase_ids:
            errors.append(f"gate {gate_id} references unknown phase")
        if gate.get("evidence_tag") not in allowed_tags:
            errors.append(f"gate {gate_id} invalid evidence_tag")
        if not has_evidence(gate.get("decision"), allowed_tags):
            errors.append(f"gate {gate_id} decision must include evidence tag")
        if gate_id == "G1":
            validate_g1(gate, errors)
        elif gate_id == "G1B":
            validate_feasibility_checkpoint(gate, errors)
        else:
            validate_later_gate(gate, errors)
    if "G1" not in seen:
        errors.append("gates must include G1")


def validate_handoff(
    packet: dict[str, Any],
    contract: dict[str, Any],
    sequence_ids: set[str],
    allowed_tags: set[str],
    errors: list[str],
) -> None:
    handoff = packet.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("handoff must be an object")
        return
    require_fields(handoff, contract["handoff_required_fields"], "handoff", errors)
    if handoff.get("handover_gate") not in contract["handover_gate_statuses"]:
        errors.append("handoff has invalid handover_gate")
    if not has_evidence(handoff.get("next_action"), allowed_tags):
        errors.append("handoff next_action must include evidence tag")
    if not isinstance(handoff.get("deliverables_expected"), list) or not handoff.get("deliverables_expected"):
        errors.append("handoff deliverables_expected must be a non-empty list")
    if handoff.get("next_skill_id") and handoff.get("next_skill_id") not in sequence_ids:
        errors.append("handoff next_skill_id references unknown skill_sequence id")


def validate_boundary_checks(packet: dict[str, Any], boundary: dict[str, Any], errors: list[str]) -> None:
    checks = packet.get("boundary_checks")
    if not isinstance(checks, dict):
        errors.append("boundary_checks must be an object")
        return
    for field in boundary["required_boundary_checks"]:
        if checks.get(field) is not True:
            errors.append(f"boundary_checks {field} must be true")
    for field in boundary["forbidden_top_level_fields"]:
        if field in packet:
            errors.append(f"forbidden top-level field: {field}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a discovery-orchestrator packet JSON file")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "report-contract.json")
    phase_contract = load_json(ASSETS / "phase-contract.json")
    sequence_contract = load_json(ASSETS / "skill-sequence-contract.json")
    gate_policy = load_json(ASSETS / "gate-policy.json")
    boundary = load_json(ASSETS / "non-analysis-boundary.json")
    allowed_tags = set(contract["allowed_evidence_tags"])

    packet = load_json(args.packet)
    errors: list[str] = []
    if not isinstance(packet, dict):
        errors.append("packet root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in packet:
                errors.append(f"missing top-level field: {field}")
        if packet.get("skill") != "discovery-orchestrator":
            errors.append("skill must be discovery-orchestrator")
        if packet.get("mode") not in contract["modes"]:
            errors.append("mode is not allowed")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_reference_date(packet, errors)
    validate_no_moving_terms(packet, contract["moving_time_terms"], errors)
    validate_no_prices(packet, boundary, errors)
    validate_boundary_checks(packet, boundary, errors)

    for section in ("summary", "validation", "risks"):
        if not has_evidence(packet.get(section), allowed_tags):
            errors.append(f"{section} must include evidence tag")

    phase_ids = validate_phase_plan(packet, phase_contract, allowed_tags, errors)
    sequence_ids = validate_skill_sequence(packet, sequence_contract, phase_ids, allowed_tags, errors)
    validate_gates(packet, gate_policy, phase_ids, allowed_tags, errors)
    validate_handoff(packet, contract, sequence_ids, allowed_tags, errors)

    for value in iter_values(packet):
        if isinstance(value, str) and len(value.strip()) > 0 and "[OPEN]" in value:
            errors.append("packet must use canonical evidence tags instead of [OPEN]")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.packet.name}: phases={len(packet['phase_plan'])} skills={len(packet['skill_sequence'])} gates={len(packet['gates'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
