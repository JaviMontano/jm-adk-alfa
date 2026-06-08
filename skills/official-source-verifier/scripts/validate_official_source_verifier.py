#!/usr/bin/env python3
"""Validate deterministic official-source verification reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "official-source-verifier"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


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

    contract = policy("official-source-verifier-contract.json")["json_contract"]
    source_policy = policy("source-priority-policy.json")
    claim_policy = policy("claim-evidence-policy.json")
    citation_policy = policy("citation-policy.json")
    decision_policy = policy("decision-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    for field in ["report_id", "question"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")

    official_types = set(source_policy["official_source_types"])
    non_authority_types = set(source_policy["non_authority_source_types"])
    source_registry = report.get("source_registry")
    if not isinstance(source_registry, list) or not source_registry:
        errors.append("source_registry must be a non-empty list")
        source_registry = []
    source_ids: set[str] = set()
    official_source_ids: set[str] = set()
    for index, source in enumerate(source_registry):
        if not isinstance(source, dict):
            errors.append(f"source_registry[{index}] must be an object")
            continue
        for field in source_policy["required_source_fields"]:
            if field not in source:
                errors.append(f"source_registry[{index}] missing field {field}")
        source_id = source.get("source_id")
        if not non_empty_string(source_id):
            errors.append(f"source_registry[{index}].source_id must be non-empty")
        elif source_id in source_ids:
            errors.append(f"duplicate source_id: {source_id}")
        else:
            source_ids.add(str(source_id))
        source_type = source.get("source_type")
        official = source.get("official")
        role = source.get("role")
        if source_type in official_types:
            if official is not True:
                errors.append(f"source {source_id} official must be true for official source types")
            official_source_ids.add(str(source_id))
            if role != "authority":
                errors.append(f"source {source_id} official source must use role authority")
        elif source_type in non_authority_types:
            if official is not False:
                errors.append(f"source {source_id} official must be false for secondary/community source types")
            if role not in source_policy["non_authority_roles"]:
                errors.append(f"source {source_id} secondary/community source must not be authority")
        else:
            errors.append(f"source {source_id} has unknown source_type")
        if role == "authority" and source_type not in official_types:
            errors.append(f"source {source_id} cannot be authority unless official")
        if not non_empty_string(source.get("publisher")) or len(str(source.get("publisher", "")).strip()) < citation_policy["minimum_publisher_length"]:
            errors.append(f"source {source_id}.publisher is too short")
        if not non_empty_string(source.get("title")) or len(str(source.get("title", "")).strip()) < citation_policy["minimum_title_length"]:
            errors.append(f"source {source_id}.title is too short")
        if not non_empty_string(source.get("url")) or not re.match(citation_policy["url_pattern"], str(source.get("url"))):
            errors.append(f"source {source_id}.url must be http(s)")
        if not non_empty_string(source.get("accessed_date")) or not re.match(citation_policy["accessed_date_pattern"], str(source.get("accessed_date"))):
            errors.append(f"source {source_id}.accessed_date must be YYYY-MM-DD")

    claims = report.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []
    verified_claim_ids: set[str] = set()
    blocking_needed = False
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{index}] must be an object")
            continue
        for field in claim_policy["required_claim_fields"]:
            if field not in claim:
                errors.append(f"claim {index} missing field {field}")
        claim_id = claim.get("claim_id")
        if not non_empty_string(claim_id):
            errors.append(f"claim {index}.claim_id must be non-empty")
        if not non_empty_string(claim.get("claim")):
            errors.append(f"claim {index}.claim must be non-empty")
        status = claim.get("status")
        if status not in claim_policy["claim_statuses"]:
            errors.append(f"claim {index}.status must be one of {claim_policy['claim_statuses']}")
        source_refs = set(claim.get("source_ids", [])) if isinstance(claim.get("source_ids"), list) else set()
        official_refs = set(claim.get("official_source_ids", [])) if isinstance(claim.get("official_source_ids"), list) else set()
        secondary_refs = set(claim.get("secondary_source_ids", [])) if isinstance(claim.get("secondary_source_ids"), list) else set()
        if not source_refs:
            errors.append(f"claim {index}.source_ids must be non-empty")
        if not source_refs.issubset(source_ids):
            errors.append(f"claim {index}.source_ids must exist in source_registry")
        if not official_refs.issubset(official_source_ids):
            errors.append(f"claim {index}.official_source_ids must reference official authority sources")
        if not secondary_refs.issubset(source_ids - official_source_ids):
            errors.append(f"claim {index}.secondary_source_ids must reference non-official sources")
        if official_refs & secondary_refs:
            errors.append(f"claim {index} official and secondary source ids must be disjoint")
        if status == "verified":
            if claim_policy["verified_requires_official_source"] and not official_refs:
                errors.append(f"claim {index} verified status requires official_source_ids")
            if non_empty_string(claim_id):
                verified_claim_ids.add(str(claim_id))
        if status in {"unverified", "conflict"}:
            blocking_needed = True
        if not non_empty_string(claim.get("decision_impact")):
            errors.append(f"claim {index}.decision_impact must be non-empty")

    decision = report.get("decision")
    if not isinstance(decision, dict):
        errors.append("decision must be an object")
        decision = {}
    else:
        if not isinstance(decision.get("change_authorized"), bool):
            errors.append("decision.change_authorized must be boolean")
        if not non_empty_string(decision.get("justified_change")):
            errors.append("decision.justified_change must be non-empty")
        if decision.get("scope") not in decision_policy["allowed_scopes"]:
            errors.append(f"decision.scope must be one of {decision_policy['allowed_scopes']}")
        blocking_gaps = decision.get("blocking_gaps")
        if not isinstance(blocking_gaps, list):
            errors.append("decision.blocking_gaps must be a list")
            blocking_gaps = []
        if blocking_needed and not blocking_gaps:
            errors.append("unverified or conflict claims require decision.blocking_gaps")
        if decision.get("change_authorized") is True:
            if blocking_gaps:
                errors.append("change_authorized true requires no blocking_gaps")
            if blocking_needed:
                errors.append("change_authorized true requires all claims verified")
            if not verified_claim_ids:
                errors.append("change_authorized true requires verified claims")
            if decision.get("scope") == "none":
                errors.append("change_authorized true requires non-none scope")
        else:
            if decision.get("scope") != "none" and blocking_needed:
                errors.append("blocked decisions with gaps should use scope none")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        expected_flags = {
            "official_sources_first": True,
            "secondary_sources_not_authority": True,
            "all_sources_have_accessed_date": True,
            "decision_traced_to_claim": True,
            "unverified_claims_block_change": True,
            "deterministic_script_passed": True,
        }
        for field, expected in expected_flags.items():
            if validation.get(field) is not expected:
                errors.append(f"validation.{field} must be {expected}")
        expected_all_claims = not blocking_needed
        if validation.get("all_claims_have_official_source") is not expected_all_claims:
            errors.append(f"validation.all_claims_have_official_source must be {expected_all_claims}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        if guardian.get("decision") not in contract["guardian_decisions"]:
            errors.append(f"guardian.decision must be one of {contract['guardian_decisions']}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")
        if guardian.get("decision") == "pass" and decision.get("change_authorized") is not True:
            errors.append("guardian pass requires an authorized change")
        if guardian.get("decision") == "pass" and blocking_needed:
            errors.append("guardian pass requires no unverified or conflict claims")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an official-source verification JSON report")
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
