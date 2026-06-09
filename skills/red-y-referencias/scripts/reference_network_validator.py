#!/usr/bin/env python3
"""Validate deterministic reference-network packets."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DIRECT_EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE_LIKE = re.compile(r"(?:\+\d[\d .()-]{7,}\d|\b\d{3}[ .()-]?\d{3}[ .()-]?\d{4}\b)")
RELATIVE_DATE_TERMS = ("today", "tomorrow", "yesterday", "next ", "last ", "ayer", "manana", "mañana")
EVIDENCE_TYPES = {"consent_message", "manual_note", "referral_context", "followup_log", "relationship_note"}
CONSENT_STATUSES = {"explicit_granted", "explicit_denied", "not_requested", "expired", "unknown"}
ACTION_TYPES = {"list_reference", "recruiter_contact", "request_consent", "ask_intro", "send_thanks", "follow_up", "no_contact"}
CONSENT_REQUIRED_ACTIONS = {"list_reference", "recruiter_contact", "ask_intro"}
FOLLOWUP_DAYS = 30


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def text(value: Any) -> str:
    return str(value or "").strip()


def all_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(all_text(v) for v in value)
    return text(value)


def as_list(data: dict[str, Any], key: str, errors: list[str], allow_empty: bool = False) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or (not value and not allow_empty):
        errors.append(f"{key} must be a {'list' if allow_empty else 'non-empty list'}")
        return []
    out: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
        else:
            out.append(item)
    return out


def has_relative_date(value: Any) -> bool:
    haystack = all_text(value).lower()
    return any(term in haystack for term in RELATIVE_DATE_TERMS)


def has_contact_detail(value: Any) -> bool:
    haystack = all_text(value)
    return bool(DIRECT_EMAIL.search(haystack) or PHONE_LIKE.search(haystack))


def require_iso(value: Any, label: str, errors: list[str]) -> date | None:
    raw = text(value)
    if not raw:
        errors.append(f"{label} is required")
        return None
    if has_relative_date(raw):
        errors.append(f"{label} must not be relative: {raw}")
        return None
    if not ISO_DATE.match(raw):
        errors.append(f"{label} must use YYYY-MM-DD: {raw}")
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        errors.append(f"{label} is not a valid calendar date: {raw}")
        return None


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
    if data.get("skill") != "red-y-referencias":
        errors.append("skill must be red-y-referencias")

    packet = data.get("packet")
    as_of: date | None = None
    if not isinstance(packet, dict):
        errors.append("packet must be an object")
    else:
        if text(packet.get("status")) not in {"active", "blocked", "closed"}:
            errors.append("packet.status must be active, blocked, or closed")
        as_of = require_iso(packet.get("as_of"), "packet.as_of", errors)

    evidence = as_list(data, "evidence", errors)
    contacts = as_list(data, "contacts", errors)
    actions = as_list(data, "actions", errors, allow_empty=True)
    edges = as_list(data, "network_edges", errors, allow_empty=True)
    blockers = data.get("blockers", [])
    if not isinstance(blockers, list):
        errors.append("blockers must be a list")
        blockers = []

    if has_contact_detail(data):
        errors.append("packet must not expose direct email or phone details")
    if has_relative_date(data):
        errors.append("packet must not contain relative date text")

    evidence_ids: list[str] = []
    for item in evidence:
        ev_id = text(item.get("id"))
        evidence_ids.append(ev_id)
        if not ev_id:
            errors.append("evidence.id is required")
        if text(item.get("type")) not in EVIDENCE_TYPES:
            errors.append(f"{ev_id}: unsupported evidence type")
        require_iso(item.get("date"), f"{ev_id}.date", errors)
        for key in ("source", "summary"):
            if not text(item.get(key)):
                errors.append(f"{ev_id}.{key} is required")
    for duplicate in duplicate_values([item for item in evidence_ids if item]):
        errors.append(f"duplicate evidence id: {duplicate}")
    evidence_id_set = set(evidence_ids)

    contact_ids: list[str] = []
    contact_by_id: dict[str, dict[str, Any]] = {}
    for contact in contacts:
        cid = text(contact.get("id"))
        contact_ids.append(cid)
        contact_by_id[cid] = contact
        if not cid:
            errors.append("contact.id is required")
        for key in ("contact_label", "relationship", "consent_status", "consent_evidence_ref"):
            if not text(contact.get(key)):
                errors.append(f"{cid}.{key} is required")
        consent = text(contact.get("consent_status"))
        if consent not in CONSENT_STATUSES:
            errors.append(f"{cid}.consent_status is unsupported: {consent}")
        ref = text(contact.get("consent_evidence_ref"))
        if ref not in evidence_id_set:
            errors.append(f"{cid}.consent_evidence_ref is unresolved: {ref}")
        allowed = contact.get("allowed_actions", [])
        if not isinstance(allowed, list):
            errors.append(f"{cid}.allowed_actions must be a list")
            allowed = []
        for action in allowed:
            if text(action) not in ACTION_TYPES:
                errors.append(f"{cid}.allowed_actions contains unsupported action: {action}")
            if text(action) in CONSENT_REQUIRED_ACTIONS and consent != "explicit_granted":
                errors.append(f"{cid}: action {action} requires explicit_granted consent")
        last_contact = contact.get("last_contact_date")
        last_date = None
        if last_contact:
            last_date = require_iso(last_contact, f"{cid}.last_contact_date", errors)
        if as_of and last_date and (as_of - last_date).days > FOLLOWUP_DAYS:
            has_followup = any(
                text(action.get("contact_id")) == cid and text(action.get("action_type")) == "follow_up"
                for action in actions
            )
            if not has_followup:
                errors.append(f"{cid}: follow-up is stale and no follow_up action exists")
    for duplicate in duplicate_values([cid for cid in contact_ids if cid]):
        errors.append(f"duplicate contact id: {duplicate}")
    contact_id_set = set(contact_ids)

    action_ids: list[str] = []
    for action in actions:
        aid = text(action.get("id"))
        action_ids.append(aid)
        if not aid:
            errors.append("action.id is required")
        action_type = text(action.get("action_type"))
        if action_type not in ACTION_TYPES:
            errors.append(f"{aid}.action_type is unsupported: {action_type}")
        cid = text(action.get("contact_id"))
        if cid not in contact_id_set:
            errors.append(f"{aid}.contact_id is unresolved: {cid}")
        ref = text(action.get("evidence_ref"))
        if ref not in evidence_id_set:
            errors.append(f"{aid}.evidence_ref is unresolved: {ref}")
        due_date = action.get("due_date")
        if due_date:
            require_iso(due_date, f"{aid}.due_date", errors)
        status = text(action.get("status"))
        if status not in {"planned", "blocked", "done"}:
            errors.append(f"{aid}.status is unsupported: {status}")
        contact = contact_by_id.get(cid, {})
        consent = text(contact.get("consent_status"))
        allowed = set(contact.get("allowed_actions", [])) if isinstance(contact.get("allowed_actions"), list) else set()
        if action_type in CONSENT_REQUIRED_ACTIONS and consent != "explicit_granted":
            errors.append(f"{aid}: {action_type} requires explicit_granted consent")
        if action_type not in allowed and action_type not in {"request_consent", "follow_up", "send_thanks", "no_contact"}:
            errors.append(f"{aid}: {action_type} is outside allowed_actions for {cid}")
    for duplicate in duplicate_values([aid for aid in action_ids if aid]):
        errors.append(f"duplicate action id: {duplicate}")

    for edge in edges:
        label = text(edge.get("id")) or "edge"
        for endpoint in ("from_contact_id", "to_contact_id"):
            if text(edge.get(endpoint)) not in contact_id_set:
                errors.append(f"{label}.{endpoint} is unresolved")
        ref = text(edge.get("evidence_ref"))
        if ref not in evidence_id_set:
            errors.append(f"{label}.evidence_ref is unresolved: {ref}")
        if not text(edge.get("relationship")):
            errors.append(f"{label}.relationship is required")

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

    if errors and isinstance(packet, dict) and text(packet.get("status")) == "active":
        errors.append("packet.status must not be active when validation errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate red-y-referencias JSON packet")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    try:
        data = load_json(Path(args.input))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"reference_packet={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
