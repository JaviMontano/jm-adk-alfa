#!/usr/bin/env python3
"""Validate deterministic subagent orchestration plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FAILURE_FIELDS = {
    "failure_type",
    "attempted_query",
    "partial_results",
    "suggested_alternatives",
}
REQUIRED_GAP_FIELDS = {"spoke_id", "reason", "attempted_query"}
ALLOWED_MODELS = {"haiku", "sonnet", "opus"}
ALLOWED_MODEL_ROLES = {"extraction", "classification", "reasoning", "verification", "aggregation"}
BLOCKED_TEXT = (
    "swallow every error",
    "return success with empty results",
    "shared coordinator transcript",
    "one agent with all context",
    "abort the batch on any spoke failure",
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def text(value: Any) -> str:
    return str(value or "").strip()


def all_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(all_text(v) for v in value)
    return text(value)


def as_dict(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def as_list(data: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{key} must be a non-empty list")
        return []
    out: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
        else:
            out.append(item)
    return out


def str_list(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {text(item) for item in value if text(item)}


def validate_spokes(spokes: list[dict[str, Any]], errors: list[str]) -> None:
    if len(spokes) < 2:
        errors.append("spokes must define at least two spoke templates")
    seen: set[str] = set()
    for index, spoke in enumerate(spokes, start=1):
        label = f"spokes[{index}]"
        spoke_id = text(spoke.get("id"))
        if not spoke_id:
            errors.append(f"{label}.id is required")
        if spoke_id in seen:
            errors.append(f"{label}.id must be unique: {spoke_id}")
        seen.add(spoke_id)
        if not text(spoke.get("task")):
            errors.append(f"{label}.task is required")

        agent_definition = spoke.get("agent_definition")
        if not isinstance(agent_definition, dict):
            errors.append(f"{label}.agent_definition must be an object")
            agent_definition = {}
        for key in ("description", "prompt", "model", "model_role"):
            if not text(agent_definition.get(key)):
                errors.append(f"{label}.agent_definition.{key} is required")
        if text(agent_definition.get("model")) not in ALLOWED_MODELS:
            errors.append(f"{label}.agent_definition.model is unsupported")
        if text(agent_definition.get("model_role")) not in ALLOWED_MODEL_ROLES:
            errors.append(f"{label}.agent_definition.model_role is unsupported")
        tools = agent_definition.get("tools")
        if not isinstance(tools, list) or any(not isinstance(tool, str) for tool in tools):
            errors.append(f"{label}.agent_definition.tools must be a list of strings")

        dispatch = spoke.get("dispatch")
        if not isinstance(dispatch, dict) or text(dispatch.get("tool")) != "Task":
            errors.append(f"{label}.dispatch.tool must be Task")

        isolation = spoke.get("isolation")
        if not isinstance(isolation, dict):
            errors.append(f"{label}.isolation must be an object")
            isolation = {}
        if text(isolation.get("mode")) != "fresh_session":
            errors.append(f"{label}.isolation.mode must be fresh_session")
        if isolation.get("shared_context") not in (False, None):
            errors.append(f"{label}.isolation.shared_context must be false")
        if isolation.get("shared_mutable_state") not in (False, None):
            errors.append(f"{label}.isolation.shared_mutable_state must be false")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("skill") != "subagent-orchestration":
        errors.append("skill must be subagent-orchestration")
    lowered = all_text(data).lower()
    for marker in BLOCKED_TEXT:
        if marker in lowered:
            errors.append(f"blocked anti-pattern text: {marker}")

    coordinator = as_dict(data, "coordinator", errors)
    if not text(coordinator.get("id")):
        errors.append("coordinator.id is required")
    if not text(coordinator.get("fanout_justification")):
        errors.append("coordinator.fanout_justification is required")
    if coordinator.get("consumes_last_message_only") is not True:
        errors.append("coordinator.consumes_last_message_only must be true")
    if coordinator.get("reads_spoke_transcript") not in (False, None):
        errors.append("coordinator.reads_spoke_transcript must be false")

    validate_spokes(as_list(data, "spokes", errors), errors)

    failure_contract = as_dict(data, "failure_contract", errors)
    failure_fields = str_list(failure_contract.get("required_fields"))
    missing_failure_fields = REQUIRED_FAILURE_FIELDS - failure_fields
    if missing_failure_fields:
        errors.append(f"failure_contract.required_fields missing: {sorted(missing_failure_fields)}")
    failure_types = str_list(failure_contract.get("failure_types"))
    if "access_failure" not in failure_types:
        errors.append("failure_contract.failure_types must include access_failure")
    if "valid_empty" in failure_types:
        errors.append("valid_empty must not be modeled as a failure_type")
    valid_empty = failure_contract.get("valid_empty")
    if not isinstance(valid_empty, dict):
        errors.append("failure_contract.valid_empty must be an object")
        valid_empty = {}
    if text(valid_empty.get("status")) != "ok":
        errors.append("failure_contract.valid_empty.status must be ok")
    if valid_empty.get("empty_valid") is not True:
        errors.append("failure_contract.valid_empty.empty_valid must be true")
    local_recovery = failure_contract.get("local_recovery")
    if not isinstance(local_recovery, dict):
        errors.append("failure_contract.local_recovery must be an object")
        local_recovery = {}
    max_attempts = local_recovery.get("max_attempts")
    if not isinstance(max_attempts, int) or max_attempts < 1 or max_attempts > 3:
        errors.append("failure_contract.local_recovery.max_attempts must be 1..3")
    strategies = local_recovery.get("strategies")
    if not isinstance(strategies, list) or not strategies:
        errors.append("failure_contract.local_recovery.strategies must be a non-empty list")

    aggregation = as_dict(data, "aggregation", errors)
    if text(aggregation.get("partial_failure_policy")) != "continue_with_coverage_gap":
        errors.append("aggregation.partial_failure_policy must be continue_with_coverage_gap")
    if aggregation.get("distinguish_access_failure_from_valid_empty") is not True:
        errors.append("aggregation.distinguish_access_failure_from_valid_empty must be true")
    if aggregation.get("abort_on_first_failure") not in (False, None):
        errors.append("aggregation.abort_on_first_failure must be false")
    if aggregation.get("empty_success_on_failure") not in (False, None):
        errors.append("aggregation.empty_success_on_failure must be false")
    gap_fields = str_list(aggregation.get("coverage_gap_fields"))
    missing_gap_fields = REQUIRED_GAP_FIELDS - gap_fields
    if missing_gap_fields:
        errors.append(f"aggregation.coverage_gap_fields missing: {sorted(missing_gap_fields)}")

    validation = as_dict(data, "validation", errors)
    if validation.get("offline") is not True:
        errors.append("validation.offline must be true")
    if validation.get("network_required") not in (False, None):
        errors.append("validation.network_required must be false")
    if validation.get("deterministic") is not True:
        errors.append("validation.deterministic must be true")
    if text(validation.get("result")) not in {"pass", "blocked"}:
        errors.append("validation.result must be pass or blocked")
    if errors and text(validation.get("result")) == "pass":
        errors.append("validation.result must not be pass when errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate subagent orchestration JSON plan")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        data = load_json(Path(args.input))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"subagent_orchestration_plan={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
