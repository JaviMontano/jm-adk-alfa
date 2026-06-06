#!/usr/bin/env python3
"""Validate deterministic Continuous Learning JSON reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.continuous-learning.report.v1"
REQUIRED_TOP = {"schema", "skill", "source_event", "prior_insight_search", "insights", "amendment_candidates", "updates", "validation"}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
EVENT_TYPES = {"debate", "discovery", "decision", "incident"}
DOMAINS = {"universal", "security", "frontend", "backend", "testing", "deployment", "governance", "workflow"}
STATUSES = {"active", "tentative", "superseded", "rejected"}
DUPLICATE_DECISIONS = {"new", "refine", "supersede", "reject_duplicate"}
AMENDMENT_STATUS = {"proposed", "not_needed"}
CHECKS = {"assets", "deterministic_scripts", "quality_criteria", "prior_insight_search", "insight_contract", "duplicate_policy", "amendment_gate", "evidence_required", "update_plan"}


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


def text(obj: dict[str, Any], key: str, ctx: str, errors: list[str]) -> None:
    require(isinstance(obj.get(key), str) and bool(obj[key].strip()), errors, f"{ctx}.{key} required")


def tag(obj: dict[str, Any], ctx: str, errors: list[str]) -> None:
    require(obj.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")


def validate_source_event(data: dict[str, Any], errors: list[str]) -> None:
    event = data.get("source_event")
    require(isinstance(event, dict), errors, "source_event must be object")
    if not isinstance(event, dict):
        return
    require(event.get("event_type") in EVENT_TYPES, errors, "source_event.event_type invalid")
    for field in ("topic", "date", "direct_answer", "question_refinements", "coverage_gaps"):
        text(event, field, "source_event", errors)
    tag(event, "source_event", errors)


def validate_prior_search(data: dict[str, Any], errors: list[str]) -> None:
    search = data.get("prior_insight_search")
    require(isinstance(search, dict), errors, "prior_insight_search must be object")
    if not isinstance(search, dict):
        return
    require(search.get("searched") is True, errors, "prior_insight_search.searched must be true")
    require(isinstance(search.get("domains"), list) and bool(search["domains"]), errors, "prior_insight_search.domains required")
    require(isinstance(search.get("matches"), list), errors, "prior_insight_search.matches must be list")
    tag(search, "prior_insight_search", errors)


def validate_insights(data: dict[str, Any], errors: list[str]) -> None:
    insights = objects(data.get("insights"), "insights", errors)
    require(bool(insights), errors, "insights required")
    seen_active: set[str] = set()
    for i, insight in enumerate(insights):
        ctx = f"insights[{i}]"
        for field in ("title", "pattern", "rationale", "constitutional_anchor"):
            text(insight, field, ctx, errors)
        require(insight.get("domain") in DOMAINS, errors, f"{ctx}.domain invalid")
        require(insight.get("status") in STATUSES, errors, f"{ctx}.status invalid")
        require(insight.get("duplicate_decision") in DUPLICATE_DECISIONS, errors, f"{ctx}.duplicate_decision invalid")
        require(isinstance(insight.get("triggers"), list) and bool(insight["triggers"]), errors, f"{ctx}.triggers required")
        if insight.get("status") == "active":
            key = str(insight.get("title", "")).strip().lower()
            require(key not in seen_active, errors, f"{ctx}: duplicate active insight title")
            seen_active.add(key)
        if insight.get("duplicate_decision") == "reject_duplicate":
            text(insight, "existing_insight_id", ctx, errors)
            require(insight.get("status") == "rejected", errors, f"{ctx}: rejected duplicate must have status rejected")
        tag(insight, ctx, errors)


def validate_amendments(data: dict[str, Any], errors: list[str]) -> None:
    candidates = objects(data.get("amendment_candidates"), "amendment_candidates", errors)
    for i, candidate in enumerate(candidates):
        ctx = f"amendment_candidates[{i}]"
        text(candidate, "ambiguity_class", ctx, errors)
        count = candidate.get("recurrence_count")
        require(isinstance(count, int) and count >= 0, errors, f"{ctx}.recurrence_count must be non-negative integer")
        require(candidate.get("status") in AMENDMENT_STATUS, errors, f"{ctx}.status invalid")
        if candidate.get("status") == "proposed":
            require(isinstance(count, int) and count >= 3, errors, f"{ctx}: proposed amendment requires recurrence_count >= 3")
            text(candidate, "rationale", ctx, errors)
            text(candidate, "proposal_path", ctx, errors)
            if isinstance(candidate.get("proposal_path"), str):
                require(candidate["proposal_path"].startswith(".specify/adr/"), errors, f"{ctx}.proposal_path must be under .specify/adr/")
        tag(candidate, ctx, errors)


def validate_updates(data: dict[str, Any], errors: list[str]) -> None:
    updates = data.get("updates")
    require(isinstance(updates, dict), errors, "updates must be object")
    if not isinstance(updates, dict):
        return
    files = updates.get("insight_files")
    require(isinstance(files, list) and bool(files), errors, "updates.insight_files required")
    if isinstance(files, list):
        for path in files:
            require(isinstance(path, str) and path.startswith("insights/") and path.endswith(".md"), errors, f"updates invalid insight file: {path}")
    require(updates.get("index_updated") is True, errors, "updates.index_updated must be true")
    require(isinstance(updates.get("cross_references"), list), errors, "updates.cross_references must be list")
    tag(updates, "updates", errors)


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if not isinstance(validation, dict):
        return
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    checks = validation.get("checks")
    require(isinstance(checks, list), errors, "validation.checks must be list")
    if isinstance(checks, list):
        require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "continuous-learning", errors, "skill must be continuous-learning")
    validate_source_event(data, errors)
    validate_prior_search(data, errors)
    validate_insights(data, errors)
    validate_amendments(data, errors)
    validate_updates(data, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_continuous_learning_report.py <report.json>", file=sys.stderr)
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
