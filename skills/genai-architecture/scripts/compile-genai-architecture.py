#!/usr/bin/env python3
"""Compile a deterministic GenAI architecture report from structured JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{key} must be a non-empty object")
    return value


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def validate_required_fields(data: dict[str, Any], required: list[str], label: str) -> None:
    missing = [field for field in required if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def validate_root(data: dict[str, Any], schema: dict[str, Any]) -> None:
    validate_required_fields(data, schema["required_root_fields"], "root")
    for key, allowed_key in [
        ("scope", "allowed_scope"),
        ("deployment_preference", "allowed_deployment_preference"),
        ("data_sensitivity", "allowed_data_sensitivity"),
    ]:
        if data[key] not in schema[allowed_key]:
            raise ValueError(f"unsupported {key}: {data[key]}")
    if not isinstance(data["evidence"], dict) or not data["evidence"]:
        raise ValueError("evidence must be a non-empty object")


def validate_knowledge_base(data: dict[str, Any], schema: dict[str, Any]) -> None:
    kb = require_object(data, "knowledge_base")
    validate_required_fields(kb, schema["required_knowledge_base_fields"], "knowledge_base")
    if kb["size"] not in schema["allowed_knowledge_base_size"]:
        raise ValueError(f"unsupported knowledge_base.size: {kb['size']}")
    if kb["update_frequency"] not in schema["allowed_update_frequency"]:
        raise ValueError(f"unsupported knowledge_base.update_frequency: {kb['update_frequency']}")
    if not isinstance(kb["languages"], list) or not kb["languages"]:
        raise ValueError("knowledge_base.languages must be a non-empty list")
    if not isinstance(kb["source_count"], int) or kb["source_count"] <= 0:
        raise ValueError("knowledge_base.source_count must be a positive integer")


def validate_sources(data: dict[str, Any], schema: dict[str, Any]) -> None:
    sources = require_list(data, "knowledge_sources")
    required = schema["required_source_fields"]
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each knowledge source must be an object")
        validate_required_fields(source, required, "knowledge_source")


def validate_rag_pipeline(data: dict[str, Any], schema: dict[str, Any]) -> None:
    stages = require_list(data, "rag_pipeline")
    required_ids = set(schema["required_rag_stage_ids"])
    required_fields = set(schema["required_rag_stage_fields"])
    seen = {stage.get("id") for stage in stages if isinstance(stage, dict)}
    missing_ids = required_ids - seen
    if missing_ids:
        raise ValueError(f"rag_pipeline missing required stage ids: {sorted(missing_ids)}")
    for stage in stages:
        if not isinstance(stage, dict):
            raise ValueError("each rag_pipeline stage must be an object")
        missing = required_fields - set(stage)
        if missing:
            raise ValueError(f"rag_pipeline stage missing fields: {sorted(missing)}")


def validate_use_cases(data: dict[str, Any], schema: dict[str, Any]) -> None:
    use_cases = require_list(data, "use_cases")
    required = set(schema["required_use_case_fields"])
    for use_case in use_cases:
        if not isinstance(use_case, dict):
            raise ValueError("each use case must be an object")
        missing = required - set(use_case)
        if missing:
            raise ValueError(f"use case missing fields: {sorted(missing)}")
        if use_case["latency_class"] not in schema["allowed_latency_class"]:
            raise ValueError(f"unsupported latency_class: {use_case['latency_class']}")
        if use_case["quality_risk"] not in schema["allowed_quality_risk"]:
            raise ValueError(f"unsupported quality_risk: {use_case['quality_risk']}")


def validate_model_tiers(data: dict[str, Any], schema: dict[str, Any]) -> None:
    tiers = require_list(data, "model_tiers")
    required = set(schema["required_model_tier_fields"])
    for tier in tiers:
        if not isinstance(tier, dict):
            raise ValueError("each model tier must be an object")
        missing = required - set(tier)
        if missing:
            raise ValueError(f"model tier missing fields: {sorted(missing)}")


def validate_connectors(data: dict[str, Any], schema: dict[str, Any]) -> None:
    connectors = require_list(data, "connectors")
    required = set(schema["required_connector_fields"])
    for connector in connectors:
        if not isinstance(connector, dict):
            raise ValueError("each connector must be an object")
        missing = required - set(connector)
        if missing:
            raise ValueError(f"connector missing fields: {sorted(missing)}")


def validate_quality(data: dict[str, Any], schema: dict[str, Any]) -> None:
    quality = require_list(data, "quality_targets")
    required = set(schema["required_quality_fields"])
    for target in quality:
        if not isinstance(target, dict):
            raise ValueError("each quality target must be an object")
        missing = required - set(target)
        if missing:
            raise ValueError(f"quality target missing fields: {sorted(missing)}")


def validate_input(data: dict[str, Any], base: Path) -> None:
    schema = load_json(base / "assets" / "genai-architecture-schema.json")
    validate_root(data, schema)
    validate_knowledge_base(data, schema)
    validate_sources(data, schema)
    validate_rag_pipeline(data, schema)
    validate_use_cases(data, schema)
    validate_model_tiers(data, schema)
    validate_connectors(data, schema)
    validate_quality(data, schema)


def recommend_pattern(data: dict[str, Any], model: dict[str, Any]) -> str:
    kb = data["knowledge_base"]
    if any(use_case.get("intent") == "multi-step-tool-use" for use_case in data["use_cases"]):
        key = "multi_step_tools"
    elif kb["size"] == "small" and kb["update_frequency"] == "stable":
        key = "small_stable"
    elif data["data_sensitivity"] in {"confidential", "regulated"} or kb["size"] == "large":
        key = "large_or_regulated"
    else:
        key = "medium_or_daily"
    recommendation = model["default_recommendations"][key]
    variant = next(item for item in model["variants"] if item["id"] == recommendation)
    return f"{variant['label']} ({variant['id']})"


def recommend_vector_db(data: dict[str, Any], matrix: dict[str, Any]) -> str:
    deployment = data["deployment_preference"]
    sensitivity = data["data_sensitivity"]
    kb_size = data["knowledge_base"]["size"]
    if deployment == "existing-postgres":
        name = "pgvector"
    elif sensitivity in {"regulated", "confidential"} and deployment == "self-hosted":
        name = "Qdrant"
    elif deployment == "managed" and kb_size == "large":
        name = "Pinecone"
    elif deployment == "hybrid":
        name = "Qdrant"
    else:
        name = "Qdrant"
    platform = next(item for item in matrix["platforms"] if item["name"].lower() == name.lower())
    return f"{platform['name']} — {platform['best_for']}"


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def knowledge_base_lines(data: dict[str, Any]) -> str:
    kb = data["knowledge_base"]
    languages = ", ".join(kb["languages"])
    lines = [
        f"- [CODE] Size: {kb['size']}.",
        f"- [CODE] Update frequency: {kb['update_frequency']}.",
        f"- [CODE] Languages: {languages}.",
        f"- [CODE] Source count: {kb['source_count']}.",
        "",
        "| Source | Type | Update | Access | Sensitivity | Owner |",
        "|---|---|---|---|---|---|",
    ]
    for source in data["knowledge_sources"]:
        lines.append(
            f"| {source['name']} | {source['type']} | {source['update_frequency']} | "
            f"{source['access_model']} | {source['sensitivity']} | {source['owner']} |"
        )
    return "\n".join(lines)


def rag_pipeline_table(stages: list[dict[str, Any]]) -> str:
    lines = [
        "| Stage | Decision | Mechanism | Owner | Metric |",
        "|---|---|---|---|---|",
    ]
    for stage in stages:
        lines.append(
            f"| {stage['id']} | {stage['decision']} | {stage['mechanism']} | "
            f"{stage['owner']} | {stage['metric']} |"
        )
    return "\n".join(lines)


def model_routing_table(data: dict[str, Any], matrix: dict[str, Any]) -> str:
    controls = "; ".join(matrix["mandatory_controls"])
    lines = [
        f"- [CODE] Mandatory routing controls: {controls}.",
        "",
        "| Tier | Class | Use case | Trigger | Fallback |",
        "|---|---|---|---|---|",
    ]
    for tier in data["model_tiers"]:
        lines.append(
            f"| {tier['tier']} | {tier['class']} | {tier['use_case']} | "
            f"{tier['trigger']} | {tier['fallback']} |"
        )
    return "\n".join(lines)


def vector_decision_lines(data: dict[str, Any], matrix: dict[str, Any], recommendation: str) -> str:
    required = "; ".join(matrix["required_decisions"])
    lines = [
        f"- [CODE] Recommendation: {recommendation}.",
        f"- [CODE] Required decisions: {required}.",
        "",
        "| Platform | Deployment | Scale | Filtering | Hybrid | Best for |",
        "|---|---|---|---|---|---|",
    ]
    for platform in matrix["platforms"]:
        lines.append(
            f"| {platform['name']} | {platform['deployment']} | {platform['scale']} | "
            f"{platform['metadata_filtering']} | {platform['hybrid_search']} | {platform['best_for']} |"
        )
    return "\n".join(lines)


def connector_lines(data: dict[str, Any], model: dict[str, Any]) -> str:
    controls = "; ".join(model["mandatory_security_controls"])
    lines = [
        f"- [CODE] Mandatory connector controls: {controls}.",
        "",
        "| Connector | Type | Access pattern | Security control | Fallback |",
        "|---|---|---|---|---|",
    ]
    for connector in data["connectors"]:
        lines.append(
            f"| {connector['name']} | {connector['type']} | {connector['access_pattern']} | "
            f"{connector['security_control']} | {connector['fallback']} |"
        )
    return "\n".join(lines)


def quality_lines(data: dict[str, Any], model: dict[str, Any]) -> str:
    guardrails = "; ".join(model["guardrails"])
    cycle = " -> ".join(model["improvement_cycle"])
    lines = [
        f"- [CODE] Guardrails: {guardrails}.",
        f"- [CODE] Improvement cycle: {cycle}.",
        "",
        "| Metric | Target | Measurement | Owner |",
        "|---|---|---|---|",
    ]
    for target in data["quality_targets"]:
        lines.append(
            f"| {target['metric']} | {target['target']} | {target['measurement']} | {target['owner']} |"
        )
    return "\n".join(lines)


def validation_lines(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "- [CODE] Required RAG stages are present: query_processing, retrieval, context_assembly, generation, validation.",
            "- [CODE] Knowledge sources have owner, access model, sensitivity, and update frequency.",
            "- [CODE] Model tiers include trigger and fallback behavior.",
            "- [CODE] Connectors include security control and degraded fallback.",
            "- [CODE] Quality targets include metric, target, measurement, and owner.",
        ]
    )


def risk_lines(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "- [INFERENCE] Architecture recommendations require benchmark validation before production rollout.",
            "- [INFERENCE] Retrieval quality depends on source quality, chunking, metadata, and labeled eval sets.",
            "- [ASSUMPTION] Input evidence and constraints are accepted as the source of truth for this deterministic report.",
        ]
    )


def render(data: dict[str, Any], base: Path) -> str:
    rag_model = load_json(base / "assets" / "rag-pattern-model.json")
    routing = load_json(base / "assets" / "model-routing-matrix.json")
    vector = load_json(base / "assets" / "vector-db-selection-matrix.json")
    connectors = load_json(base / "assets" / "connector-security-model.json")
    quality = load_json(base / "assets" / "qa-metrics-model.json")
    template = (base / "assets" / "genai-architecture-report-template.md").read_text(encoding="utf-8")
    pattern = recommend_pattern(data, rag_model)
    vector_db = recommend_vector_db(data, vector)
    replacements = {
        "{{SYSTEM_NAME}}": str(data["system_name"]),
        "{{AUDIENCE}}": str(data["audience"]),
        "{{BUSINESS_GOAL}}": str(data["business_goal"]),
        "{{SCOPE}}": str(data["scope"]),
        "{{DEPLOYMENT_PREFERENCE}}": str(data["deployment_preference"]),
        "{{DATA_SENSITIVITY}}": str(data["data_sensitivity"]),
        "{{RECOMMENDED_PATTERN}}": pattern,
        "{{RECOMMENDED_VECTOR_DB}}": vector_db,
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{KNOWLEDGE_BASE}}": knowledge_base_lines(data),
        "{{RAG_PIPELINE}}": rag_pipeline_table(data["rag_pipeline"]),
        "{{MODEL_ROUTING}}": model_routing_table(data, routing),
        "{{VECTOR_DECISION}}": vector_decision_lines(data, vector, vector_db),
        "{{CONNECTORS}}": connector_lines(data, connectors),
        "{{QUALITY}}": quality_lines(data, quality),
        "{{VALIDATION}}": validation_lines(data),
        "{{RISKS}}": risk_lines(data),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic GenAI architecture report")
    parser.add_argument("--input", required=True, help="Structured GenAI architecture JSON")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        data = load_json(Path(args.input))
        validate_input(data, base)
        output = render(data, base)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
