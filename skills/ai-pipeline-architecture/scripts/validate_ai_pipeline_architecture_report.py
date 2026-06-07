#!/usr/bin/env python3
"""Validate deterministic AI pipeline architecture reports."""

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


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_fields(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def validate_refs(errors: list[str], refs: Any, known_evidence: set[str], path: str) -> None:
    if not isinstance(refs, list) or not refs:
        errors.append(f"{path}: must be a non-empty list")
        return
    for ref in refs:
        if ref not in known_evidence:
            errors.append(f"{path}: unknown evidence id {ref}")


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
    require_fields(errors, system, "system", ["name", "domain", "mode", "risk_level", "regulated"])
    if not isinstance(system, dict):
        return
    for field in ("name", "domain"):
        if not is_non_empty_string(system.get(field)):
            errors.append(f"system.{field}: must be a non-empty string")
    if system.get("mode") not in {"greenfield", "modernization", "audit"}:
        errors.append("system.mode: must be greenfield, modernization, or audit")
    if system.get("risk_level") not in {"low", "medium", "high"}:
        errors.append("system.risk_level: must be low, medium, or high")
    if not isinstance(system.get("regulated"), bool):
        errors.append("system.regulated: must be boolean")


def validate_pipeline_stages(
    report: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    stage_policy: dict[str, Any],
) -> None:
    stages = report.get("pipeline_stages")
    if not isinstance(stages, list) or not stages:
        errors.append("pipeline_stages: must be a non-empty list")
        return
    seen_pipelines: set[str] = set()
    dev_stages = set(stage_policy["development_stages"])
    prod_stages = set(stage_policy["production_stages"])
    for index, item in enumerate(stages):
        path = f"pipeline_stages[{index}]"
        require_fields(errors, item, path, ["pipeline", "stage", "purpose", "inputs", "outputs", "gates", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        pipeline = item.get("pipeline")
        stage = item.get("stage")
        if pipeline not in set(stage_policy["allowed_pipelines"]):
            errors.append(f"{path}.pipeline: must be development or production")
        else:
            seen_pipelines.add(str(pipeline))
            allowed_stage_set = dev_stages if pipeline == "development" else prod_stages
            if stage not in allowed_stage_set:
                errors.append(f"{path}.stage: invalid {pipeline} stage {stage}")
        if not is_non_empty_string(item.get("purpose")):
            errors.append(f"{path}.purpose: must be a non-empty string")
        for field in ("inputs", "outputs", "gates"):
            if not isinstance(item.get(field), list) or not item[field]:
                errors.append(f"{path}.{field}: must be a non-empty list")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = {"development", "production"} - seen_pipelines
    if missing:
        errors.append(f"pipeline_stages: missing required pipeline coverage {sorted(missing)}")


def validate_data_stores(
    report: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    store_policy: dict[str, Any],
) -> None:
    stores = report.get("data_stores")
    if not isinstance(stores, list) or not stores:
        errors.append("data_stores: must be a non-empty list")
        return
    for index, item in enumerate(stores):
        path = f"data_stores[{index}]"
        require_fields(errors, item, path, ["store_type", "purpose", "consistency_model", "latency_class", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if item.get("store_type") not in set(store_policy["allowed_store_types"]):
            errors.append(f"{path}.store_type: must be one of {store_policy['allowed_store_types']}")
        if not is_non_empty_string(item.get("purpose")):
            errors.append(f"{path}.purpose: must be a non-empty string")
        if item.get("consistency_model") not in set(store_policy["allowed_consistency_models"]):
            errors.append(f"{path}.consistency_model: must be one of {store_policy['allowed_consistency_models']}")
        if item.get("latency_class") not in set(store_policy["allowed_latency_classes"]):
            errors.append(f"{path}.latency_class: must be one of {store_policy['allowed_latency_classes']}")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_registry(report: dict[str, Any], errors: list[str], known_evidence: set[str], registry_policy: dict[str, Any]) -> None:
    registry = report.get("model_registry")
    require_fields(errors, registry, "model_registry", ["tool_decision", "versioning_strategy", "capabilities", "promotion_stages", "evidence_ids"])
    if not isinstance(registry, dict):
        return
    if not is_non_empty_string(registry.get("tool_decision")):
        errors.append("model_registry.tool_decision: must be a non-empty string")
    if registry.get("versioning_strategy") not in set(registry_policy["allowed_versioning_strategies"]):
        errors.append("model_registry.versioning_strategy: invalid strategy")
    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, list):
        errors.append("model_registry.capabilities: must be a list")
    else:
        missing = set(registry_policy["required_capabilities"]) - set(capabilities)
        if missing:
            errors.append(f"model_registry.capabilities: missing {sorted(missing)}")
    stages = registry.get("promotion_stages")
    if not isinstance(stages, list):
        errors.append("model_registry.promotion_stages: must be a list")
    else:
        missing = set(registry_policy["required_promotion_stages"]) - set(stages)
        if missing:
            errors.append(f"model_registry.promotion_stages: missing {sorted(missing)}")
    validate_refs(errors, registry.get("evidence_ids"), known_evidence, "model_registry.evidence_ids")


def validate_cicd(report: dict[str, Any], errors: list[str], known_evidence: set[str], cicd_policy: dict[str, Any]) -> None:
    cicd = report.get("cicd")
    require_fields(errors, cicd, "cicd", ["strategy", "gates", "rollback_strategy", "evidence_ids"])
    if not isinstance(cicd, dict):
        return
    if cicd.get("strategy") not in set(cicd_policy["allowed_strategies"]):
        errors.append("cicd.strategy: invalid strategy")
    gates = cicd.get("gates")
    if not isinstance(gates, list):
        errors.append("cicd.gates: must be a list")
    else:
        missing = set(cicd_policy["required_gates"]) - set(gates)
        if missing:
            errors.append(f"cicd.gates: missing {sorted(missing)}")
    if not is_non_empty_string(cicd.get("rollback_strategy")):
        errors.append("cicd.rollback_strategy: must be a non-empty string")
    validate_refs(errors, cicd.get("evidence_ids"), known_evidence, "cicd.evidence_ids")


def validate_requirements(report: dict[str, Any], errors: list[str], known_evidence: set[str], req_policy: dict[str, Any]) -> None:
    requirements = report.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append("requirements: must be a non-empty list")
        return
    seen_categories: set[str] = set()
    prefixes = req_policy["id_prefixes"]
    for index, item in enumerate(requirements):
        path = f"requirements[{index}]"
        require_fields(errors, item, path, ["id", "category", "description", "threshold", "objective", "mapped_component", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        category = item.get("category")
        req_id = item.get("id")
        if category not in set(req_policy["allowed_categories"]):
            errors.append(f"{path}.category: invalid category")
        else:
            seen_categories.add(str(category))
            if not is_non_empty_string(req_id) or not str(req_id).startswith(prefixes[str(category)]):
                errors.append(f"{path}.id: must start with {prefixes[str(category)]}")
        for field in ("description", "threshold", "objective", "mapped_component"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be a non-empty string")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing_categories = set(req_policy["allowed_categories"]) - seen_categories
    if missing_categories:
        errors.append(f"requirements: missing categories {sorted(missing_categories)}")


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

    contract = load_json(ASSET_DIR / "pipeline-architecture-contract.json")
    stage_policy = load_json(ASSET_DIR / "stage-policy.json")
    store_policy = load_json(ASSET_DIR / "data-store-policy.json")
    registry_policy = load_json(ASSET_DIR / "registry-policy.json")
    cicd_policy = load_json(ASSET_DIR / "cicd-policy.json")
    req_policy = load_json(ASSET_DIR / "requirements-policy.json")

    require_fields(errors, report, "report", contract["required_top_level_fields"])
    if report.get("schema") != contract["report_schema"]:
        errors.append(f"schema: must be {contract['report_schema']}")
    known_evidence = validate_evidence(report, errors)
    validate_system(report, errors)
    validate_pipeline_stages(report, errors, known_evidence, stage_policy)
    validate_data_stores(report, errors, known_evidence, store_policy)
    validate_registry(report, errors, known_evidence, registry_policy)
    validate_cicd(report, errors, known_evidence, cicd_policy)
    validate_requirements(report, errors, known_evidence, req_policy)
    validate_validation(report, errors, set(contract["required_validation_checks"]))
    if not isinstance(report.get("risks"), list):
        errors.append("risks: must be a list")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI pipeline architecture report")
    parser.add_argument("report", help="Path to report JSON fixture")
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
