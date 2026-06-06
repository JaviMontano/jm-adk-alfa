#!/usr/bin/env python3
"""Validate deterministic knowledge-management report fixtures."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


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


def has_evidence_tag(value: object, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence_tag(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence_tag(item, allowed) for item in value.values())
    return False


def is_network_path(path: str) -> bool:
    parsed = urlparse(path)
    return parsed.scheme in {"http", "https"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a knowledge-management report JSON file")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    evidence_policy = load_json(ASSETS / "evidence-policy.json")
    taxonomy = load_json(ASSETS / "knowledge-taxonomy.json")
    search_policy = load_json(ASSETS / "searchability-policy.json")
    freshness_policy = load_json(ASSETS / "freshness-policy.json")
    contract = load_json(ASSETS / "report-contract.json")

    allowed_tags = set(evidence_policy["allowed_tags"])
    item_types = set(taxonomy["item_types"])
    statuses = set(taxonomy["statuses"])
    windows = freshness_policy["windows_days"]
    min_terms = int(search_policy["minimum_retrieval_terms_per_item"])
    forbidden_terms = {term.lower() for term in search_policy["forbidden_terms"]}

    report = load_json(args.report)
    errors: list[str] = []
    if not isinstance(report, dict):
        errors.append("report root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in report:
                errors.append(f"missing top-level field: {field}")
        if report.get("skill") != "knowledge-management":
            errors.append("skill must be knowledge-management")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    reference_date = iso_date(str(report["reference_date"]), "reference_date", errors)
    if not has_evidence_tag(report.get("summary"), allowed_tags):
        errors.append("summary must include an allowed evidence tag")

    register = report.get("register")
    if not isinstance(register, list) or not register:
        errors.append("register must be a non-empty list")
        register = []

    action_source_ids: set[str] = set()
    actions = report.get("actions")
    if not isinstance(actions, list):
        errors.append("actions must be a list")
        actions = []
    for action in actions:
        if not isinstance(action, dict):
            errors.append("each action must be an object")
            continue
        for field in contract["required_action_fields"]:
            if not action.get(field):
                errors.append(f"action missing {field}")
        due_date = iso_date(str(action.get("due_date", "")), "action.due_date", errors)
        if reference_date and due_date and due_date < reference_date:
            errors.append(f"action {action.get('id')} due_date is before reference_date")
        if action.get("evidence_tag") not in allowed_tags:
            errors.append(f"action {action.get('id')} has invalid evidence_tag")
        for source_id in action.get("source_ids", []):
            action_source_ids.add(str(source_id))

    for item in register:
        if not isinstance(item, dict):
            errors.append("each register item must be an object")
            continue
        item_id = str(item.get("id", ""))
        for field in contract["required_register_fields"]:
            if field not in item or item[field] in ("", [], None):
                errors.append(f"register item {item_id or '<missing-id>'} missing {field}")
        if item.get("type") not in item_types:
            errors.append(f"register item {item_id} has invalid type")
        status = item.get("status")
        if status not in statuses:
            errors.append(f"register item {item_id} has invalid status")
        if item.get("evidence_tag") not in allowed_tags:
            errors.append(f"register item {item_id} has invalid evidence_tag")
        source_path = str(item.get("source_path", ""))
        if is_network_path(source_path):
            errors.append(f"register item {item_id} uses network source_path")
        terms = item.get("retrieval_terms")
        if not isinstance(terms, list) or len([term for term in terms if str(term).strip()]) < min_terms:
            errors.append(f"register item {item_id} needs at least {min_terms} retrieval terms")
        else:
            normalized_terms = {str(term).strip().lower() for term in terms}
            if normalized_terms & forbidden_terms:
                errors.append(f"register item {item_id} uses forbidden retrieval term")
        last_reviewed = iso_date(str(item.get("last_reviewed", "")), f"register item {item_id}.last_reviewed", errors)
        if reference_date and last_reviewed and last_reviewed > reference_date:
            errors.append(f"register item {item_id} last_reviewed is after reference_date")
        if reference_date and last_reviewed and item.get("type") in windows:
            age = (reference_date - last_reviewed).days
            window = int(windows[item["type"]])
            if age > window and status != "stale":
                errors.append(f"register item {item_id} exceeds freshness window but is not stale")
        if status in {"stale", "duplicate", "contradiction", "gap", "deprecated"} and item_id not in action_source_ids:
            errors.append(f"register item {item_id} status {status} needs an owner-bound action")

    for section in ["searchability_map", "decay_review", "gaps", "validation", "risks"]:
        value = report.get(section)
        if value in ({}, [], "", None):
            errors.append(f"{section} must not be empty")
        if not has_evidence_tag(value, allowed_tags):
            errors.append(f"{section} must include an allowed evidence tag")

    moving_terms = re.compile(r"\b(today|tomorrow|yesterday|recently|soon)\b", re.IGNORECASE)
    serialized = json.dumps(report, ensure_ascii=False)
    if moving_terms.search(serialized):
        errors.append("report must avoid moving time words; use explicit dates")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.report.name}: register={len(register)} actions={len(actions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
