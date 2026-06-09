#!/usr/bin/env python3
"""Validate a SEL-EMPRESA notebook source inventory offline.

Exit 0 complete, 1 blocked or invalid packet, 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SLOTS = [
    "job-description",
    "empresa-research",
    "proceso-log",
    "entrevista-notas",
    "material-prep",
    "oferta-precontrato",
    "notas-gratitud",
    "post-mortem",
]
EVIDENCE_TYPES = {"exported_doc", "user_note", "source_excerpt", "metadata", "manual_entry"}
ALLOWED_ACTIONS = {"add_source", "mark_missing", "dedupe", "rename_slot", "request_export", "mark_optional"}
BLOCKED_ACTIONS = {"delete_all", "live_fetch", "notebooklm_sync", "browse_url", "invent_summary"}


def specific(text: Any) -> bool:
    return len(str(text or "").strip().split()) >= 3


def validate_sources(sources: Any) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    missing: list[str] = []
    if not isinstance(sources, list) or not sources:
        return SLOTS[:], ["sources must contain canonical slot objects"]

    seen: dict[str, int] = {}
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            issues.append(f"sources[{index}] must be an object")
            continue
        slot = str(source.get("slot", "")).strip()
        if slot not in SLOTS:
            issues.append(f"unsupported slot: {slot}")
            continue
        seen[slot] = seen.get(slot, 0) + 1
        if seen[slot] > 1:
            issues.append(f"duplicate slot: {slot}")
        if not str(source.get("title", "")).strip():
            issues.append(f"{slot}.title is required")
        evidence_type = source.get("evidence_type")
        if evidence_type not in EVIDENCE_TYPES:
            issues.append(f"{slot}.evidence_type unsupported: {evidence_type}")
        if not specific(source.get("evidence_detail")):
            issues.append(f"{slot}.evidence_detail must be specific")
        if source.get("requires_network") is True:
            issues.append(f"{slot}.requires_network is blocked")
        if source.get("content_claim") and not specific(source.get("content_evidence")):
            issues.append(f"{slot}.content_claim requires content_evidence")

    missing = [slot for slot in SLOTS if slot not in seen]
    return missing, issues


def validate_actions(actions: Any) -> list[str]:
    if actions in (None, []):
        return []
    if not isinstance(actions, list):
        return ["curation_actions must be a list"]
    issues: list[str] = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            issues.append(f"curation_actions[{index}] must be an object")
            continue
        action_id = action.get("action")
        if action_id in BLOCKED_ACTIONS:
            issues.append(f"blocked curation action: {action_id}")
        elif action_id not in ALLOWED_ACTIONS:
            issues.append(f"unsupported curation action: {action_id}")
        if not specific(action.get("reason")):
            issues.append(f"curation_actions[{index}].reason must be specific")
    return issues


def validate_packet(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    if data.get("schema") != 1:
        issues.append("schema must be 1")
    if data.get("skill") != "notebook-curator-seleccion":
        issues.append("skill must be notebook-curator-seleccion")
    if data.get("archetype") != "SEL-EMPRESA":
        issues.append("archetype must be SEL-EMPRESA")
    if not str(data.get("notebook_id", "")).startswith("SEL-"):
        issues.append("notebook_id must start with SEL-")
    if data.get("retrieval_mode") != "offline":
        issues.append("retrieval_mode must be offline")
    if data.get("notebooklm_sync") is True:
        issues.append("notebooklm_sync is blocked in deterministic validation")

    missing, source_issues = validate_sources(data.get("sources"))
    issues.extend(source_issues)
    issues.extend(validate_actions(data.get("curation_actions")))
    return missing, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SEL-EMPRESA notebook archetype")
    parser.add_argument("--input")
    parser.add_argument("--emit", action="store_true", help="Print canonical checklist")
    args = parser.parse_args()
    if args.emit:
        print("[SEL-EMPRESA] canonical source slots:")
        for slot in SLOTS:
            print(f"  - {slot}")
        return 0
    if not args.input:
        print("ERROR: --input is required unless --emit is used")
        return 3
    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: not found: {path}")
        return 3
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: bad JSON: {exc}")
        return 3
    if not isinstance(data, dict):
        print("ERROR: JSON root must be an object")
        return 3

    missing, issues = validate_packet(data)
    complete = not missing and not issues
    print(f"archetype={'COMPLETE' if complete else 'BLOCKED'} present={len(SLOTS) - len(missing)}/{len(SLOTS)}")
    for slot in missing:
        print(f"  MISSING: {slot}")
    for issue in issues:
        print(f"  ISSUE: {issue}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
