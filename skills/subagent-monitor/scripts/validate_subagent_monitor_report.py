#!/usr/bin/env python3
"""Validate deterministic Subagent Monitor JSON reports."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.subagent-monitor.report.v1"
REQUIRED_TOP = {"schema", "skill", "swarm_id", "task", "agents", "timeout_policy", "results", "aggregation", "evidence", "validation"}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]"}
RESULT_STATUSES = {"pass", "warn", "block", "error", "timeout"}
RESULT_TYPES = {"spoke_report", "guardian_decision", "artifact", "timeout_notice", "error_notice"}
AGGREGATION_STATUSES = {"pass", "warn", "block"}
FAILURE_STATUSES = {"block", "error", "timeout"}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "timeout_policy",
    "typed_results",
    "aggregation_policy",
    "partial_failure_handling",
    "evidence_required",
}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def object_at(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    require(isinstance(value, dict), errors, f"{key} must be object")
    return value if isinstance(value, dict) else {}


def objects(value: Any, ctx: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for i, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{ctx}[{i}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def text_list(value: Any, ctx: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for i, item in enumerate(value):
        require(is_text(item), errors, f"{ctx}[{i}] must be non-empty string")
        if is_text(item):
            out.append(item)
    return out


def validate_agents(data: dict[str, Any], errors: list[str]) -> dict[str, bool]:
    agents = objects(data.get("agents"), "agents", errors)
    require(bool(agents), errors, "agents required")
    registry: dict[str, bool] = {}
    for i, agent in enumerate(agents):
        ctx = f"agents[{i}]"
        agent_id = agent.get("id")
        require(is_text(agent_id) and bool(SLUG.match(agent_id)), errors, f"{ctx}.id must be slug")
        require(is_text(agent.get("role")), errors, f"{ctx}.role required")
        require(isinstance(agent.get("required"), bool), errors, f"{ctx}.required must be boolean")
        if is_text(agent_id):
            require(agent_id not in registry, errors, f"duplicate agent id: {agent_id}")
            registry[agent_id] = bool(agent.get("required"))
    return registry


def validate_timeout(data: dict[str, Any], errors: list[str]) -> None:
    policy = object_at(data, "timeout_policy", errors)
    seconds = policy.get("per_agent_seconds")
    require(isinstance(seconds, int) and 1 <= seconds <= 3600, errors, "timeout_policy.per_agent_seconds must be 1..3600")
    require(policy.get("action") == "cancel-and-record", errors, "timeout_policy.action must be cancel-and-record")
    require(policy.get("uses_wall_clock_evidence") is False, errors, "timeout_policy.uses_wall_clock_evidence must be false")
    require(policy.get("sequence_based") is True, errors, "timeout_policy.sequence_based must be true")


def validate_results(data: dict[str, Any], registry: dict[str, bool], errors: list[str]) -> dict[str, str]:
    results = objects(data.get("results"), "results", errors)
    seen: dict[str, str] = {}
    sequences: set[int] = set()
    for i, result in enumerate(results):
        ctx = f"results[{i}]"
        agent_id = result.get("agent_id")
        status = result.get("status")
        sequence = result.get("sequence")
        require(agent_id in registry, errors, f"{ctx}.agent_id unknown")
        require(status in RESULT_STATUSES, errors, f"{ctx}.status invalid")
        require(result.get("result_type") in RESULT_TYPES, errors, f"{ctx}.result_type invalid")
        require(isinstance(sequence, int) and sequence > 0, errors, f"{ctx}.sequence must be positive integer")
        require(result.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        if status in {"error", "timeout", "block"}:
            require(is_text(result.get("error")) or status == "block", errors, f"{ctx}.error required for error/timeout")
        if isinstance(sequence, int):
            require(sequence not in sequences, errors, f"duplicate result sequence: {sequence}")
            sequences.add(sequence)
        if isinstance(agent_id, str):
            require(agent_id not in seen, errors, f"duplicate result for agent: {agent_id}")
            if isinstance(status, str):
                seen[agent_id] = status
    for agent_id, required in registry.items():
        if required:
            require(agent_id in seen, errors, f"missing result for required agent: {agent_id}")
    return seen


def validate_aggregation(data: dict[str, Any], registry: dict[str, bool], seen: dict[str, str], errors: list[str]) -> None:
    aggregation = object_at(data, "aggregation", errors)
    status = aggregation.get("status")
    require(status in AGGREGATION_STATUSES, errors, "aggregation.status invalid")
    require(aggregation.get("partial_failure_policy") == "block-on-required-agent-failure", errors, "aggregation.partial_failure_policy invalid")
    blockers = text_list(aggregation.get("blockers"), "aggregation.blockers", errors)
    gaps = text_list(aggregation.get("coverage_gaps"), "aggregation.coverage_gaps", errors)
    require(aggregation.get("result_count") == len(seen), errors, "aggregation.result_count must equal number of unique results")
    required_failed = [agent_id for agent_id, result_status in seen.items() if registry.get(agent_id) and result_status in FAILURE_STATUSES]
    optional_failed = [agent_id for agent_id, result_status in seen.items() if not registry.get(agent_id) and result_status in FAILURE_STATUSES]
    missing_required = [agent_id for agent_id, required in registry.items() if required and agent_id not in seen]
    if required_failed or missing_required:
        require(status == "block", errors, "required agent failure or missing result must block aggregation")
        require(bool(blockers), errors, "aggregation.blockers required when blocked")
    if optional_failed:
        require(status in {"warn", "block"}, errors, "optional agent failure must warn or block")
        require(bool(gaps), errors, "aggregation.coverage_gaps required for optional failure")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> None:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    for i, item in enumerate(evidence):
        ctx = f"evidence[{i}]"
        require(is_text(item.get("claim")), errors, f"{ctx}.claim required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        require(is_text(item.get("source")), errors, f"{ctx}.source required")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = object_at(data, "validation", errors)
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    require(validation.get("offline") is True, errors, "validation.offline must be true")
    require(validation.get("network_required") is False, errors, "validation.network_required must be false")
    require(validation.get("deterministic") is True, errors, "validation.deterministic must be true")
    checks = set(text_list(validation.get("checks"), "validation.checks", errors))
    require(REQUIRED_CHECKS.issubset(checks), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "subagent-monitor", errors, "skill must be subagent-monitor")
    require(is_text(data.get("swarm_id")) and bool(SLUG.match(data.get("swarm_id", ""))), errors, "swarm_id must be slug")
    require(is_text(data.get("task")), errors, "task required")
    registry = validate_agents(data, errors)
    validate_timeout(data, errors)
    seen = validate_results(data, registry, errors)
    validate_aggregation(data, registry, seen, errors)
    validate_evidence(data, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_subagent_monitor_report.py <report.json>", file=sys.stderr)
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
