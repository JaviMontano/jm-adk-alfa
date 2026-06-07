#!/usr/bin/env python3
"""Validate deterministic analytics engineering reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def refs(errors: list[str], values: Any, known: set[str], path: str) -> None:
    if not isinstance(values, list) or not values:
        errors.append(f"{path}: must be a non-empty list")
        return
    for value in values:
        if value not in known:
            errors.append(f"{path}: unknown evidence id {value}")


def validate_system(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    system = report.get("system")
    require(errors, system, "system", contract["required_system_fields"])
    if isinstance(system, dict):
        for field in contract["required_system_fields"]:
            if not is_text(system.get(field)):
                errors.append(f"system.{field}: must be non-empty")


def validate_evidence(report: dict[str, Any], errors: list[str], policy: dict[str, Any]) -> set[str]:
    items = report.get("evidence")
    if not isinstance(items, list) or not items:
        errors.append("evidence: must be a non-empty list")
        return set()
    allowed_tags = set(policy["allowed_tags"])
    seen: set[str] = set()
    for index, item in enumerate(items):
        path = f"evidence[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if not is_text(evidence_id):
            errors.append(f"{path}.id: must be non-empty")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate {evidence_id}")
        else:
            seen.add(str(evidence_id))
        if item.get("tag") not in allowed_tags:
            errors.append(f"{path}.tag: invalid")
        for field in ("source", "summary"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
    return seen


def validate_sources(report: dict[str, Any], errors: list[str], known_evidence: set[str]) -> set[str]:
    items = report.get("sources")
    if not isinstance(items, list) or not items:
        errors.append("sources: must be a non-empty list")
        return set()
    source_ids: set[str] = set()
    for index, item in enumerate(items):
        path = f"sources[{index}]"
        require(errors, item, path, ["id", "system", "tables", "freshness_sla", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        source_id = item.get("id")
        if is_text(source_id):
            source_ids.add(str(source_id))
        for field in ("system", "freshness_sla"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        tables = item.get("tables")
        if not isinstance(tables, list) or not tables or not all(is_text(table) for table in tables):
            errors.append(f"{path}.tables: must be a non-empty list of strings")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return source_ids


def layer_maps(policy: dict[str, Any]) -> tuple[dict[str, list[str]], dict[str, list[str]], set[str]]:
    prefixes: dict[str, list[str]] = {}
    materializations: dict[str, list[str]] = {}
    raw_allowed: set[str] = set()
    for layer in policy["layers"]:
        name = layer["layer"]
        prefixes[name] = layer["allowed_prefixes"]
        materializations[name] = layer["allowed_materializations"]
        if layer.get("raw_sources_allowed"):
            raw_allowed.add(name)
    return prefixes, materializations, raw_allowed


def validate_models(
    report: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    layer_policy: dict[str, Any],
    materialization_policy: dict[str, Any],
    known_sources: set[str],
) -> dict[str, dict[str, Any]]:
    items = report.get("models")
    if not isinstance(items, list) or not items:
        errors.append("models: must be a non-empty list")
        return {}
    prefixes, layer_materializations, raw_allowed = layer_maps(layer_policy)
    allowed_layers = set(prefixes)
    allowed_incremental = set(materialization_policy["allowed_incremental_strategies"])
    models: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        path = f"models[{index}]"
        require(errors, item, path, materialization_policy["required_model_fields"])
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        layer = item.get("layer")
        materialization = item.get("materialization")
        if not is_text(name):
            errors.append(f"{path}.name: must be non-empty")
            continue
        model_name = str(name)
        if model_name in models:
            errors.append(f"{path}.name: duplicate {model_name}")
        models[model_name] = item
        if layer not in allowed_layers:
            errors.append(f"{path}.layer: invalid")
        else:
            if not any(model_name.startswith(prefix) for prefix in prefixes[str(layer)]):
                errors.append(f"{path}.name: prefix invalid for layer {layer}")
            if materialization not in layer_materializations[str(layer)]:
                errors.append(f"{path}.materialization: invalid for layer {layer}")
        for field in ("grain", "owner"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        columns = item.get("columns")
        if not isinstance(columns, list) or not columns or not all(is_text(column) for column in columns):
            errors.append(f"{path}.columns: must be a non-empty list of strings")
        upstream = item.get("upstream")
        if not isinstance(upstream, list):
            errors.append(f"{path}.upstream: must be a list")
        elif layer != "staging" and not upstream:
            errors.append(f"{path}.upstream: non-staging model requires upstream dependencies")
        elif layer == "staging" and upstream:
            unknown_sources = [value for value in upstream if value not in known_sources]
            if unknown_sources:
                errors.append(f"{path}.upstream: staging model references unknown sources {unknown_sources}")
        elif layer not in raw_allowed:
            raw_refs = [value for value in upstream if value in known_sources]
            if raw_refs:
                errors.append(f"{path}.upstream: non-staging model cannot reference raw sources {raw_refs}")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
        if materialization == "incremental":
            for field in materialization_policy["incremental_required_fields"]:
                if not is_text(item.get(field)):
                    errors.append(f"{path}.{field}: required for incremental models")
            if item.get("incremental_strategy") not in allowed_incremental:
                errors.append(f"{path}.incremental_strategy: invalid")
    for name, item in models.items():
        if item.get("layer") == "staging":
            continue
        for upstream in item.get("upstream", []):
            if upstream not in models:
                errors.append(f"models[{name}].upstream: unknown model {upstream}")
    return models


def validate_tests(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_evidence: set[str], models: dict[str, dict[str, Any]]) -> None:
    items = report.get("tests")
    if not isinstance(items, list) or not items:
        errors.append("tests: must be a non-empty list")
        return
    allowed_types = set(policy["allowed_test_types"])
    allowed_severities = set(policy["allowed_severities"])
    tests_by_model: dict[str, set[str]] = {}
    for index, item in enumerate(items):
        path = f"tests[{index}]"
        require(errors, item, path, policy["required_test_fields"])
        if not isinstance(item, dict):
            continue
        model_name = item.get("model_name")
        if model_name not in models:
            errors.append(f"{path}.model_name: unknown")
        else:
            tests_by_model.setdefault(str(model_name), set()).add(str(item.get("test_type")))
        if item.get("test_type") not in allowed_types:
            errors.append(f"{path}.test_type: invalid")
        if item.get("severity") not in allowed_severities:
            errors.append(f"{path}.severity: invalid")
        if not is_text(item.get("field")):
            errors.append(f"{path}.field: must be non-empty")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    required = set(policy["mart_required_test_types"])
    for model_name, model in models.items():
        if model.get("layer") == "mart":
            missing = required - tests_by_model.get(model_name, set())
            if missing:
                errors.append(f"tests: mart {model_name} missing required tests {sorted(missing)}")


def validate_contracts(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_evidence: set[str], models: dict[str, dict[str, Any]]) -> None:
    items = report.get("data_contracts")
    if not isinstance(items, list) or not items:
        errors.append("data_contracts: must be a non-empty list")
        return
    allowed_policies = set(policy["allowed_breaking_change_policies"])
    contracts_by_model: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        path = f"data_contracts[{index}]"
        require(errors, item, path, policy["required_contract_fields"])
        if not isinstance(item, dict):
            continue
        model_name = item.get("model_name")
        if model_name not in models:
            errors.append(f"{path}.model_name: unknown")
        else:
            contracts_by_model[str(model_name)] = item
        if not isinstance(item.get("enforced"), bool):
            errors.append(f"{path}.enforced: must be boolean")
        if not is_text(item.get("owner")):
            errors.append(f"{path}.owner: must be non-empty")
        if item.get("breaking_change_policy") not in allowed_policies:
            errors.append(f"{path}.breaking_change_policy: invalid")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    required_layers = set(policy["production_layers_requiring_contracts"])
    for model_name, model in models.items():
        if model.get("layer") in required_layers:
            contract = contracts_by_model.get(model_name)
            if contract is None:
                errors.append(f"data_contracts: missing contract for {model_name}")
            elif contract.get("enforced") is not True:
                errors.append(f"data_contracts: contract for {model_name} must be enforced")


def validate_lineage(report: dict[str, Any], errors: list[str], known_sources: set[str], models: dict[str, dict[str, Any]]) -> None:
    items = report.get("lineage")
    if not isinstance(items, list) or not items:
        errors.append("lineage: must be a non-empty list")
        return
    known_nodes = known_sources | set(models)
    incoming: dict[str, int] = {name: 0 for name, model in models.items() if model.get("layer") != "staging"}
    for index, item in enumerate(items):
        path = f"lineage[{index}]"
        require(errors, item, path, ["from", "to"])
        if not isinstance(item, dict):
            continue
        src = item.get("from")
        dst = item.get("to")
        if src not in known_nodes:
            errors.append(f"{path}.from: unknown")
        if dst not in known_nodes:
            errors.append(f"{path}.to: unknown")
        if dst in incoming:
            incoming[str(dst)] += 1
    for model_name, count in incoming.items():
        if count == 0:
            errors.append(f"lineage: missing incoming edge for {model_name}")


def validate_docs(report: dict[str, Any], errors: list[str], models: dict[str, dict[str, Any]]) -> None:
    items = report.get("documentation")
    if not isinstance(items, list) or not items:
        errors.append("documentation: must be a non-empty list")
        return
    docs_by_model: set[str] = set()
    for index, item in enumerate(items):
        path = f"documentation[{index}]"
        require(errors, item, path, ["model_name", "description", "column_descriptions", "owner"])
        if not isinstance(item, dict):
            continue
        model_name = item.get("model_name")
        if model_name not in models:
            errors.append(f"{path}.model_name: unknown")
        else:
            docs_by_model.add(str(model_name))
        for field in ("description", "owner"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        columns = item.get("column_descriptions")
        if not isinstance(columns, list) or not columns or not all(is_text(column) for column in columns):
            errors.append(f"{path}.column_descriptions: must be a non-empty list of strings")
    for model_name, model in models.items():
        if model.get("layer") == "mart" and model_name not in docs_by_model:
            errors.append(f"documentation: missing mart documentation for {model_name}")


def validate_validation(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    validation = report.get("validation")
    require(errors, validation, "validation", ["status", "checks"])
    if not isinstance(validation, dict):
        return
    if validation.get("status") not in set(contract["allowed_validation_statuses"]):
        errors.append("validation.status: invalid")
    checks = validation.get("checks")
    if not isinstance(checks, list):
        errors.append("validation.checks: must be a list")
        return
    missing = set(contract["required_validation_checks"]) - set(checks)
    if missing:
        errors.append(f"validation.checks: missing required checks {sorted(missing)}")


def validate_report(report: dict[str, Any]) -> list[str]:
    contract = load_json(ASSET_DIR / "analytics-engineering-contract.json")
    layer_policy = load_json(ASSET_DIR / "layer-policy.json")
    materialization_policy = load_json(ASSET_DIR / "materialization-policy.json")
    testing_policy = load_json(ASSET_DIR / "testing-policy.json")
    data_contract_policy = load_json(ASSET_DIR / "data-contract-policy.json")
    evidence_policy = load_json(ASSET_DIR / "evidence-policy.json")
    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing required section {section}")
    if errors:
        return errors
    validate_system(report, errors, contract)
    known_evidence = validate_evidence(report, errors, evidence_policy)
    known_sources = validate_sources(report, errors, known_evidence)
    models = validate_models(report, errors, known_evidence, layer_policy, materialization_policy, known_sources)
    validate_tests(report, errors, testing_policy, known_evidence, models)
    validate_contracts(report, errors, data_contract_policy, known_evidence, models)
    validate_lineage(report, errors, known_sources, models)
    validate_docs(report, errors, models)
    validate_validation(report, errors, contract)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an analytics engineering JSON handoff")
    parser.add_argument("report")
    args = parser.parse_args()
    report_path = Path(args.report)
    try:
        report = load_json(report_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {report_path}: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(report, dict):
        print(f"ERROR {report_path}: root must be an object", file=sys.stderr)
        return 1
    errors = validate_report(report)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(f"report={report_path.name} status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
