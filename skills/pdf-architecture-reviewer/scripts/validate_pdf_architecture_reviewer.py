#!/usr/bin/env python3
"""Validate deterministic PDF architecture reviewer reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "pdf-architecture-reviewer"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("pdf-architecture-reviewer-contract.json")["json_contract"]
    document_policy = asset("document-read-policy.json")
    page_policy = asset("page-evidence-policy.json")
    mapping_policy = asset("repo-mapping-policy.json")
    source_policy = asset("official-source-requirement-policy.json")
    decision_policy = asset("decision-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("report_id")):
        errors.append("report_id must be a non-empty string")

    document = report.get("document")
    reviewed_pages: set[int] = set()
    if not isinstance(document, dict):
        errors.append("document must be an object")
        document = {}
    for field in document_policy["required_document_fields"]:
        if field not in document:
            errors.append(f"document missing field {field}")
    if not non_empty_string(document.get("document_id")):
        errors.append("document.document_id must be non-empty")
    if not non_empty_string(document.get("file_name")):
        errors.append("document.file_name must be non-empty")
    if not re.match(document_policy["sha256_pattern"], str(document.get("sha256", ""))):
        errors.append("document.sha256 must be a lowercase sha256 hex digest")
    if document.get("extraction_status") != document_policy["read_status"]:
        errors.append("document.extraction_status must be read")
    if document.get("extraction_method") not in document_policy["allowed_extraction_methods"]:
        errors.append("document.extraction_method is not allowed")
    page_count = document.get("page_count")
    if not isinstance(page_count, int) or page_count < 1:
        errors.append("document.page_count must be a positive integer")
        page_count = 0
    pages_reviewed = document.get("pages_reviewed")
    if not isinstance(pages_reviewed, list) or not pages_reviewed:
        errors.append("document.pages_reviewed must be a non-empty list")
        pages_reviewed = []
    for page in pages_reviewed:
        if not isinstance(page, int) or page < 1 or page > page_count:
            errors.append(f"document.pages_reviewed contains invalid page: {page}")
        else:
            reviewed_pages.add(page)
    if len(reviewed_pages) != len(pages_reviewed):
        errors.append("document.pages_reviewed must not contain duplicates")

    page_evidence = report.get("page_evidence")
    if not isinstance(page_evidence, list) or not page_evidence:
        errors.append("page_evidence must be a non-empty list")
        page_evidence = []
    evidence_ids: set[str] = set()
    evidence_claim_refs: set[str] = set()
    for index, evidence in enumerate(page_evidence):
        if not isinstance(evidence, dict):
            errors.append(f"page_evidence[{index}] must be an object")
            continue
        for field in page_policy["required_page_evidence_fields"]:
            if field not in evidence:
                errors.append(f"page_evidence[{index}] missing field {field}")
        evidence_id = evidence.get("evidence_id")
        if not non_empty_string(evidence_id):
            errors.append(f"page_evidence[{index}].evidence_id must be non-empty")
        elif evidence_id in evidence_ids:
            errors.append(f"duplicate evidence_id: {evidence_id}")
        else:
            evidence_ids.add(str(evidence_id))
        page = evidence.get("page")
        if not isinstance(page, int):
            errors.append(f"page_evidence[{index}].page must be an integer")
        elif page_policy["allow_unreviewed_pages"] is False and page not in reviewed_pages:
            errors.append(f"page_evidence[{index}].page must be reviewed")
        excerpt = evidence.get("excerpt")
        if not non_empty_string(excerpt) or len(str(excerpt).strip()) < page_policy["minimum_excerpt_length"]:
            errors.append(f"page_evidence[{index}].excerpt is too short")
        if evidence.get("extraction_method") not in document_policy["allowed_extraction_methods"]:
            errors.append(f"page_evidence[{index}].extraction_method is not allowed")
        claim_ids = evidence.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids:
            errors.append(f"page_evidence[{index}].claim_ids must be a non-empty list")
        else:
            evidence_claim_refs.update(str(claim_id) for claim_id in claim_ids if non_empty_string(claim_id))

    mappings = report.get("repo_mapping")
    if not isinstance(mappings, list) or not mappings:
        errors.append("repo_mapping must be a non-empty list")
        mappings = []
    mapping_claim_refs: dict[str, list[dict[str, Any]]] = {}
    for index, mapping in enumerate(mappings):
        if not isinstance(mapping, dict):
            errors.append(f"repo_mapping[{index}] must be an object")
            continue
        for field in mapping_policy["required_mapping_fields"]:
            if field not in mapping:
                errors.append(f"repo_mapping[{index}] missing field {field}")
        claim_id = mapping.get("claim_id")
        if not non_empty_string(claim_id):
            errors.append(f"repo_mapping[{index}].claim_id must be non-empty")
            claim_id = ""
        if not non_empty_string(mapping.get("path")):
            errors.append(f"repo_mapping[{index}].path must be non-empty")
        if mapping.get("mapping_status") not in mapping_policy["mapping_statuses"]:
            errors.append(f"repo_mapping[{index}].mapping_status is not allowed")
        if not non_empty_string(mapping.get("observed_state")):
            errors.append(f"repo_mapping[{index}].observed_state must be non-empty")
        if claim_id:
            mapping_claim_refs.setdefault(str(claim_id), []).append(mapping)

    requirements = report.get("official_source_requirements")
    if not isinstance(requirements, list):
        errors.append("official_source_requirements must be a list")
        requirements = []
    requirement_claim_refs: dict[str, list[dict[str, Any]]] = {}
    for index, requirement in enumerate(requirements):
        if not isinstance(requirement, dict):
            errors.append(f"official_source_requirements[{index}] must be an object")
            continue
        for field in source_policy["required_requirement_fields"]:
            if field not in requirement:
                errors.append(f"official_source_requirements[{index}] missing field {field}")
        claim_id = requirement.get("claim_id")
        if not non_empty_string(claim_id):
            errors.append(f"official_source_requirements[{index}].claim_id must be non-empty")
            claim_id = ""
        if requirement.get("source_kind") not in source_policy["source_kinds"]:
            errors.append(f"official_source_requirements[{index}].source_kind is not allowed")
        if requirement.get("status") not in source_policy["requirement_statuses"]:
            errors.append(f"official_source_requirements[{index}].status is not allowed")
        if not non_empty_string(requirement.get("requirement_reason")):
            errors.append(f"official_source_requirements[{index}].requirement_reason must be non-empty")
        official_source_ids = requirement.get("official_source_ids")
        if not isinstance(official_source_ids, list):
            errors.append(f"official_source_requirements[{index}].official_source_ids must be a list")
            official_source_ids = []
        if requirement.get("status") == "satisfied" and not official_source_ids:
            errors.append(f"official_source_requirements[{index}] satisfied requires official_source_ids")
        if claim_id:
            requirement_claim_refs.setdefault(str(claim_id), []).append(requirement)

    claims = report.get("architecture_claims")
    if not isinstance(claims, list) or not claims:
        errors.append("architecture_claims must be a non-empty list")
        claims = []
    claim_ids: set[str] = set()
    blocking_needed = False
    contradiction_needed: set[str] = set()
    source_requirement_needed: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"architecture_claims[{index}] must be an object")
            continue
        claim_id = claim.get("claim_id")
        if not non_empty_string(claim_id):
            errors.append(f"architecture_claims[{index}].claim_id must be non-empty")
            claim_id = ""
        elif claim_id in claim_ids:
            errors.append(f"duplicate claim_id: {claim_id}")
        else:
            claim_ids.add(str(claim_id))
        if not non_empty_string(claim.get("claim")):
            errors.append(f"architecture_claims[{index}].claim must be non-empty")
        status = claim.get("status")
        if status not in ["supported", "contradicted", "unverified", "repo_missing"]:
            errors.append(f"architecture_claims[{index}].status is not allowed")
        if status in decision_policy["blocking_claim_statuses"]:
            blocking_needed = True
        if status == "contradicted" and claim_id:
            contradiction_needed.add(str(claim_id))
        page_evidence_ids = claim.get("page_evidence_ids")
        if not isinstance(page_evidence_ids, list) or not page_evidence_ids:
            errors.append(f"architecture_claims[{index}].page_evidence_ids must be a non-empty list")
            page_evidence_ids = []
        if not set(page_evidence_ids).issubset(evidence_ids):
            errors.append(f"architecture_claims[{index}].page_evidence_ids must exist in page_evidence")
        if claim_id and str(claim_id) not in mapping_claim_refs:
            errors.append(f"claim {claim_id} requires repo_mapping")
        if claim.get("official_source_required") is True and claim_id:
            source_requirement_needed.add(str(claim_id))
        elif claim.get("official_source_required") is not False:
            errors.append(f"architecture_claims[{index}].official_source_required must be boolean")
        if not non_empty_string(claim.get("decision_impact")):
            errors.append(f"architecture_claims[{index}].decision_impact must be non-empty")

    if not evidence_claim_refs.issubset(claim_ids):
        errors.append("page_evidence.claim_ids must reference architecture_claims")
    for claim_id in source_requirement_needed:
        if claim_id not in requirement_claim_refs:
            errors.append(f"claim {claim_id} requires official_source_requirements")

    contradictions = report.get("contradictions")
    if not isinstance(contradictions, list):
        errors.append("contradictions must be a list")
        contradictions = []
    contradiction_claim_refs: set[str] = set()
    for index, contradiction in enumerate(contradictions):
        if not isinstance(contradiction, dict):
            errors.append(f"contradictions[{index}] must be an object")
            continue
        for field in ["contradiction_id", "claim_id", "page_evidence_id", "repo_ref", "severity", "resolution_status"]:
            if field not in contradiction:
                errors.append(f"contradictions[{index}] missing field {field}")
        claim_id = contradiction.get("claim_id")
        if non_empty_string(claim_id):
            contradiction_claim_refs.add(str(claim_id))
        if claim_id not in claim_ids:
            errors.append(f"contradictions[{index}].claim_id must reference a claim")
        if contradiction.get("page_evidence_id") not in evidence_ids:
            errors.append(f"contradictions[{index}].page_evidence_id must reference page_evidence")
        if not non_empty_string(contradiction.get("repo_ref")):
            errors.append(f"contradictions[{index}].repo_ref must be non-empty")
        if contradiction.get("severity") not in ["low", "medium", "high"]:
            errors.append(f"contradictions[{index}].severity is not allowed")
        if contradiction.get("resolution_status") not in ["open", "resolved", "deferred"]:
            errors.append(f"contradictions[{index}].resolution_status is not allowed")
        if contradiction.get("resolution_status") == "open":
            blocking_needed = True
    missing_contradictions = contradiction_needed - contradiction_claim_refs
    if missing_contradictions:
        errors.append(f"contradicted claims missing contradictions: {sorted(missing_contradictions)}")

    unsatisfied_requirements = {
        claim_id
        for claim_id in source_requirement_needed
        if any(req.get("status") != "satisfied" for req in requirement_claim_refs.get(claim_id, []))
    }
    if unsatisfied_requirements:
        blocking_needed = True

    decisions = report.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append("decisions must be a non-empty list")
        decisions = []
    has_authorize = False
    has_blocking_decision = False
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            errors.append(f"decisions[{index}] must be an object")
            continue
        for field in decision_policy["required_decision_fields"]:
            if field not in decision:
                errors.append(f"decisions[{index}] missing field {field}")
        action = decision.get("action")
        if action not in decision_policy["actions"]:
            errors.append(f"decisions[{index}].action is not allowed")
        if action == "authorize":
            has_authorize = True
        if action in ["block", "defer", "needs_official_source"]:
            has_blocking_decision = True
        claim_refs = decision.get("claim_ids")
        if not isinstance(claim_refs, list) or not claim_refs:
            errors.append(f"decisions[{index}].claim_ids must be a non-empty list")
            claim_refs = []
        if not set(claim_refs).issubset(claim_ids):
            errors.append(f"decisions[{index}].claim_ids must reference claims")
        blocking_gaps = decision.get("blocking_gaps")
        if not isinstance(blocking_gaps, list):
            errors.append(f"decisions[{index}].blocking_gaps must be a list")
            blocking_gaps = []
        if action == "authorize" and blocking_gaps:
            errors.append(f"decisions[{index}] authorize requires no blocking_gaps")
        if action == "authorize" and blocking_needed:
            errors.append(f"decisions[{index}] authorize is forbidden while blocking gaps exist")
        if action != "authorize" and blocking_needed and not blocking_gaps:
            errors.append(f"decisions[{index}] blocking action requires blocking_gaps")
        if not non_empty_string(decision.get("rationale")):
            errors.append(f"decisions[{index}].rationale must be non-empty")
    if blocking_needed and has_authorize:
        errors.append("authorization is forbidden while unresolved gaps exist")
    if blocking_needed and not has_blocking_decision:
        errors.append("blocking gaps require a block, defer, or needs_official_source decision")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    expected_flags = {
        "pdf_read_before_evidence": True,
        "page_evidence_present": True,
        "claims_trace_to_pages": True,
        "repo_mapping_traceable": True,
        "official_sources_identified": bool(source_requirement_needed),
        "contradictions_recorded": not missing_contradictions,
        "deterministic_script_passed": True,
    }
    for field, expected in expected_flags.items():
        if validation.get(field) is not expected:
            errors.append(f"validation.{field} must be {expected}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
        guardian = {}
    decision = guardian.get("decision")
    if decision not in contract["guardian_decisions"]:
        errors.append(f"guardian.decision must be one of {contract['guardian_decisions']}")
    if not non_empty_string(guardian.get("reason")):
        errors.append("guardian.reason must be non-empty")
    if decision == "pass" and blocking_needed:
        errors.append("guardian pass requires no blocking gaps")
    if decision == "pass" and not has_authorize:
        errors.append("guardian pass requires an authorize decision")
    if decision == "block" and not blocking_needed:
        errors.append("guardian block requires a blocking gap")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PDF architecture reviewer JSON report")
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
