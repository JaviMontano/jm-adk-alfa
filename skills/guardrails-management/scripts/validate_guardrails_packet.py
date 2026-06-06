#!/usr/bin/env python3
"""Validate deterministic guardrails-management operation packets."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def iso_date(value: str, field: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must be ISO date: {value}")
        return None


def normalize_rule(rule: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", rule.lower())).strip()


def has_evidence(value: object, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item, allowed) for item in value.values())
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a guardrails-management operation packet")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()

    schema = load_json(ASSETS / "rule-schema.json")
    storage_map = load_json(ASSETS / "storage-map.json")
    contract = load_json(ASSETS / "report-contract.json")
    allowed_tags = set(schema["allowed_evidence_tags"])
    allowed_types = set(schema["allowed_types"])
    allowed_sources = set(schema["allowed_sources"])
    operations = set(contract["operations"])
    storage_actions = set(contract["storage_actions"])

    packet = load_json(args.packet)
    errors: list[str] = []
    if not isinstance(packet, dict):
        errors.append("packet root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in packet:
                errors.append(f"missing top-level field: {field}")
        if packet.get("skill") != "guardrails-management":
            errors.append("skill must be guardrails-management")
        if packet.get("operation") not in operations:
            errors.append("invalid operation")
        if packet.get("storage_action") not in storage_actions:
            errors.append("invalid storage_action")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    reference_date = iso_date(str(packet["reference_date"]), "reference_date", errors)
    confirmation = packet.get("confirmation")
    if not isinstance(confirmation, dict):
        errors.append("confirmation must be an object")
        confirmation = {}
    confirmed = confirmation.get("status") == "confirmed"
    if confirmed and confirmation.get("confirmed_by") != "user":
        errors.append("confirmed packets require confirmed_by=user")
    if confirmed:
        confirmed_date = iso_date(str(confirmation.get("confirmed_date", "")), "confirmation.confirmed_date", errors)
        if reference_date and confirmed_date and confirmed_date != reference_date:
            errors.append("confirmation.confirmed_date must equal reference_date")

    rule = packet.get("rule_entry")
    if not isinstance(rule, dict):
        errors.append("rule_entry must be an object")
        rule = {}
    for field in schema["required_fields"]:
        if field not in rule or rule[field] in ("", [], None):
            errors.append(f"rule_entry missing {field}")

    rule_type = rule.get("type")
    if rule_type not in allowed_types:
        errors.append("rule_entry has invalid type")
    if rule.get("source") not in allowed_sources:
        errors.append("rule_entry has invalid source")
    if rule.get("evidence_tag") not in allowed_tags:
        errors.append("rule_entry has invalid evidence_tag")
    if not isinstance(rule.get("active"), bool):
        errors.append("rule_entry.active must be boolean")
    storage = storage_map["types"].get(rule_type, {}) if isinstance(rule_type, str) else {}
    expected_prefix = storage.get("id_prefix")
    expected_file = storage.get("target_file")
    rule_id = str(rule.get("id", ""))
    if expected_prefix and not re.fullmatch(rf"{expected_prefix}-\d{{3}}", rule_id):
        errors.append(f"rule_entry id must match {expected_prefix}-NNN")
    if expected_file and rule.get("target_file") != expected_file:
        errors.append("rule_entry target_file does not match type")
    confirmed_date_value = str(rule.get("confirmed_date", ""))
    rule_confirmed_date = iso_date(confirmed_date_value, "rule_entry.confirmed_date", errors)
    if reference_date and rule_confirmed_date and rule_confirmed_date != reference_date:
        errors.append("rule_entry.confirmed_date must equal reference_date")
    if len(str(rule.get("verifiable_check", "")).strip()) < 20:
        errors.append("rule_entry.verifiable_check must be specific")

    operation = packet.get("operation")
    storage_action = packet.get("storage_action")
    if storage_action in {"append-one", "deactivate-one"} and not confirmed:
        errors.append("persistence requires confirmed confirmation")
    if operation == "store" and storage_action != "append-one":
        errors.append("store operation requires append-one storage_action")
    if operation == "propose" and storage_action != "proposal-only":
        errors.append("propose operation must be proposal-only")
    if operation == "deactivate":
        if storage_action != "deactivate-one":
            errors.append("deactivate operation requires deactivate-one storage_action")
        if rule.get("active") is not False:
            errors.append("deactivate operation must set active=false")

    conflict_review = packet.get("conflict_review")
    if not isinstance(conflict_review, dict):
        errors.append("conflict_review must be an object")
        conflict_review = {}
    if conflict_review.get("duplicate_active") is True and storage_action != "blocked":
        errors.append("duplicate active rule must block storage")
    if conflict_review.get("conflict") is True and storage_action != "blocked":
        errors.append("conflicting rule must block storage")
    existing_rules = conflict_review.get("existing_rules", [])
    active_rules = [
        item for item in existing_rules
        if isinstance(item, dict) and item.get("active") is True
    ]
    normalized = normalize_rule(str(rule.get("rule", "")))
    for existing in active_rules:
        if normalize_rule(str(existing.get("rule", ""))) == normalized and existing.get("id") != rule_id:
            errors.append("normalized active duplicate found")

    for section in ["source_utterance", "conflict_review", "validation", "risks"]:
        if not has_evidence(packet.get(section), allowed_tags):
            errors.append(f"{section} must include an allowed evidence tag")

    moving_terms = re.compile(r"\b(today|tomorrow|yesterday|soon|recently)\b", re.IGNORECASE)
    if moving_terms.search(json.dumps(packet, ensure_ascii=False)):
        errors.append("packet must avoid moving time words; use explicit dates")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.packet.name}: operation={operation} action={storage_action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
