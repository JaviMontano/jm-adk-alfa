#!/usr/bin/env python3
"""Validate deterministic discovery-orchestration packet fixtures."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def iso_date(value: str, field: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must be ISO date: {value}")
        return None


def has_evidence(value: object, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item, allowed) for item in value.values())
    return False


def has_cycle(nodes: set[str], edges: list[tuple[str, str]]) -> bool:
    graph = {node: [] for node in nodes}
    for source, target in edges:
        graph.setdefault(source, []).append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for target in graph.get(node, []):
            if visit(target):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a discovery orchestration packet JSON file")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()

    pipeline_schema = load_json(ASSETS / "pipeline-schema.json")
    gate_policy = load_json(ASSETS / "gate-policy.json")
    deliverable_policy = load_json(ASSETS / "deliverable-policy.json")
    dependency_policy = load_json(ASSETS / "dependency-policy.json")
    status_taxonomy = load_json(ASSETS / "status-taxonomy.json")
    contract = load_json(ASSETS / "report-contract.json")

    allowed_tags = set(status_taxonomy["allowed_evidence_tags"])
    packet = load_json(args.packet)
    errors: list[str] = []
    if not isinstance(packet, dict):
        errors.append("packet root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in packet:
                errors.append(f"missing top-level field: {field}")
        if packet.get("skill") != "discovery-orchestration":
            errors.append("skill must be discovery-orchestration")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    iso_date(str(packet["reference_date"]), "reference_date", errors)
    if not has_evidence(packet.get("summary"), allowed_tags):
        errors.append("summary must include evidence tag")

    pipeline = packet.get("pipeline")
    if not isinstance(pipeline, dict):
        errors.append("pipeline must be an object")
        pipeline = {}
    for field in pipeline_schema["required_pipeline_fields"]:
        if not pipeline.get(field):
            errors.append(f"pipeline missing {field}")
    if pipeline.get("status") not in status_taxonomy["pipeline_statuses"]:
        errors.append("pipeline has invalid status")

    phases = packet.get("phases")
    if not isinstance(phases, list) or not phases:
        errors.append("phases must be a non-empty list")
        phases = []
    phase_ids = {str(phase.get("id")) for phase in phases if isinstance(phase, dict)}
    for phase in phases:
        if not isinstance(phase, dict):
            errors.append("each phase must be an object")
            continue
        for field in pipeline_schema["required_phase_fields"]:
            if phase.get(field) in ("", [], None):
                errors.append(f"phase {phase.get('id')} missing {field}")
        if phase.get("status") not in status_taxonomy["phase_statuses"]:
            errors.append(f"phase {phase.get('id')} invalid status")

    sequence = packet.get("skill_sequence")
    if not isinstance(sequence, list) or not sequence:
        errors.append("skill_sequence must be a non-empty list")
        sequence = []
    skill_names = {str(item.get("skill")) for item in sequence if isinstance(item, dict)}
    for item in sequence:
        if not isinstance(item, dict):
            errors.append("each skill_sequence entry must be an object")
            continue
        skill = str(item.get("skill", ""))
        for field in pipeline_schema["required_skill_fields"]:
            if field not in item or item[field] in ("", None):
                errors.append(f"skill_sequence {skill or '<missing-skill>'} missing {field}")
        if item.get("phase") not in phase_ids:
            errors.append(f"skill_sequence {skill} references unknown phase")
        if item.get("evidence_tag") not in allowed_tags:
            errors.append(f"skill_sequence {skill} invalid evidence_tag")
        if not item.get("owner"):
            errors.append(f"skill_sequence {skill} missing owner")

    dependencies = packet.get("dependencies")
    if not isinstance(dependencies, list):
        errors.append("dependencies must be a list")
        dependencies = []
    edges: list[tuple[str, str]] = []
    for dep in dependencies:
        if not isinstance(dep, dict):
            errors.append("each dependency must be an object")
            continue
        for field in dependency_policy["required_fields"]:
            if not dep.get(field):
                errors.append(f"dependency missing {field}")
        source = str(dep.get("from", ""))
        target = str(dep.get("to", ""))
        if source not in skill_names or target not in skill_names:
            errors.append(f"dependency {source}->{target} references unknown skill")
        if dep.get("type") not in dependency_policy["types"]:
            errors.append(f"dependency {source}->{target} invalid type")
        if dep.get("evidence_tag") not in allowed_tags:
            errors.append(f"dependency {source}->{target} invalid evidence_tag")
        if dep.get("type") == "blocks":
            edges.append((source, target))
    if has_cycle(skill_names, edges):
        errors.append("dependency graph contains a cycle")

    gates = packet.get("gates")
    if not isinstance(gates, list):
        errors.append("gates must be a list")
        gates = []
    gated_phases = {str(gate.get("before_phase")) for gate in gates if isinstance(gate, dict)}
    for gate in gates:
        if not isinstance(gate, dict):
            errors.append("each gate must be an object")
            continue
        for field in gate_policy["required_gate_fields"]:
            if gate.get(field) in ("", [], None):
                errors.append(f"gate {gate.get('id')} missing {field}")
        if gate.get("before_phase") not in phase_ids:
            errors.append(f"gate {gate.get('id')} references unknown phase")
        if gate.get("status") not in gate_policy["gate_statuses"]:
            errors.append(f"gate {gate.get('id')} invalid status")
        if gate.get("evidence_tag") not in allowed_tags:
            errors.append(f"gate {gate.get('id')} invalid evidence_tag")
    ordered_phase_ids = [str(phase.get("id")) for phase in phases if isinstance(phase, dict)]
    for phase_id in ordered_phase_ids[1:]:
        if phase_id not in gated_phases:
            errors.append(f"phase {phase_id} missing transition gate")

    deliverables = packet.get("deliverables")
    if not isinstance(deliverables, list) or not deliverables:
        errors.append("deliverables must be a non-empty list")
        deliverables = []
    for deliverable in deliverables:
        if not isinstance(deliverable, dict):
            errors.append("each deliverable must be an object")
            continue
        did = str(deliverable.get("id", ""))
        for field in deliverable_policy["required_fields"]:
            if deliverable.get(field) in ("", [], None):
                errors.append(f"deliverable {did or '<missing-id>'} missing {field}")
        if deliverable.get("source_skill") not in skill_names:
            errors.append(f"deliverable {did} references unknown source_skill")
        if deliverable.get("status") not in deliverable_policy["statuses"]:
            errors.append(f"deliverable {did} invalid status")
        if deliverable.get("evidence_tag") not in allowed_tags:
            errors.append(f"deliverable {did} invalid evidence_tag")
        if pipeline.get("status") == "ready" and deliverable.get("status") != "validated":
            errors.append(f"ready pipeline has unvalidated deliverable {did}")

    blockers = packet.get("blockers")
    if pipeline.get("status") == "blocked":
        if not isinstance(blockers, list) or not blockers:
            errors.append("blocked pipeline requires blockers")
        elif not has_evidence(blockers, allowed_tags):
            errors.append("blockers must include evidence tag")
    if pipeline.get("status") == "ready":
        if any(isinstance(gate, dict) and gate.get("status") != "pass" for gate in gates):
            errors.append("ready pipeline requires all gates to pass")

    for section in ["validation", "risks"]:
        if not has_evidence(packet.get(section), allowed_tags):
            errors.append(f"{section} must include evidence tag")

    moving_terms = re.compile(r"\b(today|tomorrow|yesterday|soon|recently|later|TBD)\b", re.IGNORECASE)
    if moving_terms.search(json.dumps(packet, ensure_ascii=False)):
        errors.append("packet must avoid moving time or TBD language")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.packet.name}: phases={len(phases)} skills={len(sequence)} gates={len(gates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
