#!/usr/bin/env python3
"""Validate deterministic assumption-log JSON reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected list")
    return value


def find_blocked_phrase(value: Any, phrases: list[str], path: str = "$") -> str | None:
    if isinstance(value, str):
        lower = value.lower()
        for phrase in phrases:
            if phrase.lower() in lower:
                return f"{path}: blocked phrase: {phrase}"
    elif isinstance(value, dict):
        for key, item in value.items():
            found = find_blocked_phrase(item, phrases, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = find_blocked_phrase(item, phrases, f"{path}[{index}]")
            if found:
                return found
    return None


def validate_required_fields(item: dict[str, Any], fields: list[str], label: str) -> list[str]:
    errors: list[str] = []
    for field in fields:
        if field not in item:
            errors.append(f"{label}: missing field {field}")
        elif isinstance(item[field], str) and not item[field].strip():
            errors.append(f"{label}.{field}: must not be empty")
        elif isinstance(item[field], list) and not item[field]:
            errors.append(f"{label}.{field}: must not be empty")
    return errors


def validate_report(
    report: dict[str, Any],
    contract: dict[str, Any],
    status_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing section {section}")
    if errors:
        return errors

    blocked = find_blocked_phrase(report, list(contract.get("blocked_phrases", [])))
    if blocked:
        errors.append(blocked)

    summary = require_object(report["summary"], "summary")
    errors.extend(validate_required_fields(summary, contract["summary_fields"], "summary"))

    assumptions_raw = require_list(report["assumptions"], "assumptions")
    assumptions = [require_object(item, f"assumptions[{index}]") for index, item in enumerate(assumptions_raw)]
    if not assumptions:
        errors.append("assumptions: must contain at least one assumption")

    allowed_statuses = set(status_policy["statuses"])
    open_statuses = set(status_policy["open_statuses"])
    closed_statuses = set(status_policy["closed_statuses"])
    allowed_impacts = set(status_policy["impact_levels"])
    id_re = re.compile(status_policy["id_pattern"])
    allowed_tags = set(evidence_policy["allowed_tags"])
    strong_tags = set(evidence_policy["strong_evidence_tags"])

    seen_ids: list[str] = []
    assumption_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(assumptions):
        label = f"assumptions[{index}]"
        errors.extend(validate_required_fields(item, contract["assumption_fields"], label))
        assumption_id = str(item.get("id", ""))
        if not id_re.fullmatch(assumption_id):
            errors.append(f"{label}.id: must match {status_policy['id_pattern']}")
        if assumption_id in assumption_by_id:
            errors.append(f"{label}.id: duplicate assumption id {assumption_id}")
        seen_ids.append(assumption_id)
        assumption_by_id[assumption_id] = item

        status = item.get("status")
        if status not in allowed_statuses:
            errors.append(f"{label}.status: unsupported status {status}")
        tag = item.get("evidence_tag")
        if tag not in allowed_tags:
            errors.append(f"{label}.evidence_tag: unsupported tag {tag}")
        impact = item.get("impact")
        if impact not in allowed_impacts:
            errors.append(f"{label}.impact: unsupported impact {impact}")

        if status in closed_statuses and tag not in strong_tags:
            errors.append(f"{label}: closed status requires strong evidence tag")
        if status in {"validated", "invalidated"} and not str(item.get("source_ref", "")).strip():
            errors.append(f"{label}: {status} requires source_ref")
        if status in open_statuses and not str(item.get("validation_action", "")).strip():
            errors.append(f"{label}: open status requires validation_action")
        if status == "unvalidated" and tag != "[ASSUMPTION]":
            errors.append(f"{label}: unvalidated assumptions must use [ASSUMPTION]")

    expected_ids = [f"A-{index:03d}" for index in range(1, len(assumptions) + 1)]
    if seen_ids != expected_ids:
        errors.append(f"assumptions: ids must be ascending and gapless: {expected_ids}")

    open_count = sum(1 for item in assumptions if item.get("status") in open_statuses)
    validated_count = sum(1 for item in assumptions if item.get("status") == "validated")
    invalidated_count = sum(1 for item in assumptions if item.get("status") == "invalidated")
    high_open_ids = {
        str(item.get("id"))
        for item in assumptions
        if item.get("status") in open_statuses and item.get("impact") in {"high", "critical"}
    }
    assumption_ratio = (
        sum(1 for item in assumptions if item.get("evidence_tag") == "[ASSUMPTION]") / len(assumptions)
        if assumptions
        else 0.0
    )

    expected_summary = {
        "total_assumptions": len(assumptions),
        "open_count": open_count,
        "validated_count": validated_count,
        "invalidated_count": invalidated_count,
        "high_impact_open_count": len(high_open_ids),
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key}: expected {expected}, got {summary.get(key)}")
    if not isinstance(summary.get("assumption_ratio"), (int, float)):
        errors.append("summary.assumption_ratio: must be numeric")
    elif abs(float(summary["assumption_ratio"]) - assumption_ratio) > 0.001:
        errors.append(f"summary.assumption_ratio: expected {assumption_ratio:.3f}, got {summary['assumption_ratio']}")
    if summary.get("overall_risk") not in status_policy["risk_levels"]:
        errors.append(f"summary.overall_risk: unsupported risk {summary.get('overall_risk')}")

    contradictions = [require_object(item, f"contradictions[{index}]") for index, item in enumerate(require_list(report["contradictions"], "contradictions"))]
    for index, item in enumerate(contradictions):
        label = f"contradictions[{index}]"
        errors.extend(validate_required_fields(item, contract["contradiction_fields"], label))
        for assumption_id in item.get("assumption_ids", []):
            if assumption_id not in assumption_by_id:
                errors.append(f"{label}.assumption_ids: unknown id {assumption_id}")

    decision_links = [require_object(item, f"decision_links[{index}]") for index, item in enumerate(require_list(report["decision_links"], "decision_links"))]
    for index, item in enumerate(decision_links):
        label = f"decision_links[{index}]"
        errors.extend(validate_required_fields(item, contract["decision_link_fields"], label))
        for assumption_id in item.get("assumption_ids", []):
            if assumption_id not in assumption_by_id:
                errors.append(f"{label}.assumption_ids: unknown id {assumption_id}")

    queue = [require_object(item, f"validation_queue[{index}]") for index, item in enumerate(require_list(report["validation_queue"], "validation_queue"))]
    queued_ids: set[str] = set()
    for index, item in enumerate(queue):
        label = f"validation_queue[{index}]"
        errors.extend(validate_required_fields(item, contract["validation_queue_fields"], label))
        assumption_id = item.get("assumption_id")
        if assumption_id not in assumption_by_id:
            errors.append(f"{label}.assumption_id: unknown id {assumption_id}")
        else:
            queued_ids.add(str(assumption_id))
            if assumption_by_id[str(assumption_id)].get("status") not in open_statuses:
                errors.append(f"{label}.assumption_id: queue may only include open assumptions")

    missing_high_open = sorted(high_open_ids - queued_ids)
    if missing_high_open:
        errors.append(f"validation_queue: missing high-impact open assumptions {missing_high_open}")

    warnings = require_list(report["warnings"], "warnings")
    has_ratio_warning = any(
        isinstance(item, dict) and item.get("code") == "HIGH_ASSUMPTION_RATIO"
        for item in warnings
    )
    if assumption_ratio > 0.30 and not has_ratio_warning:
        errors.append("warnings: HIGH_ASSUMPTION_RATIO required when >30% entries use [ASSUMPTION]")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate assumption-log report fixtures")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--status-policy", required=True, type=Path)
    parser.add_argument("--evidence-policy", required=True, type=Path)
    args = parser.parse_args()

    try:
        report = require_object(load_json(args.report), "report")
        contract = require_object(load_json(args.contract), "contract")
        status_policy = require_object(load_json(args.status_policy), "status_policy")
        evidence_policy = require_object(load_json(args.evidence_policy), "evidence_policy")
        errors = validate_report(report, contract, status_policy, evidence_policy)
    except ValueError as exc:
        errors = [str(exc)]

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"report={args.report} valid=false errors={len(errors)}")
        return 1
    print(f"report={args.report} valid=true errors=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
