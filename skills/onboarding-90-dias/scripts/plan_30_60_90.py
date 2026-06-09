#!/usr/bin/env python3
"""Validate sustainable 30/60/90 onboarding plans offline.

Exit 0 valid, 1 blocked or invalid plan, 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_PHASES = [30, 60, 90]
MAX_HOURS = 45
MAX_PRIORITIES = 4
EVIDENCE_TYPES = {"role_brief", "manager_input", "user_constraint", "stakeholder_note", "team_doc", "manual_entry"}
HUSTLE_TERMS = ["always-on", "24/7", "sin descanso", "no dormir", "hustle", "siempre disponible"]
PROMISE_TERMS = ["garantiza promocion", "asegura ascenso", "resultado garantizado", "exito seguro"]


def normalize(text: str) -> str:
    return text.translate(str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")).lower()


def specific(value: Any) -> bool:
    return len(str(value or "").strip().split()) >= 3


def short_label(value: Any) -> bool:
    return len(str(value or "").strip().split()) >= 2


def number(value: Any, field: str, issues: list[str], minimum: float = 0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        issues.append(f"{field} must be numeric")
        return 0.0
    if result < minimum:
        issues.append(f"{field} must be >= {minimum:g}")
    return result


def validate_evidence(items: Any) -> tuple[set[str], list[str]]:
    issues: list[str] = []
    refs: set[str] = set()
    if not isinstance(items, list) or not items:
        return refs, ["evidence must contain at least one item"]
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            issues.append(f"evidence[{index}] must be an object")
            continue
        ref = str(item.get("id", "")).strip()
        if not ref:
            issues.append(f"evidence[{index}].id is required")
        else:
            refs.add(ref)
        if item.get("type") not in EVIDENCE_TYPES:
            issues.append(f"unsupported evidence type: {item.get('type')}")
        if not specific(item.get("detail")):
            issues.append(f"evidence[{index}].detail must be specific")
    return refs, issues


def text_issues(data: Any) -> list[str]:
    text = normalize(json.dumps(data, ensure_ascii=False))
    issues: list[str] = []
    for term in HUSTLE_TERMS:
        if normalize(term) in text:
            issues.append(f"blocked hustle term: {term}")
    for term in PROMISE_TERMS:
        if normalize(term) in text:
            issues.append(f"unsupported promise term: {term}")
    return issues


def validate_priority(priority: Any, phase: int, index: int, refs: set[str]) -> list[str]:
    issues: list[str] = []
    label = f"phase_{phase}.priorities[{index}]"
    if not isinstance(priority, dict):
        return [f"{label} must be an object"]
    for field in ["title", "deliverable", "validation_signal"]:
        if not specific(priority.get(field)):
            issues.append(f"{label}.{field} must be specific")
    evidence_ref = str(priority.get("evidence_ref", "")).strip()
    if evidence_ref not in refs:
        issues.append(f"{label}.evidence_ref must reference supplied evidence")
    number(priority.get("estimated_hours_per_week"), f"{label}.estimated_hours_per_week", issues, 0)
    return issues


def validate_phases(phases: Any, refs: set[str]) -> list[str]:
    issues: list[str] = []
    if not isinstance(phases, list):
        return ["phases must be a list"]
    seen: set[int] = set()
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            issues.append(f"phases[{index}] must be an object")
            continue
        try:
            day = int(phase.get("day"))
        except (TypeError, ValueError):
            issues.append(f"phases[{index}].day must be 30, 60, or 90")
            continue
        if day not in REQUIRED_PHASES:
            issues.append(f"unsupported phase day: {day}")
        if day in seen:
            issues.append(f"duplicate phase day: {day}")
        seen.add(day)
        if not specific(phase.get("theme")):
            issues.append(f"phase_{day}.theme must be specific")
        priorities = phase.get("priorities")
        if not isinstance(priorities, list) or not priorities:
            issues.append(f"phase_{day}.priorities must contain at least one item")
            continue
        if len(priorities) > MAX_PRIORITIES:
            issues.append(f"phase_{day}.priorities has {len(priorities)} items > {MAX_PRIORITIES}")
        for p_index, priority in enumerate(priorities):
            issues.extend(validate_priority(priority, day, p_index, refs))
    for required in REQUIRED_PHASES:
        if required not in seen:
            issues.append(f"missing phase: {required}")
    return issues


def validate_packet(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if data.get("schema") != 1:
        issues.append("schema must be 1")
    if data.get("skill") != "onboarding-90-dias":
        issues.append("skill must be onboarding-90-dias")
    role = data.get("role")
    if not isinstance(role, dict):
        issues.append("role must be an object")
    else:
        if not short_label(role.get("title")):
            issues.append("role.title must be specific")
        if not specific(role.get("context")):
            issues.append("role.context must be specific")
    constraints = data.get("constraints")
    if not isinstance(constraints, dict):
        issues.append("constraints must be an object")
        weekly_hours = 0.0
    else:
        weekly_hours = number(constraints.get("weekly_hours"), "constraints.weekly_hours", issues, 0)
        recovery_days = number(constraints.get("recovery_days_per_week", 0), "constraints.recovery_days_per_week", issues, 0)
        if recovery_days < 1:
            issues.append("constraints.recovery_days_per_week must be >= 1")
    if weekly_hours > MAX_HOURS:
        issues.append(f"weekly_hours {weekly_hours:g} > {MAX_HOURS}")
    refs, evidence_issues = validate_evidence(data.get("evidence"))
    issues.extend(evidence_issues)
    issues.extend(validate_phases(data.get("phases"), refs))
    stakeholders = data.get("stakeholders", [])
    if not isinstance(stakeholders, list):
        issues.append("stakeholders must be a list")
    elif not stakeholders:
        issues.append("stakeholders must contain at least one entry or open question")
    issues.extend(text_issues(data))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sustainable 30/60/90 onboarding plans")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
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

    issues = validate_packet(data)
    role_title = data.get("role", {}).get("title", "(role)") if isinstance(data.get("role"), dict) else "(role)"
    print(f"Plan 30/60/90: {role_title}")
    if issues:
        print("STATUS: BLOCKED")
        for issue in issues:
            print(f"  ISSUE: {issue}")
        return 1
    print("STATUS: PASS")
    print("anti_burnout=pass phases=3 max_priorities_per_phase<=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
