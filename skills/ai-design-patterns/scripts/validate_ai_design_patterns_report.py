#!/usr/bin/env python3
"""Validate deterministic AI design pattern selection reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_fields(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def validate_evidence(report: dict[str, Any], errors: list[str]) -> set[str]:
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence: must be a non-empty list")
        return set()

    allowed_tags = {"[EXPLICIT]", "[INFERRED]", "[OPEN]"}
    seen: set[str] = set()
    for index, item in enumerate(evidence):
        path = f"evidence[{index}]"
        require_fields(errors, item, path, ["id", "tag", "source", "summary"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if not is_non_empty_string(evidence_id):
            errors.append(f"{path}.id: must be a non-empty string")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate evidence id {evidence_id}")
        else:
            seen.add(evidence_id)
        if item.get("tag") not in allowed_tags:
            errors.append(f"{path}.tag: must be one of {sorted(allowed_tags)}")
        for field in ("source", "summary"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be a non-empty string")
    return seen


def validate_system(report: dict[str, Any], errors: list[str]) -> None:
    system = report.get("system")
    require_fields(errors, system, "system", ["name", "domain", "risk_level", "regulatory_context"])
    if not isinstance(system, dict):
        return
    if not is_non_empty_string(system.get("name")):
        errors.append("system.name: must be a non-empty string")
    if not is_non_empty_string(system.get("domain")):
        errors.append("system.domain: must be a non-empty string")
    if system.get("risk_level") not in {"low", "medium", "high"}:
        errors.append("system.risk_level: must be low, medium, or high")
    if not isinstance(system.get("regulatory_context"), bool):
        errors.append("system.regulatory_context: must be boolean")


def validate_requirements(report: dict[str, Any], errors: list[str]) -> None:
    requirements = report.get("requirements")
    require_fields(errors, requirements, "requirements", ["quality_attributes", "constraints", "model_count", "traffic_profile"])
    if not isinstance(requirements, dict):
        return
    if not isinstance(requirements.get("quality_attributes"), list) or not requirements["quality_attributes"]:
        errors.append("requirements.quality_attributes: must be a non-empty list")
    if not isinstance(requirements.get("constraints"), list):
        errors.append("requirements.constraints: must be a list")
    if not isinstance(requirements.get("model_count"), int) or requirements["model_count"] < 1:
        errors.append("requirements.model_count: must be an integer >= 1")
    if requirements.get("traffic_profile") not in {"low", "medium", "high"}:
        errors.append("requirements.traffic_profile: must be low, medium, or high")


def validate_detected_context(report: dict[str, Any], errors: list[str]) -> None:
    context = report.get("detected_context")
    fields = ["feature_store_present", "model_registry_present", "monitoring_present"]
    require_fields(errors, context, "detected_context", fields)
    if not isinstance(context, dict):
        return
    for field in fields:
        if not isinstance(context.get(field), bool):
            errors.append(f"detected_context.{field}: must be boolean")


def validate_anti_patterns(
    report: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    allowed_patterns: set[str],
    allowed_severities: set[str],
    anti_required_fields: list[str],
) -> set[str]:
    anti_patterns = report.get("anti_patterns")
    if not isinstance(anti_patterns, list):
        errors.append("anti_patterns: must be a list")
        return set()

    anti_ids: set[str] = set()
    for index, item in enumerate(anti_patterns):
        path = f"anti_patterns[{index}]"
        require_fields(errors, item, path, anti_required_fields)
        if not isinstance(item, dict):
            continue
        anti_id = item.get("id")
        if not is_non_empty_string(anti_id):
            errors.append(f"{path}.id: must be a non-empty string")
        elif anti_id in anti_ids:
            errors.append(f"{path}.id: duplicate anti-pattern id {anti_id}")
        else:
            anti_ids.add(anti_id)
        if not is_non_empty_string(item.get("name")):
            errors.append(f"{path}.name: must be a non-empty string")
        if item.get("severity") not in allowed_severities:
            errors.append(f"{path}.severity: must be one of {sorted(allowed_severities)}")
        if not is_non_empty_string(item.get("detection_signal")):
            errors.append(f"{path}.detection_signal: must be a non-empty string")
        if item.get("remediation_pattern") not in allowed_patterns:
            errors.append(f"{path}.remediation_pattern: must be in the allowed pattern catalog")
        validate_evidence_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return anti_ids


def validate_evidence_refs(errors: list[str], refs: Any, known_evidence: set[str], path: str) -> None:
    if not isinstance(refs, list) or not refs:
        errors.append(f"{path}: must be a non-empty list")
        return
    for ref in refs:
        if ref not in known_evidence:
            errors.append(f"{path}: unknown evidence id {ref}")


def validate_pattern_recommendations(
    report: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    anti_ids: set[str],
    allowed_patterns: set[str],
    allowed_priorities: set[str],
    dependency_policy: dict[str, list[str]],
) -> None:
    recommendations = report.get("pattern_recommendations")
    if not isinstance(recommendations, list) or not recommendations:
        errors.append("pattern_recommendations: must be a non-empty list")
        return

    for index, item in enumerate(recommendations):
        path = f"pattern_recommendations[{index}]"
        require_fields(
            errors,
            item,
            path,
            ["pattern", "priority", "rationale", "tradeoffs", "required_tactics", "dependencies", "evidence_ids", "addresses"],
        )
        if not isinstance(item, dict):
            continue
        pattern = item.get("pattern")
        if pattern not in allowed_patterns:
            errors.append(f"{path}.pattern: must be in the allowed pattern catalog")
        if item.get("priority") not in allowed_priorities:
            errors.append(f"{path}.priority: must be one of {sorted(allowed_priorities)}")
        if not is_non_empty_string(item.get("rationale")):
            errors.append(f"{path}.rationale: must be a non-empty string")
        for list_field in ("tradeoffs", "required_tactics"):
            if not isinstance(item.get(list_field), list) or not item[list_field]:
                errors.append(f"{path}.{list_field}: must be a non-empty list")
        if not isinstance(item.get("dependencies"), list):
            errors.append(f"{path}.dependencies: must be a list")
        else:
            missing = set(dependency_policy.get(str(pattern), [])) - set(item["dependencies"])
            if missing:
                errors.append(f"{path}.dependencies: missing required dependencies {sorted(missing)}")
            for dependency in item["dependencies"]:
                if dependency not in allowed_patterns:
                    errors.append(f"{path}.dependencies: unknown dependency {dependency}")
        validate_evidence_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
        addresses = item.get("addresses")
        if not isinstance(addresses, list):
            errors.append(f"{path}.addresses: must be a list")
        else:
            for anti_id in addresses:
                if anti_id not in anti_ids:
                    errors.append(f"{path}.addresses: unknown anti-pattern id {anti_id}")


def validate_tactics(
    report: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    allowed_categories: set[str],
    tactic_required_fields: list[str],
) -> None:
    tactics = report.get("tactics")
    if not isinstance(tactics, list) or not tactics:
        errors.append("tactics: must be a non-empty list")
        return
    for index, item in enumerate(tactics):
        path = f"tactics[{index}]"
        require_fields(errors, item, path, tactic_required_fields)
        if not isinstance(item, dict):
            continue
        if item.get("category") not in allowed_categories:
            errors.append(f"{path}.category: must be one of {sorted(allowed_categories)}")
        for field in ("name", "mapped_component"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be a non-empty string")
        validate_evidence_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_roadmap(
    report: dict[str, Any],
    errors: list[str],
    allowed_patterns: set[str],
    roadmap_required_fields: list[str],
) -> None:
    roadmap = report.get("roadmap")
    if not isinstance(roadmap, list) or not roadmap:
        errors.append("roadmap: must be a non-empty list")
        return
    for index, item in enumerate(roadmap):
        path = f"roadmap[{index}]"
        require_fields(errors, item, path, roadmap_required_fields)
        if not isinstance(item, dict):
            continue
        if not is_non_empty_string(item.get("phase")):
            errors.append(f"{path}.phase: must be a non-empty string")
        if not isinstance(item.get("patterns"), list) or not item["patterns"]:
            errors.append(f"{path}.patterns: must be a non-empty list")
        else:
            for pattern in item["patterns"]:
                if pattern not in allowed_patterns:
                    errors.append(f"{path}.patterns: unknown pattern {pattern}")
        if not isinstance(item.get("exit_criteria"), list) or not item["exit_criteria"]:
            errors.append(f"{path}.exit_criteria: must be a non-empty list")


def validate_validation(report: dict[str, Any], errors: list[str], required_checks: set[str]) -> None:
    validation = report.get("validation")
    require_fields(errors, validation, "validation", ["status", "checks"])
    if not isinstance(validation, dict):
        return
    if validation.get("status") not in {"pass", "warn", "block"}:
        errors.append("validation.status: must be pass, warn, or block")
    checks = validation.get("checks")
    if not isinstance(checks, list):
        errors.append("validation.checks: must be a list")
    else:
        missing = required_checks - set(checks)
        if missing:
            errors.append(f"validation.checks: missing required checks {sorted(missing)}")


def validate_report(report_path: Path) -> list[str]:
    errors: list[str] = []
    report = load_json(report_path)
    if not isinstance(report, dict):
        return ["report: must be a JSON object"]

    contract = load_json(ASSET_DIR / "pattern-selection-contract.json")
    catalog = load_json(ASSET_DIR / "pattern-catalog-policy.json")
    anti_policy = load_json(ASSET_DIR / "anti-pattern-policy.json")
    tactic_policy = load_json(ASSET_DIR / "tactic-policy.json")
    dependency_policy = load_json(ASSET_DIR / "dependency-policy.json")
    roadmap_policy = load_json(ASSET_DIR / "roadmap-policy.json")

    required_top_level = contract["required_top_level_fields"]
    require_fields(errors, report, "report", required_top_level)
    if report.get("schema") != contract["report_schema"]:
        errors.append(f"schema: must be {contract['report_schema']}")

    allowed_patterns = set(catalog["allowed_patterns"])
    allowed_priorities = set(catalog["priorities"])
    known_evidence = validate_evidence(report, errors)

    validate_system(report, errors)
    validate_requirements(report, errors)
    validate_detected_context(report, errors)
    anti_ids = validate_anti_patterns(
        report=report,
        errors=errors,
        known_evidence=known_evidence,
        allowed_patterns=allowed_patterns,
        allowed_severities=set(anti_policy["allowed_severities"]),
        anti_required_fields=anti_policy["required_fields"],
    )
    validate_pattern_recommendations(
        report=report,
        errors=errors,
        known_evidence=known_evidence,
        anti_ids=anti_ids,
        allowed_patterns=allowed_patterns,
        allowed_priorities=allowed_priorities,
        dependency_policy=dependency_policy["dependencies"],
    )
    validate_tactics(
        report=report,
        errors=errors,
        known_evidence=known_evidence,
        allowed_categories=set(tactic_policy["allowed_categories"]),
        tactic_required_fields=tactic_policy["required_fields"],
    )
    validate_roadmap(
        report=report,
        errors=errors,
        allowed_patterns=allowed_patterns,
        roadmap_required_fields=roadmap_policy["required_fields"],
    )
    validate_validation(report, errors, set(contract["required_validation_checks"]))

    if not isinstance(report.get("risks"), list):
        errors.append("risks: must be a list")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI design patterns report")
    parser.add_argument("report", help="Path to a report JSON fixture")
    args = parser.parse_args()

    report_path = Path(args.report)
    try:
        errors = validate_report(report_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {report_path}: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR {report_path}: {error}", file=sys.stderr)
        return 1

    print(f"report={report_path.name} status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
