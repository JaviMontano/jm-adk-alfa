#!/usr/bin/env python3
"""Validate deterministic generate-qa-report fixtures."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def has_evidence(value: Any, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item, allowed) for item in value.values())
    return False


def require_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if obj.get(field) in ("", [], None):
            errors.append(f"{label} missing {field}")


def validate_date(value: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"reference_date must be ISO date: {value}")


def validate_metadata(spec: dict[str, Any], severity_policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    metadata = spec.get("report_metadata")
    if not isinstance(metadata, dict):
        errors.append("report_metadata must be an object")
        return
    require_fields(metadata, ["plugin_name", "plugin_version", "plugin_path", "coverage_status", "evidence_tag"], "report_metadata", errors)
    if metadata.get("coverage_status") not in severity_policy["coverage_statuses"]:
        errors.append(f"coverage_status is invalid: {metadata.get('coverage_status')}")
    if metadata.get("evidence_tag") not in allowed:
        errors.append("report_metadata evidence_tag is invalid")


def validate_sources(spec: dict[str, Any], source_policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    sources = spec.get("source_runs")
    if not isinstance(sources, list) or not sources:
        errors.append("source_runs must be a non-empty list")
        return
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            errors.append("source run must be an object")
            continue
        require_fields(source, ["name", "status", "findings_count", "evidence_tag"], "source run", errors)
        seen.add(source.get("name"))
        if source.get("name") not in source_policy["required_sources"]:
            errors.append(f"unknown source run: {source.get('name')}")
        if source.get("status") not in ("pass", "warn", "fail", "not-run"):
            errors.append(f"source status is invalid: {source.get('status')}")
        if not isinstance(source.get("findings_count"), int):
            errors.append("source findings_count must be integer")
        if source.get("evidence_tag") not in allowed or not has_evidence(source, allowed):
            errors.append(f"source run missing valid evidence: {source.get('name')}")
    if spec.get("report_metadata", {}).get("coverage_status") == "complete":
        missing = set(source_policy["required_sources"]) - seen
        if missing:
            errors.append(f"complete coverage missing sources: {', '.join(sorted(missing))}")


def validate_findings_and_counts(spec: dict[str, Any], contract: dict[str, Any], severity_policy: dict[str, Any], source_policy: dict[str, Any], output_policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    findings = spec.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        return
    ids = set()
    counts = Counter()
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append("finding must be an object")
            continue
        require_fields(finding, contract["required_finding_fields"], "finding", errors)
        finding_id = str(finding.get("id", ""))
        ids.add(finding_id)
        if not re.match(output_policy["finding_id_pattern"], finding_id):
            errors.append(f"finding id is invalid: {finding_id}")
        severity = finding.get("severity")
        category = finding.get("category")
        if severity not in severity_policy["severities"]:
            errors.append(f"finding severity is invalid: {severity}")
        else:
            counts[severity] += 1
        if category not in source_policy["categories"]:
            errors.append(f"finding category is invalid: {category}")
        if finding.get("evidence_tag") not in allowed or not has_evidence(finding, allowed):
            errors.append(f"finding missing valid evidence: {finding_id}")

    stats = spec.get("summary_stats")
    if not isinstance(stats, dict):
        errors.append("summary_stats must be an object")
        return
    expected_total = len(findings)
    if stats.get("total_findings") != expected_total:
        errors.append("summary_stats total_findings does not match findings")
    for severity in severity_policy["severities"]:
        key = severity.lower()
        if stats.get(key) != counts[severity]:
            errors.append(f"summary_stats {key} count does not match findings")


def validate_tldr_categories_recommendations(spec: dict[str, Any], severity_policy: dict[str, Any], source_policy: dict[str, Any], output_policy: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    tldr = spec.get("tldr")
    if not isinstance(tldr, list) or len(tldr) != output_policy["tldr_lines"]:
        errors.append("tldr must contain exactly three lines")
    elif not has_evidence(tldr, allowed):
        errors.append("tldr must include evidence tags")

    categories = spec.get("category_status")
    if not isinstance(categories, list) or not categories:
        errors.append("category_status must be a non-empty list")
    else:
        for item in categories:
            if not isinstance(item, dict):
                errors.append("category_status item must be an object")
                continue
            require_fields(item, ["category", "status", "critical", "warning", "info", "evidence_tag"], "category_status", errors)
            if item.get("category") not in source_policy["categories"]:
                errors.append(f"category_status category is invalid: {item.get('category')}")
            if item.get("status") not in severity_policy["category_statuses"]:
                errors.append(f"category_status status is invalid: {item.get('status')}")
            if item.get("evidence_tag") not in allowed:
                errors.append("category_status evidence_tag is invalid")

    recommendations = spec.get("recommendations")
    if not isinstance(recommendations, list):
        errors.append("recommendations must be a list")
        return
    if not (output_policy["recommendation_min"] <= len(recommendations) <= output_policy["recommendation_max"]):
        errors.append("recommendations count is outside policy")
    finding_ids = {finding.get("id") for finding in spec.get("findings", []) if isinstance(finding, dict)}
    ranks = []
    for rec in recommendations:
        if not isinstance(rec, dict):
            errors.append("recommendation must be an object")
            continue
        require_fields(rec, ["rank", "finding_ids", "action", "rationale", "effort", "evidence_tag"], "recommendation", errors)
        ranks.append(rec.get("rank"))
        if rec.get("effort") not in severity_policy["effort_values"]:
            errors.append(f"recommendation effort is invalid: {rec.get('effort')}")
        if not isinstance(rec.get("finding_ids"), list) or not set(rec.get("finding_ids", [])).issubset(finding_ids):
            errors.append("recommendation finding_ids must reference included findings")
        if rec.get("evidence_tag") not in allowed or not has_evidence(rec, allowed):
            errors.append("recommendation missing valid evidence")
    if ranks != list(range(1, len(recommendations) + 1)):
        errors.append("recommendation ranks must be sequential")


def validate_validation_and_risks(spec: dict[str, Any], allowed: set[str], errors: list[str]) -> None:
    if not has_evidence(spec.get("validation"), allowed):
        errors.append("validation must include evidence tags")
    if not has_evidence(spec.get("risks"), allowed):
        errors.append("risks must include evidence tags")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generate-qa-report JSON fixture")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "report-contract.json")
    severity_policy = load_json(ASSETS / "severity-policy.json")
    source_policy = load_json(ASSETS / "source-policy.json")
    output_policy = load_json(ASSETS / "output-policy.json")
    allowed = set(contract["allowed_evidence_tags"])

    spec = load_json(args.report)
    errors: list[str] = []
    if not isinstance(spec, dict):
        errors.append("report root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in spec:
                errors.append(f"missing top-level field: {field}")
        if spec.get("skill") != "generate-qa-report":
            errors.append("skill must be generate-qa-report")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_date(str(spec["reference_date"]), errors)
    body = json.dumps(spec, ensure_ascii=False)
    for term in contract["moving_time_terms"]:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"report must avoid moving time term: {term}")

    validate_metadata(spec, severity_policy, allowed, errors)
    validate_sources(spec, source_policy, allowed, errors)
    validate_findings_and_counts(spec, contract, severity_policy, source_policy, output_policy, allowed, errors)
    validate_tldr_categories_recommendations(spec, severity_policy, source_policy, output_policy, allowed, errors)
    validate_validation_and_risks(spec, allowed, errors)

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(
        f"PASS {args.report.name}: findings={spec['summary_stats']['total_findings']} "
        f"coverage={spec['report_metadata']['coverage_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
