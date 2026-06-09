#!/usr/bin/env python3
"""Validate deterministic Builtin Tool Selection JSON reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.katas-builtin-tool-selection.report.v1"
REQUIRED_TOP = {
    "schema",
    "skill",
    "objective",
    "scope",
    "selected_strategy",
    "tool_decisions",
    "read_plan",
    "edit_plan",
    "evidence",
    "validation",
    "risks",
}
TAGS = {"[CODIGO]", "[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]"}
INTENT_TO_TOOL = {
    "content-search": "Grep",
    "path-search": "Glob",
    "file-read": "Read",
    "targeted-edit": "Edit",
    "full-file-write": "Write",
    "shell-command": "Bash",
}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "tool_fit",
    "read_economy",
    "edit_anchor_safety",
    "fallback_policy",
    "evidence_required",
}


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


def validate_tool_decisions(data: dict[str, Any], errors: list[str]) -> set[str]:
    decisions = objects(data.get("tool_decisions"), "tool_decisions", errors)
    require(bool(decisions), errors, "tool_decisions required")
    intents: set[str] = set()
    for index, item in enumerate(decisions):
        ctx = f"tool_decisions[{index}]"
        intent = item.get("intent")
        tool = item.get("chosen_tool")
        intents.add(intent) if isinstance(intent, str) else None
        require(intent in INTENT_TO_TOOL, errors, f"{ctx}.intent invalid")
        if isinstance(intent, str) and intent in INTENT_TO_TOOL:
            require(tool == INTENT_TO_TOOL[intent], errors, f"{ctx}.chosen_tool must be {INTENT_TO_TOOL[intent]}")
        require(is_text(item.get("rationale")), errors, f"{ctx}.rationale required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
    return intents


def validate_read_plan(data: dict[str, Any], intents: set[str], errors: list[str]) -> None:
    read_plan = object_at(data, "read_plan", errors)
    require(read_plan.get("mass_read_upfront") is False, errors, "read_plan.mass_read_upfront must be false")
    require(read_plan.get("search_before_read") is True, errors, "read_plan.search_before_read must be true")
    files_considered = read_plan.get("files_considered")
    files_read = text_list(read_plan.get("files_read"), "read_plan.files_read", errors)
    require(isinstance(files_considered, int) and files_considered >= len(files_read), errors, "read_plan.files_considered invalid")
    require(bool(files_read), errors, "read_plan.files_read required")
    require("file-read" in intents, errors, "tool_decisions must include file-read when files_read is non-empty")
    if isinstance(files_considered, int) and files_considered > 1:
        require({"content-search", "path-search"}.intersection(intents), errors, "multi-file consideration requires Grep or Glob first")


def validate_edit_plan(data: dict[str, Any], intents: set[str], errors: list[str]) -> None:
    edit_plan = object_at(data, "edit_plan", errors)
    operation = edit_plan.get("operation")
    require(operation in {"Edit", "Write", "none"}, errors, "edit_plan.operation invalid")
    anchor = object_at(edit_plan, "anchor", errors)
    unique_match_count = anchor.get("unique_match_count")
    fallback = object_at(edit_plan, "fallback", errors)
    if operation == "Edit":
        require("targeted-edit" in intents, errors, "Edit operation requires targeted-edit decision")
        require(is_text(anchor.get("old_text")), errors, "edit_plan.anchor.old_text required for Edit")
        require(unique_match_count == 1, errors, "Edit requires unique anchor match count of 1")
        require(fallback.get("declared") is True, errors, "Edit requires declared fallback")
        require(fallback.get("action") in {"expand-anchor", "read-and-write-full-file"}, errors, "Edit fallback action invalid")
    elif operation == "Write":
        require("full-file-write" in intents, errors, "Write operation requires full-file-write decision")
        require(fallback.get("trigger") == "ambiguous-anchor", errors, "Write fallback trigger must be ambiguous-anchor")
        require(fallback.get("full_file_read_before_write") is True, errors, "Write fallback requires full file read before write")
        require(is_text(fallback.get("reason")), errors, "Write fallback reason required")
    else:
        require("targeted-edit" not in intents and "full-file-write" not in intents, errors, "none operation cannot include edit/write decisions")


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
    require(not {"read_all_files", "repo_wide_read", "ambiguous_edit_anchor", "tool_mismatch"}.intersection(forbidden), errors, "forbidden anti-pattern present")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "katas-builtin-tool-selection", errors, "skill must be katas-builtin-tool-selection")
    require(is_text(data.get("objective")), errors, "objective required")
    require(is_text(data.get("scope")), errors, "scope required")
    require(data.get("selected_strategy") in {"Grep-Read-Edit", "Glob-Read", "Grep-Read-Write", "Bash-only"}, errors, "selected_strategy invalid")
    intents = validate_tool_decisions(data, errors)
    validate_read_plan(data, intents, errors)
    validate_edit_plan(data, intents, errors)
    validate_evidence(data, errors)
    validate_validation(data, errors)
    validate_risks(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_tool_selection_report.py <report.json>", file=sys.stderr)
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
