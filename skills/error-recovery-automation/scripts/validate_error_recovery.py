#!/usr/bin/env python3
"""Validate deterministic error recovery plans for error-recovery-automation."""

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


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(is_non_empty_string(item) for item in value)


def require_object(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def validate(plan: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["plan must be a JSON object"]

    contract = policy("error-recovery-contract.json")
    classification = policy("classification-policy.json")
    retry_policy = policy("retry-policy.json")
    evidence_policy = policy("evidence-policy.json")

    required_top = contract["json_contract"]["required_top_level_fields"]
    for field in required_top:
        if field not in plan:
            errors.append(f"missing required field: {field}")

    if plan.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if plan.get("skill") != "error-recovery-automation":
        errors.append("skill must be error-recovery-automation")
    if not is_non_empty_string(plan.get("scenario_id")):
        errors.append("scenario_id must be a non-empty string")

    allowed_decisions = set(contract["json_contract"]["allowed_decisions"])
    decision = plan.get("decision")
    if decision not in allowed_decisions:
        errors.append(f"decision must be one of {sorted(allowed_decisions)}")

    error = require_object(plan, "error", errors)
    retry = require_object(plan, "retry", errors)
    rollback = require_object(plan, "rollback", errors)
    escalation = require_object(plan, "escalation", errors)
    evidence = require_object(plan, "evidence", errors)
    validation = require_object(plan, "validation", errors)
    safety = require_object(plan, "safety", errors)

    retryable = set(classification["retryable_categories"])
    non_retryable = set(classification["non_retryable_categories"])
    human_required = set(classification["human_required_categories"])
    allowed_categories = retryable | non_retryable | human_required
    recoverability_values = set(classification["recoverability_values"])

    category = error.get("category")
    recoverability = error.get("recoverability")
    if category not in allowed_categories:
        errors.append(f"error.category must be one of {sorted(allowed_categories)}")
    if recoverability not in recoverability_values:
        errors.append(f"error.recoverability must be one of {sorted(recoverability_values)}")
    if category in non_retryable and recoverability == "retryable":
        errors.append("non-retryable categories cannot be marked retryable")
    if category in human_required and recoverability != "human_required":
        errors.append("human-required categories must use human_required recoverability")

    retry_enabled = retry.get("enabled")
    if not isinstance(retry_enabled, bool):
        errors.append("retry.enabled must be a boolean")
    if retry_enabled:
        if decision != "recover":
            errors.append("enabled retry requires decision=recover")
        if category not in retryable or recoverability != "retryable":
            errors.append("enabled retry requires a retryable category and recoverability")
        max_attempts = retry.get("max_attempts")
        if not isinstance(max_attempts, int) or not 1 <= max_attempts <= retry_policy["max_attempts"]:
            errors.append(f"retry.max_attempts must be 1..{retry_policy['max_attempts']}")
        if retry.get("backoff_strategy") != retry_policy["strategy"]:
            errors.append(f"retry.backoff_strategy must be {retry_policy['strategy']}")
        base_delay = retry.get("base_delay_seconds")
        max_delay = retry.get("max_delay_seconds")
        if not isinstance(base_delay, int) or base_delay < 1:
            errors.append("retry.base_delay_seconds must be a positive integer")
        if not isinstance(max_delay, int) or max_delay < max(base_delay if isinstance(base_delay, int) else 1, 1):
            errors.append("retry.max_delay_seconds must be >= base_delay_seconds")
        elif max_delay > retry_policy["max_delay_seconds"]:
            errors.append(f"retry.max_delay_seconds must be <= {retry_policy['max_delay_seconds']}")
        if retry.get("jitter") not in retry_policy["allowed_jitter"]:
            errors.append(f"retry.jitter must be one of {retry_policy['allowed_jitter']}")
        if retry.get("jitter") == "deterministic" and "deterministic_seed" not in retry:
            errors.append("deterministic jitter requires deterministic_seed")
        if not is_string_list(retry.get("stop_conditions")):
            errors.append("retry.stop_conditions must be a non-empty list of strings")
    elif decision == "recover":
        errors.append("decision=recover requires retry.enabled=true")

    destructive_action = safety.get("destructive_action")
    approval_required = safety.get("approval_required")
    state_changed = safety.get("state_changed")
    idempotency_checked = safety.get("idempotency_checked")
    side_effects = safety.get("side_effects")
    if not isinstance(destructive_action, bool):
        errors.append("safety.destructive_action must be a boolean")
    if not isinstance(approval_required, bool):
        errors.append("safety.approval_required must be a boolean")
    if not isinstance(state_changed, bool):
        errors.append("safety.state_changed must be a boolean")
    if retry_enabled and idempotency_checked is not True:
        errors.append("enabled retry requires safety.idempotency_checked=true")
    if retry_enabled and side_effects not in {"none", "known_reversible"}:
        errors.append("enabled retry requires side_effects to be none or known_reversible")
    if destructive_action and not approval_required:
        errors.append("destructive actions require approval_required=true")
    if destructive_action and retry_enabled:
        errors.append("destructive actions cannot be retried automatically")

    rollback_required = rollback.get("required")
    if not isinstance(rollback_required, bool):
        errors.append("rollback.required must be a boolean")
    if state_changed or destructive_action or side_effects == "known_reversible":
        if rollback_required is not True:
            errors.append("stateful or destructive recovery requires rollback.required=true")
    if rollback_required:
        if not is_string_list(rollback.get("plan")):
            errors.append("rollback.plan must be a non-empty list of strings when required")
        if not is_string_list(rollback.get("verification")):
            errors.append("rollback.verification must be a non-empty list of strings when required")

    escalation_required = escalation.get("required")
    if not isinstance(escalation_required, bool):
        errors.append("escalation.required must be a boolean")
    must_escalate = decision == "escalate" or recoverability in {"not_retryable", "human_required"}
    if must_escalate and escalation_required is not True:
        errors.append("non-retryable or escalated plans require escalation.required=true")
    if escalation_required:
        if not is_non_empty_string(escalation.get("owner")):
            errors.append("escalation.owner must be a non-empty string when required")
        if not is_non_empty_string(escalation.get("trigger")):
            errors.append("escalation.trigger must be a non-empty string when required")
        if not is_string_list(escalation.get("handoff")):
            errors.append("escalation.handoff must be a non-empty list of strings when required")

    for field in evidence_policy["required_evidence_fields"]:
        if not is_non_empty_string(evidence.get(field)):
            errors.append(f"evidence.{field} must be a non-empty string")

    for field in evidence_policy["required_validation_fields"]:
        if not is_string_list(validation.get(field)):
            errors.append(f"validation.{field} must be a non-empty list of strings")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an error recovery JSON plan")
    parser.add_argument("plan", type=Path, help="Path to a JSON recovery plan")
    args = parser.parse_args()

    try:
        plan = load_json(args.plan)
        errors = validate(plan)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.plan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
