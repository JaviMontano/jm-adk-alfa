#!/usr/bin/env python3
"""Validate deterministic Session Lifecycle Management JSON reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.session-lifecycle-management.report.v1"
REQUIRED_TOP = {"schema", "skill", "transition", "reason", "context", "staleness_results", "typed_summary", "forks", "validation"}
TRANSITIONS = {"resume", "fork", "fresh"}
SIGNALS = {"mtime", "hash", "head", "path", "schema"}
STATUSES = {"fresh", "stale"}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
CHECKS = {"assets", "deterministic_scripts", "quality_criteria", "staleness_detected", "typed_summary", "transition_traced", "fork_isolation", "evidence_required"}


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


def validate_context(data: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    ctx = data.get("context")
    require(isinstance(ctx, dict), errors, "context must be object")
    if not isinstance(ctx, dict):
        return {}
    text(ctx, "goal", "context", errors)
    require(isinstance(ctx.get("goal_branchable"), bool), errors, "context.goal_branchable must be boolean")
    require(isinstance(ctx.get("shares_mutable_state"), bool), errors, "context.shares_mutable_state must be boolean")
    tag(ctx, "context", errors)
    return ctx


def validate_staleness(data: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    rows = objects(data.get("staleness_results"), "staleness_results", errors)
    require(bool(rows), errors, "staleness_results required")
    for i, row in enumerate(rows):
        ctx = f"staleness_results[{i}]"
        for field in ("result_id", "source"):
            text(row, field, ctx, errors)
        require(row.get("signal_type") in SIGNALS, errors, f"{ctx}.signal_type invalid")
        require(row.get("status") in STATUSES, errors, f"{ctx}.status invalid")
        require(isinstance(row.get("critical"), bool), errors, f"{ctx}.critical must be boolean")
        tag(row, ctx, errors)
    return rows


def validate_typed_summary(summary: Any, transition: str, stale_rows: list[dict[str, Any]], errors: list[str]) -> None:
    critical_stale = [row for row in stale_rows if row.get("critical") is True and row.get("status") == "stale"]
    if transition != "fresh":
        require(summary is None, errors, "typed_summary must be null unless transition is fresh")
        return
    require(isinstance(summary, dict), errors, "fresh transition requires typed_summary object")
    if not isinstance(summary, dict):
        return
    for field in ("goal", "decisions", "open_questions", "verified_facts", "stale_dropped"):
        require(field in summary, errors, f"typed_summary.{field} required")
    require(summary.get("raw_transcript_allowed") is False, errors, "typed_summary.raw_transcript_allowed must be false")
    require(isinstance(summary.get("stale_dropped"), list) and bool(summary["stale_dropped"]), errors, "typed_summary.stale_dropped required")
    if critical_stale and isinstance(summary.get("stale_dropped"), list):
        dropped = set(summary["stale_dropped"])
        for row in critical_stale:
            require(row.get("source") in dropped, errors, f"typed_summary must drop stale source {row.get('source')}")


def validate_forks(data: dict[str, Any], transition: str, lifecycle_context: dict[str, Any], errors: list[str]) -> None:
    forks = objects(data.get("forks"), "forks", errors)
    if transition != "fork":
        require(not forks, errors, "forks must be empty unless transition is fork")
        return
    require(lifecycle_context.get("goal_branchable") is True, errors, "fork requires branchable goal")
    require(lifecycle_context.get("shares_mutable_state") is False, errors, "fork requires no shared mutable state")
    require(bool(forks), errors, "fork transition requires forks")
    for i, fork in enumerate(forks):
        ctx = f"forks[{i}]"
        text(fork, "branch", ctx, errors)
        text(fork, "workspace", ctx, errors)
        require(fork.get("isolated_scratchpad") is True, errors, f"{ctx}.isolated_scratchpad must be true")
        require(fork.get("isolated_workspace") is True, errors, f"{ctx}.isolated_workspace must be true")
        tag(fork, ctx, errors)


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
    transition = data.get("transition")
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "session-lifecycle-management", errors, "skill must be session-lifecycle-management")
    require(transition in TRANSITIONS, errors, "transition invalid")
    require(bool(data.get("reason")), errors, "reason required")
    lifecycle_context = validate_context(data, errors)
    stale_rows = validate_staleness(data, errors)
    critical_stale = any(row.get("critical") is True and row.get("status") == "stale" for row in stale_rows)
    if critical_stale:
        require(transition == "fresh", errors, "critical stale result requires fresh transition")
    if transition == "resume":
        require(not critical_stale, errors, "resume requires no critical stale results")
    validate_typed_summary(data.get("typed_summary"), str(transition), stale_rows, errors)
    validate_forks(data, str(transition), lifecycle_context, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_session_lifecycle_report.py <report.json>", file=sys.stderr)
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
