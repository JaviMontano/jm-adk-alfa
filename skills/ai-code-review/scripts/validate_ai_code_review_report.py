#!/usr/bin/env python3
"""Validate deterministic AI Code Review report packets offline."""

from __future__ import annotations

import fnmatch
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.ai-code-review.report.v1"
REQUIRED_TOP = {
    "schema",
    "target",
    "scope",
    "review_mode",
    "evidence",
    "findings",
    "summary",
    "validation",
    "risks",
}
REQUIRED_FINDING = {
    "id",
    "priority",
    "category",
    "status",
    "file",
    "line_start",
    "evidence_id",
    "observation",
    "impact",
    "recommendation",
    "confidence",
    "false_positive_notes",
}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
EVIDENCE_KINDS = {"source", "diff", "test", "command_output", "doc", "config"}
REVIEW_MODES = {"quick", "standard", "deep", "adversarial"}
PRIORITIES = {
    "P0": 0.90,
    "P1": 0.80,
    "P2": 0.65,
    "P3": 0.50,
}
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
STATUSES = {"confirmed", "probable", "needs-verification"}
CATEGORIES = {
    "correctness",
    "security",
    "tests",
    "performance",
    "maintainability",
    "data-integrity",
    "observability",
    "accessibility",
    "ai-safety",
}
CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "file_line_evidence",
    "false_positive_filter",
    "no_fake_test_results",
}
TEST_CLAIMS = {"not-run", "pass", "fail", "partial"}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def objects(value: Any, name: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for i, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{name}[{i}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def strings(value: Any, name: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out = [item for item in value if isinstance(item, str) and item]
    require(len(out) == len(value), errors, f"{name} must contain only non-empty strings")
    return out


def matches_any(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern == path or fnmatch.fnmatch(path, pattern):
            return True
        if pattern.endswith("/**") and path.startswith(pattern[:-3]):
            return True
    return False


def validate_scope(data: dict[str, Any], errors: list[str]) -> tuple[list[str], list[str]]:
    scope = data.get("scope")
    require(isinstance(scope, dict), errors, "scope must be object")
    if not isinstance(scope, dict):
        return [], []
    includes = strings(scope.get("includes"), "scope.includes", errors)
    excludes = strings(scope.get("excludes"), "scope.excludes", errors)
    require(bool(includes), errors, "scope.includes required")
    require(bool(scope.get("basis")), errors, "scope.basis required")
    return includes, excludes


def validate_evidence(data: dict[str, Any], errors: list[str]) -> tuple[set[str], set[str]]:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    evidence_ids: set[str] = set()
    command_evidence_ids: set[str] = set()
    for item in evidence:
        eid = item.get("id")
        require(isinstance(eid, str) and bool(eid), errors, "evidence id required")
        if isinstance(eid, str):
            require(eid not in evidence_ids, errors, f"duplicate evidence id {eid}")
            evidence_ids.add(eid)
        tag = item.get("tag")
        kind = item.get("kind")
        source = item.get("source")
        require(tag in TAGS, errors, f"evidence {eid} invalid tag")
        require(kind in EVIDENCE_KINDS, errors, f"evidence {eid} invalid kind")
        require(isinstance(source, str) and bool(source), errors, f"evidence {eid} source required")
        require(bool(item.get("summary")), errors, f"evidence {eid} summary required")
        if kind in {"source", "diff", "test", "config"} and isinstance(source, str):
            require(":" in source, errors, f"evidence {eid} source must include file:line marker")
        if kind == "command_output" and isinstance(eid, str):
            command_evidence_ids.add(eid)
    return evidence_ids, command_evidence_ids


def validate_findings(
    data: dict[str, Any],
    evidence_ids: set[str],
    includes: list[str],
    excludes: list[str],
    errors: list[str],
) -> None:
    findings = objects(data.get("findings"), "findings", errors)
    finding_ids: set[str] = set()
    for finding in findings:
        fid = finding.get("id")
        missing = sorted(REQUIRED_FINDING - set(finding))
        require(not missing, errors, f"finding {fid} missing fields: {', '.join(missing)}")
        require(isinstance(fid, str) and bool(fid), errors, "finding id required")
        if isinstance(fid, str):
            require(fid not in finding_ids, errors, f"duplicate finding id {fid}")
            finding_ids.add(fid)

        priority = finding.get("priority")
        status = finding.get("status")
        category = finding.get("category")
        file_path = finding.get("file")
        line_start = finding.get("line_start")
        confidence = finding.get("confidence")
        evidence_id = finding.get("evidence_id")

        require(priority in PRIORITIES, errors, f"finding {fid} invalid priority")
        require(status in STATUSES, errors, f"finding {fid} invalid status")
        require(category in CATEGORIES, errors, f"finding {fid} invalid category")
        require(isinstance(file_path, str) and bool(file_path), errors, f"finding {fid} file required")
        require(isinstance(line_start, int) and line_start >= 1, errors, f"finding {fid} line_start must be >= 1")
        require(evidence_id in evidence_ids, errors, f"finding {fid} references unknown evidence {evidence_id}")
        require(isinstance(confidence, (int, float)) and 0 <= confidence <= 1, errors, f"finding {fid} confidence must be 0..1")
        for field in ("observation", "impact", "recommendation"):
            require(isinstance(finding.get(field), str) and bool(finding.get(field)), errors, f"finding {fid} missing {field}")
        require(isinstance(finding.get("false_positive_notes"), str), errors, f"finding {fid} false_positive_notes must be string")

        if isinstance(file_path, str) and file_path:
            require(matches_any(file_path, includes), errors, f"finding {fid} file outside scope.includes: {file_path}")
            require(not matches_any(file_path, excludes), errors, f"finding {fid} file is excluded by scope: {file_path}")

        if priority in {"P0", "P1"}:
            require(status == "confirmed", errors, f"finding {fid} P0/P1 must be confirmed")
            if isinstance(confidence, (int, float)):
                require(confidence >= PRIORITIES[str(priority)], errors, f"finding {fid} confidence below {priority} threshold")
        if status == "needs-verification":
            require(priority not in {"P0", "P1"}, errors, f"finding {fid} needs-verification cannot be P0/P1")
            require(bool(finding.get("false_positive_notes")), errors, f"finding {fid} needs-verification requires false_positive_notes")


def validate_summary(data: dict[str, Any], errors: list[str]) -> None:
    summary = data.get("summary")
    findings = data.get("findings") if isinstance(data.get("findings"), list) else []
    require(isinstance(summary, dict), errors, "summary must be object")
    if not isinstance(summary, dict):
        return
    require(summary.get("finding_count") == len(findings), errors, "summary.finding_count must equal findings length")
    priorities = [item.get("priority") for item in findings if isinstance(item, dict) and item.get("priority") in PRIORITIES]
    highest = min(priorities, key=lambda value: PRIORITY_ORDER[str(value)]) if priorities else "none"
    require(summary.get("highest_priority") == highest, errors, "summary.highest_priority mismatch")
    require(summary.get("overall_risk") in {"none", "low", "medium", "high", "critical"}, errors, "summary.overall_risk invalid")
    if not findings:
        require(bool(summary.get("clean_review_rationale")), errors, "clean review requires summary.clean_review_rationale")


def validate_validation(data: dict[str, Any], command_evidence_ids: set[str], errors: list[str]) -> None:
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if not isinstance(validation, dict):
        return
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    checks = validation.get("checks")
    require(isinstance(checks, list), errors, "validation.checks must be list")
    if isinstance(checks, list):
        require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")
    commands = objects(validation.get("commands_run"), "validation.commands_run", errors)
    claim = validation.get("claimed_test_status")
    require(claim in TEST_CLAIMS, errors, "validation.claimed_test_status invalid")
    if claim in {"pass", "fail", "partial"}:
        require(bool(commands), errors, "test pass/fail/partial claim requires commands_run")
        for command in commands:
            eid = command.get("evidence_id")
            require(eid in command_evidence_ids, errors, f"command evidence_id {eid} must reference command_output evidence")
            require(bool(command.get("command")), errors, "command entry requires command")
            require(command.get("status") in {"pass", "fail"}, errors, "command entry status must be pass/fail")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors

    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(isinstance(data.get("target"), str) and bool(data.get("target")), errors, "target required")
    require(data.get("review_mode") in REVIEW_MODES, errors, "review_mode invalid")
    includes, excludes = validate_scope(data, errors)
    evidence_ids, command_evidence_ids = validate_evidence(data, errors)
    validate_findings(data, evidence_ids, includes, excludes, errors)
    validate_summary(data, errors)
    validate_validation(data, command_evidence_ids, errors)
    require(isinstance(data.get("risks"), list), errors, "risks must be list")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_ai_code_review_report.py <report.json>", file=sys.stderr)
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
