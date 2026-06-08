#!/usr/bin/env python3
"""Validate Alfa repository maintenance orchestration reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.alfa-repo-maintenance-orchestrator.report.v1"
PHASES = [
    "bootstrap",
    "repo-sync-audit",
    "local-state-preservation",
    "branch-plan",
    "import-consolidation-plan",
    "cleanup-plan",
    "validation-gates",
    "closeout",
]
REQUIRED_GATES = {
    "git-status",
    "check-repo-boundaries",
    "count-components",
    "validate-skills-strict",
    "validate-skill-dod",
    "validate-skill-scripts-skill",
    "validate-skill-scripts-global",
    "validate-runtime-instructions",
    "check-devkit-readiness",
    "diff-check",
}
REQUIRED_INTEGRATIONS = {
    "repo-sync-auditor",
    "local-state-preservation",
    "workspace-governance",
    "git-workflow",
    "safe-scripting-and-bash",
    "quality-gatekeeper",
    "tasklog-management",
    "session-end-cleanup",
}


def obj(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(f"{name} must be an object")
    return {}


def arr(value: Any, name: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{name} must be a list")
    return []


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    root = obj(report, "root", errors)
    if not root:
        return errors
    if root.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if root.get("skill") != "alfa-repo-maintenance-orchestrator":
        errors.append("skill must be alfa-repo-maintenance-orchestrator")
    if arr(root.get("phases"), "phases", errors) != PHASES:
        errors.append("phases must match fixed phase order")

    baseline = obj(root.get("baseline"), "baseline", errors)
    for key in ("repo_root", "branch", "head", "upstream", "status"):
        if not nonempty(baseline.get(key)):
            errors.append(f"baseline.{key} is required")

    policies = obj(root.get("policies"), "policies", errors)
    if policies.get("no_push") is not True:
        errors.append("policies.no_push must remain true")
    if policies.get("no_main_merge") is not True:
        errors.append("policies.no_main_merge must remain true")

    mutating = root.get("mutating") is True
    actions = arr(root.get("planned_actions"), "planned_actions", errors)
    if mutating and baseline.get("branch") in {"main", "master"}:
        errors.append("mutating work cannot run on main")
    if mutating and not nonempty(root.get("preservation_manifest")):
        errors.append("mutating work requires preservation_manifest")
    if any(isinstance(action, dict) and action.get("type") == "cleanup" for action in actions):
        if not nonempty(root.get("cleanup_manifest")):
            errors.append("cleanup actions require cleanup_manifest")

    gates = set(arr(root.get("validation_gates"), "validation_gates", errors))
    missing_gates = sorted(REQUIRED_GATES - gates)
    if missing_gates:
        errors.append(f"missing validation gates: {', '.join(missing_gates)}")

    integrations = set(arr(root.get("integrations"), "integrations", errors))
    missing_integrations = sorted(REQUIRED_INTEGRATIONS - integrations)
    if missing_integrations:
        errors.append(f"missing integrations: {', '.join(missing_integrations)}")

    decision = obj(root.get("decision"), "decision", errors)
    if decision.get("next_action") not in {"proceed", "pause", "blocked"}:
        errors.append("decision.next_action is invalid")
    if errors and decision.get("next_action") == "proceed":
        errors.append("invalid report cannot proceed")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+")
    args = parser.parse_args()
    errors: list[str] = []
    for report in args.reports:
        path = Path(report)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        errors.extend(f"{path}: {error}" for error in validate(data))
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
