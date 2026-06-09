#!/usr/bin/env python3
"""Validate deterministic selection-process board reports."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RELATIVE_DATE_TERMS = (
    "today",
    "tomorrow",
    "yesterday",
    "next ",
    "last ",
    "ayer",
    "manana",
    "mañana",
    "proximo",
    "próximo",
    "siguiente semana",
)
GUARANTEE_TERMS = (
    "guaranteed hire",
    "guaranteed offer",
    "guaranteed outcome",
    "contratacion garantizada",
    "contratación garantizada",
    "oferta garantizada",
    "seleccion garantizada",
    "selección garantizada",
)
ALLOWED_EVIDENCE_TYPES = {
    "copied_email",
    "recruiter_note",
    "interview_note",
    "manual_entry",
    "scheduler_note",
    "feedback_summary",
}
ALLOWED_STATUSES = {"pending", "scheduled", "completed", "blocked", "declined", "unknown"}
ALLOWED_RISK_SEVERITIES = {"low", "medium", "high"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def as_list(data: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{key} must be a non-empty list")
        return []
    items: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
        else:
            items.append(item)
    return items


def text(value: Any) -> str:
    return str(value or "").strip()


def normalized(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().split())


def contains_term(value: Any, terms: tuple[str, ...]) -> bool:
    haystack = normalized(str(value))
    return any(normalized(term) in haystack for term in terms)


def require_iso_date(value: Any, label: str, errors: list[str]) -> None:
    raw = text(value)
    if not raw:
        errors.append(f"{label} is required")
        return
    if contains_term(raw, RELATIVE_DATE_TERMS):
        errors.append(f"{label} must not be relative: {raw}")
        return
    if not ISO_DATE.match(raw):
        errors.append(f"{label} must use YYYY-MM-DD: {raw}")


def duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return dupes


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("skill") != "proceso-seleccion-orchestrator":
        errors.append("skill must be proceso-seleccion-orchestrator")

    candidate = data.get("candidate")
    if not isinstance(candidate, dict):
        errors.append("candidate must be an object")
    else:
        if not text(candidate.get("alias")):
            errors.append("candidate.alias is required")
        if not text(candidate.get("target_role")):
            errors.append("candidate.target_role is required")

    board = data.get("board")
    if not isinstance(board, dict):
        errors.append("board must be an object")
    else:
        if text(board.get("status")) not in {"active", "blocked", "closed"}:
            errors.append("board.status must be active, blocked, or closed")
        require_iso_date(board.get("as_of"), "board.as_of", errors)

    evidence = as_list(data, "evidence", errors)
    contacts = as_list(data, "contacts", errors)
    stages = as_list(data, "stages", errors)
    risks = data.get("risks", [])
    if not isinstance(risks, list):
        errors.append("risks must be a list")
        risks = []

    evidence_ids: list[str] = []
    for item in evidence:
        ev_id = text(item.get("id"))
        if not ev_id:
            errors.append("evidence.id is required")
        evidence_ids.append(ev_id)
        if text(item.get("type")) not in ALLOWED_EVIDENCE_TYPES:
            errors.append(f"{ev_id}: unsupported evidence type")
        require_iso_date(item.get("received_date"), f"{ev_id}.received_date", errors)
        for key in ("source", "summary"):
            if not text(item.get(key)):
                errors.append(f"{ev_id}.{key} is required")
        if contains_term(item, GUARANTEE_TERMS):
            errors.append(f"{ev_id}: guaranteed outcome language must be blocked, not accepted")
    for duplicate in duplicate_values([item for item in evidence_ids if item]):
        errors.append(f"duplicate evidence id: {duplicate}")
    evidence_id_set = set(evidence_ids)

    for contact in contacts:
        label = text(contact.get("name")) or "contact"
        if not text(contact.get("name")):
            errors.append("contact.name is required")
        if not text(contact.get("role")):
            errors.append(f"{label}.role is required")
        ref = text(contact.get("evidence_ref"))
        if ref not in evidence_id_set:
            errors.append(f"{label}.evidence_ref is unresolved: {ref}")

    stage_ids: list[str] = []
    sequences: list[str] = []
    stage_status_by_key: dict[str, str] = {}
    for stage in stages:
        stage_id = text(stage.get("id"))
        stage_ids.append(stage_id)
        sequence = str(stage.get("sequence", "")).strip()
        sequences.append(sequence)
        if not stage_id:
            errors.append("stage.id is required")
        if not isinstance(stage.get("sequence"), int) or int(stage.get("sequence", 0)) < 1:
            errors.append(f"{stage_id}.sequence must be a positive integer")
        for key in ("label", "owner", "status_reason"):
            if not text(stage.get(key)):
                errors.append(f"{stage_id}.{key} is required")
        status = text(stage.get("status"))
        if status not in ALLOWED_STATUSES:
            errors.append(f"{stage_id}.status is unsupported: {status}")
        ref = text(stage.get("evidence_ref"))
        if ref not in evidence_id_set:
            errors.append(f"{stage_id}.evidence_ref is unresolved: {ref}")
        if contains_term(stage, RELATIVE_DATE_TERMS):
            errors.append(f"{stage_id}: relative date text must be blocked")
        if contains_term(stage, GUARANTEE_TERMS):
            errors.append(f"{stage_id}: guaranteed outcome language must be blocked")
        conflict_key = f"{normalized(text(stage.get('label')))}|{normalized(text(stage.get('owner')))}"
        prior_status = stage_status_by_key.get(conflict_key)
        if prior_status and prior_status != status:
            errors.append(f"{stage_id}: conflicting status for same stage owner")
        stage_status_by_key[conflict_key] = status
    for duplicate in duplicate_values([sid for sid in stage_ids if sid]):
        errors.append(f"duplicate stage id: {duplicate}")
    for duplicate in duplicate_values([seq for seq in sequences if seq]):
        errors.append(f"duplicate stage sequence: {duplicate}")
    stage_id_set = set(stage_ids)

    next_action = data.get("next_action")
    if not isinstance(next_action, dict):
        errors.append("next_action must be an object")
    else:
        for key in ("owner", "action", "stage_id", "evidence_ref"):
            if not text(next_action.get(key)):
                errors.append(f"next_action.{key} is required")
        if text(next_action.get("stage_id")) not in stage_id_set:
            errors.append("next_action.stage_id is unresolved")
        if text(next_action.get("evidence_ref")) not in evidence_id_set:
            errors.append("next_action.evidence_ref is unresolved")
        due_date = text(next_action.get("due_date"))
        if due_date:
            require_iso_date(due_date, "next_action.due_date", errors)
        if contains_term(next_action, RELATIVE_DATE_TERMS):
            errors.append("next_action contains relative date text")
        if contains_term(next_action, GUARANTEE_TERMS):
            errors.append("next_action contains guaranteed outcome language")

    for risk in risks:
        risk_id = text(risk.get("id")) or "risk"
        if text(risk.get("severity")) not in ALLOWED_RISK_SEVERITIES:
            errors.append(f"{risk_id}.severity is unsupported")
        for key in ("description", "mitigation"):
            if not text(risk.get(key)):
                errors.append(f"{risk_id}.{key} is required")
        ref = text(risk.get("evidence_ref"))
        if ref and ref not in evidence_id_set:
            errors.append(f"{risk_id}.evidence_ref is unresolved: {ref}")

    validation = data.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("offline") is not True:
            errors.append("validation.offline must be true")
        if validation.get("network_used") not in (False, None):
            errors.append("validation.network_used must be false")
        if text(validation.get("result")) not in {"pass", "blocked"}:
            errors.append("validation.result must be pass or blocked")

    if errors and isinstance(board, dict) and text(board.get("status")) == "active":
        errors.append("board.status must not be active when validation errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate proceso-seleccion-orchestrator JSON board")
    parser.add_argument("--input", required=True, help="Path to a selection board JSON file")
    args = parser.parse_args()

    path = Path(args.input)
    try:
        data = load_json(path)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3

    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"selection_board={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
