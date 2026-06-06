#!/usr/bin/env python3
"""Validate deterministic Session Manager JSON reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = [
    "schema_version",
    "skill",
    "context_snapshot",
    "priming_sources",
    "stage_computation",
    "persistence_actions",
    "next_action",
    "guardian_decision",
]
TAGS = {"[CODE]", "[CONFIG]", "[DOC]", "[INFERENCE]", "[ASSUMPTION]", "[OPEN]"}
CONTEXT_STATUSES = {"present", "missing", "invalid"}
SOURCE_STATUSES = {"loaded", "missing", "skipped"}
STAGES = ["specified", "planned", "testified", "tasks-ready", "implementing", "complete"]
WRITE_ACTIONS = {"create", "update", "append"}
ALLOWED_TARGETS = {
    ".specify/context.json",
    ".specify/score-history.json",
    ".specify/decisions/",
}
DECISIONS = {"pass", "block"}


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def text(obj: dict, key: str, ctx: str, errors: list[str]) -> None:
    if not isinstance(obj.get(key), str) or not obj[key].strip():
        errors.append(f"{ctx}: missing non-empty {key}")


def tag(obj: dict, ctx: str, errors: list[str]) -> None:
    if obj.get("evidence_tag") not in TAGS:
        errors.append(f"{ctx}: evidence_tag must be one of {sorted(TAGS)}")


def stage_index(stage: str) -> int:
    return STAGES.index(stage)


def context_snapshot(data: dict, errors: list[str]) -> None:
    item = data.get("context_snapshot")
    if not isinstance(item, dict):
        errors.append("context_snapshot: must be an object")
        return
    text(item, "context_path", "context_snapshot", errors)
    text(item, "active_feature", "context_snapshot", errors)
    if item.get("context_status") not in CONTEXT_STATUSES:
        errors.append(f"context_snapshot: context_status must be one of {sorted(CONTEXT_STATUSES)}")
    if item.get("recorded_stage") not in STAGES:
        errors.append(f"context_snapshot: recorded_stage must be one of {STAGES}")
    tag(item, "context_snapshot", errors)


def priming_sources(data: dict, errors: list[str]) -> None:
    rows = data.get("priming_sources")
    if not isinstance(rows, list) or not rows:
        errors.append("priming_sources: must be a non-empty list")
        return
    orders = []
    sources = set()
    for index, row in enumerate(rows):
        ctx = f"priming_sources[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        if isinstance(row.get("order"), int):
            orders.append(row["order"])
        else:
            errors.append(f"{ctx}: order must be an integer")
        text(row, "source", ctx, errors)
        sources.add(row.get("source"))
        if row.get("status") not in SOURCE_STATUSES:
            errors.append(f"{ctx}: status must be one of {sorted(SOURCE_STATUSES)}")
        tag(row, ctx, errors)
    if orders != sorted(orders):
        errors.append("priming_sources: orders must be sorted")
    if ".specify/context.json" not in sources:
        errors.append("priming_sources: .specify/context.json must be represented")


def artifact_evidence(rows: object, errors: list[str]) -> tuple[bool, bool]:
    if not isinstance(rows, list) or not rows:
        errors.append("stage_computation.artifact_evidence: must be a non-empty list")
        return False, False
    tasks_exist = False
    validation_exists = False
    for index, row in enumerate(rows):
        ctx = f"stage_computation.artifact_evidence[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "artifact", ctx, errors)
        if not isinstance(row.get("exists"), bool):
            errors.append(f"{ctx}: exists must be boolean")
        artifact = str(row.get("artifact", ""))
        exists = row.get("exists") is True
        if exists and artifact in {"tasks.md", ".specify/tasks.md"}:
            tasks_exist = True
        if exists and "validation" in artifact:
            validation_exists = True
        tag(row, ctx, errors)
    return tasks_exist, validation_exists


def stage_computation(data: dict, errors: list[str]) -> None:
    item = data.get("stage_computation")
    if not isinstance(item, dict):
        errors.append("stage_computation: must be an object")
        return
    previous = item.get("previous_stage")
    computed = item.get("computed_stage")
    if previous not in STAGES:
        errors.append(f"stage_computation: previous_stage must be one of {STAGES}")
    if computed not in STAGES:
        errors.append(f"stage_computation: computed_stage must be one of {STAGES}")
    tasks_exist, validation_exists = artifact_evidence(item.get("artifact_evidence"), errors)
    progress = item.get("implementation_progress_percent")
    if not isinstance(progress, int) or progress < 0 or progress > 100:
        errors.append("stage_computation: implementation_progress_percent must be 0..100")
    if not isinstance(item.get("tasks_complete"), bool):
        errors.append("stage_computation: tasks_complete must be boolean")
    if computed in STAGES and previous in STAGES and stage_index(computed) - stage_index(previous) > 1:
        errors.append("stage_computation: cannot advance more than one stage per pass")
    if computed == "implementing":
        if not tasks_exist:
            errors.append("stage_computation: implementing requires task evidence")
        if not isinstance(progress, int) or not 1 <= progress <= 99:
            errors.append("stage_computation: implementing requires progress 1..99")
    if computed == "complete":
        if item.get("tasks_complete") is not True:
            errors.append("stage_computation: complete requires tasks_complete=true")
        if validation_exists is not True:
            errors.append("stage_computation: complete requires validation evidence")
        if progress != 100:
            errors.append("stage_computation: complete requires progress 100")
    tag(item, "stage_computation", errors)


def persistence_actions(data: dict, errors: list[str]) -> None:
    rows = data.get("persistence_actions")
    if not isinstance(rows, list):
        errors.append("persistence_actions: must be a list")
        return
    for index, row in enumerate(rows):
        ctx = f"persistence_actions[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{ctx}: must be an object")
            continue
        text(row, "target", ctx, errors)
        text(row, "action", ctx, errors)
        target = row.get("target")
        action = row.get("action")
        if action in WRITE_ACTIONS:
            if target not in ALLOWED_TARGETS:
                errors.append(f"{ctx}: target is outside allowed persistence targets")
            if row.get("authorized") is not True:
                errors.append(f"{ctx}: write action requires authorized=true")
        elif action != "none":
            errors.append(f"{ctx}: action must be one of {sorted(WRITE_ACTIONS | {'none'})}")
        if not isinstance(row.get("authorized"), bool):
            errors.append(f"{ctx}: authorized must be boolean")
        text(row, "rationale", ctx, errors)
        tag(row, ctx, errors)


def next_action(data: dict, errors: list[str]) -> None:
    item = data.get("next_action")
    if not isinstance(item, dict):
        errors.append("next_action: must be an object")
        return
    text(item, "recommended", "next_action", errors)
    text(item, "rationale", "next_action", errors)
    if item.get("stage") not in STAGES:
        errors.append(f"next_action: stage must be one of {STAGES}")
    tag(item, "next_action", errors)


def guardian_decision(data: dict, errors: list[str]) -> None:
    item = data.get("guardian_decision")
    if not isinstance(item, dict):
        errors.append("guardian_decision: must be an object")
        return
    if item.get("decision") not in DECISIONS:
        errors.append(f"guardian_decision: decision must be one of {sorted(DECISIONS)}")
    text(item, "rationale", "guardian_decision", errors)
    tag(item, "guardian_decision", errors)
    context_status = data.get("context_snapshot", {}).get("context_status")
    if item.get("decision") == "pass" and context_status != "present":
        errors.append("guardian_decision: pass requires present context")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("skill") != "session-manager":
        errors.append("skill must be session-manager")
    context_snapshot(data, errors)
    priming_sources(data, errors)
    stage_computation(data, errors)
    persistence_actions(data, errors)
    next_action(data, errors)
    guardian_decision(data, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Session Manager JSON report")
    parser.add_argument("report")
    args = parser.parse_args()
    path = Path(args.report)
    try:
        data = load(path)
    except ValueError as exc:
        print(f"ERROR: {path}: {exc}")
        return 1
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {path}: {error}")
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
