#!/usr/bin/env python3
"""Validate deterministic provenance preservation reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def policy(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("provenance-preservation-contract.json")
    claim_policy = policy("claim-source-policy.json")
    conflict_policy = policy("conflict-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["json_contract"]["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["json_contract"]["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != "katas-provenance-preservation":
        errors.append("skill must be katas-provenance-preservation")
    for field in ["report_id", "scenario"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")

    evidence = report.get("evidence")
    accepted_evidence = set(evidence_policy["accepted_evidence_types"])
    if not isinstance(evidence, list) or len(evidence) < evidence_policy["minimum_evidence_items"]:
        errors.append(f"evidence must contain at least {evidence_policy['minimum_evidence_items']} items")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            if item.get("type") not in accepted_evidence:
                errors.append(f"evidence[{index}].type must be accepted")
            if not non_empty_string(item.get("detail")):
                errors.append(f"evidence[{index}].detail must be non-empty")

    source_registry = report.get("source_registry")
    if not isinstance(source_registry, list) or not source_registry:
        errors.append("source_registry must be a non-empty list")
        source_registry = []
    source_ids: set[str] = set()
    for index, source in enumerate(source_registry):
        if not isinstance(source, dict):
            errors.append(f"source_registry[{index}] must be an object")
            continue
        for field in claim_policy["required_source_fields"]:
            if field not in source:
                errors.append(f"source_registry[{index}] missing field {field}")
        source_id = source.get("source_id")
        if not non_empty_string(source_id):
            errors.append(f"source_registry[{index}].source_id must be non-empty")
        else:
            if source_id in source_ids:
                errors.append(f"duplicate source_id: {source_id}")
            source_ids.add(source_id)
        if not non_empty_string(source.get("source_name")):
            errors.append(f"source_registry[{index}].source_name must be non-empty")
        publication_date = source.get("publication_date")
        if not non_empty_string(publication_date) or not DATE_RE.match(publication_date):
            errors.append(f"source_registry[{index}].publication_date must be YYYY-MM-DD")

    claims = report.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{index}] must be an object")
            continue
        for field in claim_policy["required_claim_fields"]:
            if field not in claim:
                errors.append(f"claim {index} missing field {field}")
        if not non_empty_string(claim.get("claim_id")):
            errors.append(f"claim {index}.claim_id must be non-empty")
        if not non_empty_string(claim.get("claim")):
            errors.append(f"claim {index}.claim must be non-empty")
        sources = claim.get("sources")
        if not isinstance(sources, list) or len(sources) < claim_policy["sources_min_length"]:
            errors.append(f"claim {index}.sources must be a non-empty list")
            sources = []
        seen_values = set()
        for source_index, source_ref in enumerate(sources):
            if not isinstance(source_ref, dict):
                errors.append(f"claim {index}.sources[{source_index}] must be an object")
                continue
            source_id = source_ref.get("source_id")
            if not non_empty_string(source_id):
                errors.append(f"claim {index}.sources[{source_index}].source_id must be non-empty")
            elif source_id not in source_ids:
                errors.append(f"claim {index}.sources[{source_index}].source_id must exist in registry")
            if "value" in source_ref:
                seen_values.add(json.dumps(source_ref.get("value"), sort_keys=True))
        conflict = claim.get("conflict")
        if not isinstance(conflict, bool):
            errors.append(f"claim {index}.conflict must be boolean")
        if conflict is True:
            if conflict_policy["conflict_requires_multiple_source_values"] and len(seen_values) < 2:
                errors.append(f"claim {index} conflict requires at least two source values")
            if claim.get("needs_human_review") is not True:
                errors.append(f"claim {index} conflict requires needs_human_review true")
            if claim.get("escalation_route") not in conflict_policy["allowed_escalation_routes"]:
                errors.append(f"claim {index} conflict requires allowed escalation_route")
            if claim.get("resolution_method") in conflict_policy["forbidden_resolution_methods"]:
                errors.append(f"claim {index} conflict uses forbidden resolution_method")
            if "resolved_value" in claim:
                errors.append(f"claim {index} conflict must not set resolved_value")
        if conflict is False:
            if claim.get("needs_human_review") is True:
                errors.append(f"claim {index} non-conflict must not require human review")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("claims_without_sources") != 0:
            errors.append("validation.claims_without_sources must be 0")
        if validation.get("unknown_source_refs") != 0:
            errors.append("validation.unknown_source_refs must be 0")
        if validation.get("conflicts_silenced") != 0:
            errors.append("validation.conflicts_silenced must be 0")
        if validation.get("free_prose_only") is not False:
            errors.append("validation.free_prose_only must be false")
        if validation.get("structural_test_passed") is not True:
            errors.append("validation.structural_test_passed must be true")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        decisions = set(contract["json_contract"]["guardian_decisions"])
        if guardian.get("decision") not in decisions:
            errors.append(f"guardian.decision must be one of {sorted(decisions)}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a provenance preservation JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON report")
    args = parser.parse_args()

    try:
        report = load_json(args.report)
        errors = validate(report)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
