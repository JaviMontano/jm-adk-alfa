#!/usr/bin/env python3
"""Validate deterministic Adaptive Investigation JSON reports."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.katas-adaptive-investigation.report.v1"
REQUIRED_TOP = {
    "schema",
    "skill",
    "objective",
    "scope",
    "hypothesis",
    "budget",
    "topology",
    "prioritized_plan",
    "findings",
    "replans",
    "scratchpad",
    "evidence",
    "validation",
    "risks",
}
TAGS = {"[CODIGO]", "[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]"}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "exploration_budget",
    "cheap_mapping_before_deep_dive",
    "selective_deep_dive",
    "replan_gate",
    "evidence_required",
    "scratchpad_persistence",
}
TOOLS = {"Glob", "Grep"}
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
    for index, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{ctx}[{index}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def text_list(value: Any, ctx: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for index, item in enumerate(value):
        require(is_text(item), errors, f"{ctx}[{index}] must be non-empty string")
        if is_text(item):
            out.append(item)
    return out


def validate_budget(data: dict[str, Any], errors: list[str]) -> None:
    budget = object_at(data, "budget", errors)
    status = budget.get("status")
    require(status in {"complete", "exhausted_with_pending"}, errors, "budget.status invalid")
    for dimension in ("files", "queries", "minutes"):
        item = budget.get(dimension)
        require(isinstance(item, dict), errors, f"budget.{dimension} must be object")
        if not isinstance(item, dict):
            continue
        limit = item.get("limit")
        used = item.get("used")
        require(isinstance(limit, int) and limit > 0, errors, f"budget.{dimension}.limit must be positive integer")
        require(isinstance(used, int) and used >= 0, errors, f"budget.{dimension}.used must be non-negative integer")
        if isinstance(limit, int) and isinstance(used, int):
            require(used <= limit, errors, f"budget.{dimension}.used must not exceed limit")
    pending = text_list(budget.get("pending_questions"), "budget.pending_questions", errors)
    if status == "exhausted_with_pending":
        require(bool(pending), errors, "exhausted budget requires pending_questions")


def validate_topology(data: dict[str, Any], errors: list[str]) -> set[str]:
    topology = object_at(data, "topology", errors)
    scans = objects(topology.get("cheap_mapping"), "topology.cheap_mapping", errors)
    require(bool(scans), errors, "topology.cheap_mapping required")
    seen_tools: set[str] = set()
    for index, scan in enumerate(scans):
        ctx = f"topology.cheap_mapping[{index}]"
        tool = scan.get("tool")
        require(tool in TOOLS, errors, f"{ctx}.tool must be Glob or Grep")
        if isinstance(tool, str):
            seen_tools.add(tool)
        require(is_text(scan.get("pattern")), errors, f"{ctx}.pattern required")
        require(isinstance(scan.get("result_count"), int) and scan.get("result_count") >= 0, errors, f"{ctx}.result_count invalid")
        require(scan.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
    require(TOOLS.issubset(seen_tools), errors, "cheap mapping must include both Glob and Grep")
    candidates = text_list(topology.get("candidates"), "topology.candidates", errors)
    require(bool(candidates), errors, "topology.candidates required")
    return set(candidates)


def validate_plan(data: dict[str, Any], candidates: set[str], errors: list[str]) -> list[str]:
    plan = objects(data.get("prioritized_plan"), "prioritized_plan", errors)
    require(bool(plan), errors, "prioritized_plan required")
    targets: list[str] = []
    priorities: set[int] = set()
    for index, item in enumerate(plan):
        ctx = f"prioritized_plan[{index}]"
        target = item.get("target")
        priority = item.get("priority")
        require(is_text(target), errors, f"{ctx}.target required")
        if is_text(target):
            require(target in candidates, errors, f"{ctx}.target must come from topology candidates")
            targets.append(target)
        require(isinstance(priority, int) and priority > 0, errors, f"{ctx}.priority must be positive integer")
        if isinstance(priority, int):
            require(priority not in priorities, errors, f"duplicate plan priority: {priority}")
            priorities.add(priority)
        require(is_text(item.get("rationale")), errors, f"{ctx}.rationale required")
        require(item.get("source") == "topology", errors, f"{ctx}.source must be topology")
    return targets


def validate_findings(data: dict[str, Any], plan_targets: list[str], errors: list[str]) -> dict[str, bool]:
    findings = objects(data.get("findings"), "findings", errors)
    require(bool(findings), errors, "findings required")
    finding_flags: dict[str, bool] = {}
    for index, item in enumerate(findings):
        ctx = f"findings[{index}]"
        finding_id = item.get("id")
        target = item.get("target")
        require(is_text(finding_id) and bool(SLUG.match(finding_id or "")), errors, f"{ctx}.id must be slug")
        require(target in plan_targets, errors, f"{ctx}.target must come from prioritized_plan")
        require(is_text(item.get("summary")), errors, f"{ctx}.summary required")
        require(is_text(item.get("source")), errors, f"{ctx}.source required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        require(isinstance(item.get("invalidates_hypothesis"), bool), errors, f"{ctx}.invalidates_hypothesis must be boolean")
        require(item.get("deep_dive_after_mapping") is True, errors, f"{ctx}.deep_dive_after_mapping must be true")
        if is_text(finding_id):
            require(finding_id not in finding_flags, errors, f"duplicate finding id: {finding_id}")
            finding_flags[finding_id] = bool(item.get("invalidates_hypothesis"))
    return finding_flags


def validate_replans(data: dict[str, Any], finding_flags: dict[str, bool], plan_targets: list[str], errors: list[str]) -> None:
    replans = objects(data.get("replans"), "replans", errors)
    invalidating_findings = {finding_id for finding_id, invalidates in finding_flags.items() if invalidates}
    if invalidating_findings:
        triggers = {item.get("trigger_finding_id") for item in replans}
        require(bool(invalidating_findings.intersection(triggers)), errors, "invalidating finding requires replan")
    for index, item in enumerate(replans):
        ctx = f"replans[{index}]"
        trigger = item.get("trigger_finding_id")
        require(trigger in finding_flags, errors, f"{ctx}.trigger_finding_id unknown")
        if isinstance(trigger, str) and trigger in finding_flags:
            require(finding_flags[trigger] is True, errors, f"{ctx}.trigger must invalidate hypothesis")
        require(is_text(item.get("invalidated_hypothesis")), errors, f"{ctx}.invalidated_hypothesis required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        new_order = text_list(item.get("new_plan_order"), f"{ctx}.new_plan_order", errors)
        require(set(new_order).issubset(set(plan_targets)), errors, f"{ctx}.new_plan_order must use plan targets")


def validate_scratchpad(data: dict[str, Any], errors: list[str]) -> None:
    scratchpad = object_at(data, "scratchpad", errors)
    require(scratchpad.get("persisted") is True, errors, "scratchpad.persisted must be true")
    sections = set(text_list(scratchpad.get("sections"), "scratchpad.sections", errors))
    require({"topology", "plan", "findings", "budget", "risks"}.issubset(sections), errors, "scratchpad.sections missing required sections")
    require(is_text(scratchpad.get("source")), errors, "scratchpad.source required")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> None:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    for index, item in enumerate(evidence):
        ctx = f"evidence[{index}]"
        require(is_text(item.get("claim")), errors, f"{ctx}.claim required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        require(is_text(item.get("source")), errors, f"{ctx}.source required")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = object_at(data, "validation", errors)
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    require(validation.get("offline") is True, errors, "validation.offline must be true")
    require(validation.get("network_required") is False, errors, "validation.network_required must be false")
    require(validation.get("deterministic") is True, errors, "validation.deterministic must be true")
    require(validation.get("uses_randomness") is False, errors, "validation.uses_randomness must be false")
    checks = set(text_list(validation.get("checks"), "validation.checks", errors))
    require(REQUIRED_CHECKS.issubset(checks), errors, "validation.checks missing required checks")


def validate_risks(data: dict[str, Any], errors: list[str]) -> None:
    risks = object_at(data, "risks", errors)
    require(isinstance(risks.get("remaining"), list), errors, "risks.remaining must be list")
    forbidden = set(text_list(risks.get("forbidden_patterns"), "risks.forbidden_patterns", errors))
    require(not {"read_all_files", "unbounded_exploration"}.intersection(forbidden), errors, "forbidden anti-pattern present")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "katas-adaptive-investigation", errors, "skill must be katas-adaptive-investigation")
    require(is_text(data.get("objective")), errors, "objective required")
    require(is_text(data.get("scope")), errors, "scope required")
    require(is_text(data.get("hypothesis")), errors, "hypothesis required")
    validate_budget(data, errors)
    candidates = validate_topology(data, errors)
    plan_targets = validate_plan(data, candidates, errors)
    finding_flags = validate_findings(data, plan_targets, errors)
    validate_replans(data, finding_flags, plan_targets, errors)
    validate_scratchpad(data, errors)
    validate_evidence(data, errors)
    validate_validation(data, errors)
    validate_risks(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_adaptive_investigation_report.py <report.json>", file=sys.stderr)
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
