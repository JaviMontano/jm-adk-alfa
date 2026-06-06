#!/usr/bin/env python3
"""Validate deterministic AI workflow automation plan fixtures."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ALLOWED_EVIDENCE = {"[CONFIG]", "[DOC]", "[CÓDIGO]", "[INFERENCIA]", "[SUPUESTO]"}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def iso_date(value: str, field: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must be ISO date: {value}")
        return None


def has_evidence(value: object) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in ALLOWED_EVIDENCE)
    if isinstance(value, list):
        return any(has_evidence(item) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item) for item in value.values())
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI workflow automation plan JSON file")
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()

    workflow_schema = load_json(ASSETS / "workflow-schema.json")
    actor_taxonomy = load_json(ASSETS / "actor-taxonomy.json")
    approval_policy = load_json(ASSETS / "approval-gate-policy.json")
    handoff_policy = load_json(ASSETS / "handoff-policy.json")
    failure_policy = load_json(ASSETS / "failure-policy.json")
    contract = load_json(ASSETS / "report-contract.json")

    plan = load_json(args.plan)
    errors: list[str] = []
    if not isinstance(plan, dict):
        errors.append("plan root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in plan:
                errors.append(f"missing top-level field: {field}")
        if plan.get("skill") != "ai-workflow-automation":
            errors.append("skill must be ai-workflow-automation")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    iso_date(str(plan["reference_date"]), "reference_date", errors)
    if not has_evidence(plan.get("summary")):
        errors.append("summary must include an allowed evidence tag")

    actors = plan.get("actors")
    if not isinstance(actors, list) or not actors:
        errors.append("actors must be a non-empty list")
        actors = []
    actor_ids = {str(actor.get("id")) for actor in actors if isinstance(actor, dict)}
    allowed_actors = set(actor_taxonomy["actors"])
    for actor in actors:
        if not isinstance(actor, dict):
            errors.append("each actor must be an object")
            continue
        if actor.get("type") not in allowed_actors:
            errors.append(f"actor {actor.get('id')} has invalid type")
        if not actor.get("owner"):
            errors.append(f"actor {actor.get('id')} missing owner")

    steps = plan.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("steps must be a non-empty list")
        steps = []
    step_ids = {str(step.get("id")) for step in steps if isinstance(step, dict)}
    gated_steps = {str(gate.get("before_step")) for gate in plan.get("approval_gates", []) if isinstance(gate, dict)}
    max_retry = int(failure_policy["max_retry_limit"])
    required_approval_risk = set(approval_policy["required_for_risk"])
    for step in steps:
        if not isinstance(step, dict):
            errors.append("each step must be an object")
            continue
        step_id = str(step.get("id", ""))
        for field in workflow_schema["required_step_fields"]:
            if field not in step or step[field] in ("", [], None):
                errors.append(f"step {step_id or '<missing-id>'} missing {field}")
        if step.get("actor") not in actor_ids:
            errors.append(f"step {step_id} references unknown actor")
        if step.get("risk_level") not in workflow_schema["risk_levels"]:
            errors.append(f"step {step_id} has invalid risk_level")
        retry_limit = step.get("retry_limit")
        if not isinstance(retry_limit, int) or retry_limit < 0 or retry_limit > max_retry:
            errors.append(f"step {step_id} retry_limit must be between 0 and {max_retry}")
        if step.get("risk_level") in required_approval_risk and step.get("requires_approval") is not True:
            errors.append(f"step {step_id} high-risk step must require approval")
        if step.get("requires_approval") is True and step_id not in gated_steps:
            errors.append(f"step {step_id} requires approval but has no gate")
        actor = next((item for item in actors if isinstance(item, dict) and item.get("id") == step.get("actor")), {})
        if actor.get("type") == "ai":
            for field in contract["required_ai_step_fields"]:
                if not step.get(field):
                    errors.append(f"AI step {step_id} missing {field}")
        if not str(step.get("fallback", "")).strip():
            errors.append(f"step {step_id} missing fallback")

    approval_gates = plan.get("approval_gates")
    if not isinstance(approval_gates, list):
        errors.append("approval_gates must be a list")
        approval_gates = []
    expected_decisions = set(approval_policy["decision_values"])
    for gate in approval_gates:
        if not isinstance(gate, dict):
            errors.append("each approval gate must be an object")
            continue
        for field in approval_policy["required_gate_fields"]:
            if field not in gate or gate[field] in ("", [], None):
                errors.append(f"approval gate {gate.get('id')} missing {field}")
        if gate.get("before_step") not in step_ids:
            errors.append(f"approval gate {gate.get('id')} references unknown step")
        if set(gate.get("decision_values", [])) != expected_decisions:
            errors.append(f"approval gate {gate.get('id')} decision_values mismatch")
        if gate.get("evidence_tag") not in ALLOWED_EVIDENCE:
            errors.append(f"approval gate {gate.get('id')} invalid evidence_tag")

    handoffs = plan.get("handoffs")
    if not isinstance(handoffs, list):
        errors.append("handoffs must be a list")
        handoffs = []
    for handoff in handoffs:
        if not isinstance(handoff, dict):
            errors.append("each handoff must be an object")
            continue
        for field in handoff_policy["required_fields"]:
            if field not in handoff or handoff[field] in ("", [], None):
                errors.append(f"handoff {handoff.get('id')} missing {field}")
        if handoff.get("from_actor") not in actor_ids or handoff.get("to_actor") not in actor_ids:
            errors.append(f"handoff {handoff.get('id')} references unknown actor")
        if handoff.get("evidence_tag") not in ALLOWED_EVIDENCE:
            errors.append(f"handoff {handoff.get('id')} invalid evidence_tag")

    if not isinstance(plan.get("fallbacks"), list) or not plan["fallbacks"]:
        errors.append("fallbacks must be a non-empty list")

    for section in ["validation", "risks"]:
        if not has_evidence(plan.get(section)):
            errors.append(f"{section} must include an allowed evidence tag")

    moving_terms = re.compile(r"\b(today|tomorrow|yesterday|soon|recently|until it works|retry forever|keep trying)\b", re.IGNORECASE)
    if moving_terms.search(json.dumps(plan, ensure_ascii=False)):
        errors.append("plan must avoid moving time words and unbounded retry language")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.plan.name}: steps={len(steps)} gates={len(approval_gates)} handoffs={len(handoffs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
