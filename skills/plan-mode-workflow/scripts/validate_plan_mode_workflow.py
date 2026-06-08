#!/usr/bin/env python3
"""Validate deterministic Plan Mode workflow reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "plan-mode-workflow"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("plan-mode-workflow-contract.json")["json_contract"]
    mode_policy = asset("mode-state-policy.json")
    tool_policy = asset("read-only-tool-policy.json")
    approval_policy = asset("approval-signature-policy.json")
    hook_policy = asset("hook-enforcement-policy.json")
    execution_policy = asset("execution-decision-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("workflow_id")):
        errors.append("workflow_id must be a non-empty string")

    mode_state = report.get("mode_state")
    if not isinstance(mode_state, dict):
        errors.append("mode_state must be an object")
        mode_state = {}
    for field in mode_policy["required_fields"]:
        if field not in mode_state:
            errors.append(f"mode_state missing field {field}")
    if mode_state.get("current_mode") not in mode_policy["allowed_modes"]:
        errors.append("mode_state.current_mode is not allowed")
    if mode_state.get("default_start_mode") != mode_policy["default_start_mode"]:
        errors.append("mode_state.default_start_mode must be plan")

    plan_artifact = report.get("plan_artifact")
    if not isinstance(plan_artifact, dict):
        errors.append("plan_artifact must be an object")
        plan_artifact = {}
    for field in approval_policy["required_plan_fields"]:
        if field not in plan_artifact:
            errors.append(f"plan_artifact missing field {field}")
    plan_hash = str(plan_artifact.get("sha256", ""))
    if not re.match(approval_policy["sha256_pattern"], plan_hash):
        errors.append("plan_artifact.sha256 must be a lowercase sha256 hex digest")
    if mode_state.get("plan_hash_current") != plan_artifact.get("sha256"):
        errors.append("mode_state.plan_hash_current must match plan_artifact.sha256")
    if plan_artifact.get("status") not in approval_policy["plan_statuses"]:
        errors.append("plan_artifact.status is not allowed")
    for field in ["path", "objective"]:
        if not non_empty_string(plan_artifact.get(field)):
            errors.append(f"plan_artifact.{field} must be non-empty")
    for field in ["files_to_touch", "acceptance_criteria", "risks"]:
        if not isinstance(plan_artifact.get(field), list) or not plan_artifact.get(field):
            errors.append(f"plan_artifact.{field} must be a non-empty list")

    approval = report.get("approval_event")
    if not isinstance(approval, dict):
        errors.append("approval_event must be an object")
        approval = {}
    for field in approval_policy["required_approval_fields"]:
        if field not in approval:
            errors.append(f"approval_event missing field {field}")
    approval_status = approval.get("status")
    if approval_status not in approval_policy["approval_statuses"]:
        errors.append("approval_event.status is not allowed")
    if approval_status == "signed":
        if approval.get("plan_hash") != plan_artifact.get("sha256"):
            errors.append("signed approval_event.plan_hash must match plan_artifact.sha256")
        if mode_state.get("signed_plan_hash") != approval.get("plan_hash"):
            errors.append("mode_state.signed_plan_hash must match signed approval_event.plan_hash")
        if not non_empty_string(approval.get("approved_by")):
            errors.append("signed approval_event.approved_by must be non-empty")
        if not re.match(approval_policy["signed_at_pattern"], str(approval.get("signed_at", ""))):
            errors.append("approval_event.signed_at must be UTC timestamp")
    else:
        if mode_state.get("signed_plan_hash"):
            errors.append("unsigned approval requires empty signed_plan_hash")

    read_only = report.get("read_only_exploration")
    if not isinstance(read_only, list) or not read_only:
        errors.append("read_only_exploration must be a non-empty list")
        read_only = []
    for index, step in enumerate(read_only):
        if not isinstance(step, dict):
            errors.append(f"read_only_exploration[{index}] must be an object")
            continue
        if not non_empty_string(step.get("tool")):
            errors.append(f"read_only_exploration[{index}].tool must be non-empty")
        if not non_empty_string(step.get("purpose")):
            errors.append(f"read_only_exploration[{index}].purpose must be non-empty")
        if step.get("mutates") is not False:
            errors.append(f"read_only_exploration[{index}].mutates must be false")

    write_policy = report.get("write_tool_policy")
    if not isinstance(write_policy, dict):
        errors.append("write_tool_policy must be an object")
        write_policy = {}
    read_tools = set(write_policy.get("allowed_read_tools", [])) if isinstance(write_policy.get("allowed_read_tools"), list) else set()
    blocked_tools = set(write_policy.get("blocked_write_tools", [])) if isinstance(write_policy.get("blocked_write_tools"), list) else set()
    required_read = set(tool_policy["allowed_read_tools"])
    required_blocked = set(tool_policy["required_blocked_write_tools"])
    if not required_read.issubset(read_tools):
        errors.append("write_tool_policy.allowed_read_tools missing required read tools")
    if not required_blocked.issubset(blocked_tools):
        errors.append("write_tool_policy.blocked_write_tools missing required write tools")
    if bool(write_policy.get("bypass_permissions")) is not False:
        errors.append("write_tool_policy.bypass_permissions must be false")

    hook = report.get("hook_enforcement")
    if not isinstance(hook, dict):
        errors.append("hook_enforcement must be an object")
        hook = {}
    for field in hook_policy["required_fields"]:
        if field not in hook:
            errors.append(f"hook_enforcement missing field {field}")
    if hook.get("hook") != hook_policy["hook"]:
        errors.append("hook_enforcement.hook must be PreToolUse")
    if hook.get("enforcement_active") is not True:
        errors.append("hook_enforcement.enforcement_active must be true")
    if hook.get("denies_write_in_plan") is not True:
        errors.append("hook_enforcement.denies_write_in_plan must be true")
    if hook.get("reverts_on_plan_hash_change") is not True:
        errors.append("hook_enforcement.reverts_on_plan_hash_change must be true")
    if not isinstance(hook.get("deny_reasons"), list) or not hook.get("deny_reasons"):
        errors.append("hook_enforcement.deny_reasons must be a non-empty list")

    execution = report.get("execution")
    if not isinstance(execution, dict):
        errors.append("execution must be an object")
        execution = {}
    for field in execution_policy["required_fields"]:
        if field not in execution:
            errors.append(f"execution missing field {field}")
    action = execution.get("action")
    if action not in execution_policy["actions"]:
        errors.append("execution.action is not allowed")
    blocking_gaps = execution.get("blocking_gaps")
    if not isinstance(blocking_gaps, list):
        errors.append("execution.blocking_gaps must be a list")
        blocking_gaps = []
    writes = execution.get("writes")
    if not isinstance(writes, list):
        errors.append("execution.writes must be a list")
        writes = []

    signed_and_matching = approval_status == "signed" and approval.get("plan_hash") == plan_artifact.get("sha256")
    plan_changed = plan_artifact.get("status") == "changed_after_signature"
    blocking_needed = not signed_and_matching or plan_changed or bool(blocking_gaps)
    if action in {"ready", "executed"}:
        if not signed_and_matching:
            errors.append("ready/executed requires signed matching approval")
        if plan_changed:
            errors.append("ready/executed is forbidden when plan changed after signature")
        if execution.get("executed_plan_hash") != plan_artifact.get("sha256"):
            errors.append("execution.executed_plan_hash must match plan_artifact.sha256")
    if action == "executed" and not writes:
        errors.append("executed action requires writes")
    if action in {"none", "blocked"} and not blocking_gaps:
        errors.append("none/blocked execution requires blocking_gaps")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    expected_flags = {
        "plan_mode_read_only": True,
        "write_tools_enumerated": True,
        "signed_hash_matches_plan": signed_and_matching,
        "hook_blocks_writes": True,
        "plan_change_requires_resign": True,
        "no_bypass_permissions": True,
        "deterministic_script_passed": True,
    }
    for field, expected in expected_flags.items():
        if validation.get(field) is not expected:
            errors.append(f"validation.{field} must be {expected}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
        guardian = {}
    guardian_decision = guardian.get("decision")
    if guardian_decision not in contract["guardian_decisions"]:
        errors.append(f"guardian.decision must be one of {contract['guardian_decisions']}")
    if not non_empty_string(guardian.get("reason")):
        errors.append("guardian.reason must be non-empty")
    if guardian_decision == "pass" and blocking_needed:
        errors.append("guardian pass requires no blocking gaps")
    if guardian_decision == "pass" and action not in {"ready", "executed"}:
        errors.append("guardian pass requires ready or executed action")
    if guardian_decision == "block" and not blocking_needed:
        errors.append("guardian block requires blocking gaps")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Plan Mode workflow JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON report")
    args = parser.parse_args()

    try:
        report = load_json(args.report)
        errors = validate(report)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
