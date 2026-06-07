#!/usr/bin/env python3
"""Validate deterministic git-workflow plan fixtures."""

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


def validate_repo_state(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    repo = spec.get("repo_state")
    decision = spec.get("decision", {})
    if not isinstance(repo, dict):
        errors.append("repo_state must be an object")
        return
    require_fields(repo, contract["required_repo_fields"], "repo_state", errors)
    if not isinstance(repo.get("clean"), bool):
        errors.append("repo_state clean must be boolean")
    if not isinstance(repo.get("aligned_with_remote"), bool):
        errors.append("repo_state aligned_with_remote must be boolean")
    if not isinstance(repo.get("open_prs"), int):
        errors.append("repo_state open_prs must be integer")
    if repo.get("evidence_tag") not in allowed:
        errors.append("repo_state evidence_tag is invalid")
    if isinstance(decision, dict) and decision.get("status") == "proceed":
        if repo.get("clean") is not True:
            errors.append("decision cannot proceed with dirty working tree")
        if repo.get("aligned_with_remote") is not True:
            errors.append("decision cannot proceed when base is not aligned with remote")


def validate_decision(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    decision = spec.get("decision")
    if not isinstance(decision, dict):
        errors.append("decision must be an object")
        return
    require_fields(decision, ["status", "rationale", "evidence_tag"], "decision", errors)
    if decision.get("status") not in contract["decision_statuses"]:
        errors.append(f"decision status is invalid: {decision.get('status')}")
    if decision.get("evidence_tag") not in allowed or not has_evidence(decision, allowed):
        errors.append("decision missing valid evidence")


def validate_branch(spec: dict[str, Any], policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    branch = spec.get("branch_strategy")
    if not isinstance(branch, dict):
        errors.append("branch_strategy must be an object")
        return
    require_fields(branch, ["type", "branch_name", "base_branch", "evidence_tag"], "branch_strategy", errors)
    if branch.get("type") not in policy["branch_types"]:
        errors.append(f"branch type is invalid: {branch.get('type')}")
    branch_name = str(branch.get("branch_name", ""))
    if branch.get("type") != "trunk" and not re.match(policy["branch_name_pattern"], branch_name):
        errors.append(f"branch_name does not match policy: {branch_name}")
    if branch_name in policy["protected_bases"]:
        errors.append("branch_name cannot be a protected base")
    if branch.get("evidence_tag") not in allowed:
        errors.append("branch_strategy evidence_tag is invalid")


def validate_commands(spec: dict[str, Any], contract: dict[str, Any], policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    steps = spec.get("operation_plan")
    if not isinstance(steps, list) or not (3 <= len(steps) <= 12):
        errors.append("operation_plan must contain 3 to 12 steps")
        return
    seen = []
    for item in steps:
        if not isinstance(item, dict):
            errors.append("operation step must be an object")
            continue
        require_fields(item, contract["required_step_fields"], "operation step", errors)
        seen.append(item.get("step"))
        command = str(item.get("command", ""))
        for pattern in policy["forbidden_patterns"]:
            if pattern in command:
                errors.append(f"forbidden command pattern: {pattern}")
        if not any(command.startswith(prefix) for prefix in policy["allowed_command_prefixes"]):
            errors.append(f"command prefix is not allowed: {command}")
        if item.get("evidence_tag") not in allowed:
            errors.append(f"operation step evidence_tag is invalid: {command}")
    if seen != sorted(seen):
        errors.append("operation steps must be ordered")


def validate_commit_pr_conflict(spec: dict[str, Any], contract: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    commit = spec.get("commit_policy")
    if not isinstance(commit, dict):
        errors.append("commit_policy must be an object")
    else:
        require_fields(commit, ["convention", "message_example", "evidence_tag"], "commit_policy", errors)
        if commit.get("convention") not in contract["commit_conventions"]:
            errors.append(f"commit convention is invalid: {commit.get('convention')}")
        if commit.get("evidence_tag") not in allowed:
            errors.append("commit_policy evidence_tag is invalid")

    pr = spec.get("pr_policy")
    if not isinstance(pr, dict):
        errors.append("pr_policy must be an object")
    else:
        require_fields(pr, ["required_checks", "merge_method", "delete_branch", "evidence_tag"], "pr_policy", errors)
        if not isinstance(pr.get("required_checks"), list) or not pr.get("required_checks"):
            errors.append("pr_policy required_checks must be a non-empty list")
        if pr.get("merge_method") not in contract["merge_methods"]:
            errors.append(f"merge method is invalid: {pr.get('merge_method')}")
        if not isinstance(pr.get("delete_branch"), bool):
            errors.append("pr_policy delete_branch must be boolean")
        if pr.get("evidence_tag") not in allowed:
            errors.append("pr_policy evidence_tag is invalid")

    conflict = spec.get("conflict_policy")
    if not isinstance(conflict, dict):
        errors.append("conflict_policy must be an object")
    else:
        require_fields(conflict, ["strategy", "marker_check", "validation_after_resolution", "evidence_tag"], "conflict_policy", errors)
        if conflict.get("evidence_tag") not in allowed:
            errors.append("conflict_policy evidence_tag is invalid")


def validate_release(spec: dict[str, Any], policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    release = spec.get("release_policy")
    if not isinstance(release, dict):
        errors.append("release_policy must be an object")
        return
    require_fields(release, ["tag_strategy", "evidence_tag"], "release_policy", errors)
    strategy = release.get("tag_strategy")
    if strategy not in policy["tag_strategies"]:
        errors.append(f"release tag_strategy is invalid: {strategy}")
    if strategy == "semver-tag":
        require_fields(release, ["tag_name", "version_source"], "release_policy", errors)
        if not re.match(policy["semver_tag_pattern"], str(release.get("tag_name", ""))):
            errors.append("release tag_name must be SemVer")
    if release.get("evidence_tag") not in allowed or not has_evidence(release, allowed):
        errors.append("release_policy missing valid evidence")


def validate_validation_and_risks(spec: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    validation = spec.get("validation")
    if not isinstance(validation, list) or len(validation) < 2:
        errors.append("validation must contain at least two commands or checks")
    elif not has_evidence(validation, allowed):
        errors.append("validation must include evidence tags")
    decision = spec.get("decision", {})
    if isinstance(decision, dict) and decision.get("status") == "proceed" and (not isinstance(validation, list) or not validation):
        errors.append("proceed decision requires validation")
    stops = spec.get("stop_conditions")
    if not isinstance(stops, list) or not stops:
        errors.append("stop_conditions must be a non-empty list")
    elif not has_evidence(stops, allowed):
        errors.append("stop_conditions must include evidence tags")
    if not has_evidence(spec.get("risks"), allowed):
        errors.append("risks must include evidence tags")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a git-workflow plan JSON file")
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "workflow-plan-contract.json")
    command_policy = load_json(ASSETS / "command-policy.json")
    branch_policy = load_json(ASSETS / "branch-policy.json")
    release_policy = load_json(ASSETS / "release-policy.json")
    allowed = set(contract["allowed_evidence_tags"])

    spec = load_json(args.plan)
    errors: list[str] = []
    if not isinstance(spec, dict):
        errors.append("plan root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in spec:
                errors.append(f"missing top-level field: {field}")
        if spec.get("skill") != "git-workflow":
            errors.append("skill must be git-workflow")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_date(str(spec["reference_date"]), errors)
    body = json.dumps(spec, ensure_ascii=False)
    for term in contract["moving_time_terms"]:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"plan must avoid moving time term: {term}")

    validate_decision(spec, contract, allowed, errors)
    validate_repo_state(spec, contract, allowed, errors)
    validate_branch(spec, branch_policy, allowed, errors)
    validate_commands(spec, contract, command_policy, allowed, errors)
    validate_commit_pr_conflict(spec, contract, allowed, errors)
    validate_release(spec, release_policy, allowed, errors)
    validate_validation_and_risks(spec, allowed, errors)

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(
        f"PASS {args.plan.name}: decision={spec['decision']['status']} "
        f"branch={spec['branch_strategy']['branch_name']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
