#!/usr/bin/env python3
"""Compile a deterministic funnel design from structured JSON."""

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


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def validate_root(data: dict[str, Any], schema: dict[str, Any]) -> None:
    missing = [key for key in schema["required_root_fields"] if key not in data]
    if missing:
        raise ValueError(f"missing required root fields: {missing}")
    if data["sales_motion"] not in schema["allowed_sales_motions"]:
        raise ValueError(f"unsupported sales_motion: {data['sales_motion']}")
    if not isinstance(data["evidence"], dict) or not data["evidence"]:
        raise ValueError("evidence must be a non-empty object")


def validate_stages(data: dict[str, Any], schema: dict[str, Any], stage_model: dict[str, Any]) -> None:
    stages = require_list(data, "stages")
    required_ids = set(schema["required_stage_ids"])
    required_fields = set(schema["required_stage_fields"])
    seen = {stage.get("id") for stage in stages if isinstance(stage, dict)}
    missing_ids = required_ids - seen
    if missing_ids:
        raise ValueError(f"stages missing required ids: {sorted(missing_ids)}")
    min_assets = {stage["id"]: int(stage["minimum_assets"]) for stage in stage_model["stages"]}
    for stage in stages:
        if not isinstance(stage, dict):
            raise ValueError("each stage must be an object")
        missing = required_fields - set(stage)
        if missing:
            raise ValueError(f"stage missing fields: {sorted(missing)}")
        assets = stage["content_assets"]
        if not isinstance(assets, list) or len(assets) < min_assets.get(stage["id"], 1):
            raise ValueError(f"stage {stage['id']} must contain at least {min_assets.get(stage['id'], 1)} assets")


def validate_scoring(data: dict[str, Any], schema: dict[str, Any], scoring_model: dict[str, Any]) -> None:
    scoring = require_list(data, "lead_scoring")
    required = set(schema["required_scoring_fields"])
    dimensions = set(scoring_model["dimensions"])
    max_points = int(scoring_model["max_points_per_rule"])
    for rule in scoring:
        if not isinstance(rule, dict):
            raise ValueError("each scoring rule must be an object")
        missing = required - set(rule)
        if missing:
            raise ValueError(f"scoring rule missing fields: {sorted(missing)}")
        if rule["dimension"] not in dimensions:
            raise ValueError(f"unsupported scoring dimension: {rule['dimension']}")
        points = rule["points"]
        if not isinstance(points, int) or points <= 0 or points > max_points:
            raise ValueError(f"points must be 1..{max_points} for {rule['name']}")


def validate_nurture(data: dict[str, Any], schema: dict[str, Any], nurture_schema: dict[str, Any]) -> None:
    paths = require_list(data, "nurture_paths")
    required = set(schema["required_nurture_fields"])
    allowed = set(nurture_schema["allowed_branches"])
    for path in paths:
        if not isinstance(path, dict):
            raise ValueError("each nurture path must be an object")
        missing = required - set(path)
        if missing:
            raise ValueError(f"nurture path missing fields: {sorted(missing)}")
        if path["branch"] not in allowed:
            raise ValueError(f"unsupported nurture branch for {path['id']}: {path['branch']}")


def validate_input(data: dict[str, Any], base: Path) -> None:
    schema = load_json(base / "assets" / "funnel-design-schema.json")
    validate_root(data, schema)
    validate_stages(data, schema, load_json(base / "assets" / "stage-content-model.json"))
    validate_scoring(data, schema, load_json(base / "assets" / "lead-scoring-model.json"))
    validate_nurture(data, schema, load_json(base / "assets" / "nurture-flow-schema.json"))


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def stage_table(stages: list[dict[str, Any]]) -> str:
    lines = [
        "| Stage | Intent | Core question | Content assets | CTA | Metric | Owner |",
        "|---|---|---|---|---|---|---|",
    ]
    for stage in stages:
        assets = "; ".join(stage["content_assets"])
        lines.append(
            f"| {stage['id'].upper()} | {stage['intent']} | {stage['core_question']} | {assets} | "
            f"{stage['cta']} | {stage['metric']} | {stage['owner']} |"
        )
    return "\n".join(lines)


def scoring_lines(scoring: list[dict[str, Any]], scoring_model: dict[str, Any]) -> str:
    thresholds = "; ".join(f"{item['state']}={item['min']}-{item['max']}" for item in scoring_model["thresholds"])
    lines = [f"- [CODE] Lifecycle thresholds: {thresholds}."]
    for rule in scoring:
        lines.append(f"- [CODE] {rule['name']}: +{rule['points']} ({rule['dimension']}; evidence: {rule['evidence']}).")
    return "\n".join(lines)


def nurture_lines(paths: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"- [CODE] `{path['id']}`: trigger `{path['trigger']}`, delay `{path['delay']}`, "
        f"message `{path['message']}`, branch `{path['branch']}`, exit `{path['exit']}`."
        for path in paths
    )


def handoff_lines(rules: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"- [CODE] MQL: score >= {rules['mql']['minimum_score']} owned by {rules['mql']['owner']}.",
            f"- [CODE] Sales-ready: score >= {rules['sales_ready']['minimum_score']} plus `{rules['sales_ready']['required_signal']}` owned by {rules['sales_ready']['owner']}.",
            f"- [CODE] Disqualify when: {', '.join(rules['disqualify_when'])}.",
            f"- [CODE] Reactivate when: {', '.join(rules['reactivate_when'])}.",
        ]
    )


def render(data: dict[str, Any], base: Path) -> str:
    template = (base / "assets" / "funnel-design-report-template.md").read_text(encoding="utf-8")
    scoring_model = load_json(base / "assets" / "lead-scoring-model.json")
    qualification = load_json(base / "assets" / "qualification-rules.json")
    validation = "\n".join(
        [
            "- [CODE] TOFU, MOFU, and BOFU stages are present.",
            "- [CODE] Every stage has content assets, CTA, metric, and owner.",
            "- [CODE] Lead scoring dimensions map to fit, intent, or engagement.",
            "- [CODE] Every nurture path has trigger, delay, branch, and exit.",
        ]
    )
    risks = "\n".join(
        [
            "- [INFERENCE] Funnel design does not prove campaign performance before launch.",
            "- [INFERENCE] Email and CRM execution still require consent and platform review.",
            "- [ASSUMPTION] Content inventory names are accepted as provided by the input.",
        ]
    )
    replacements = {
        "{{PRODUCT}}": str(data["product"]),
        "{{AUDIENCE}}": str(data["audience"]),
        "{{OFFER}}": str(data["offer"]),
        "{{GOAL}}": str(data["goal"]),
        "{{CONVERSION_EVENT}}": str(data["conversion_event"]),
        "{{SALES_MOTION}}": str(data["sales_motion"]),
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{STAGE_TABLE}}": stage_table(data["stages"]),
        "{{LEAD_SCORING}}": scoring_lines(data["lead_scoring"], scoring_model),
        "{{NURTURE_FLOW}}": nurture_lines(data["nurture_paths"]),
        "{{HANDOFF_RULES}}": handoff_lines(qualification),
        "{{VALIDATION}}": validation,
        "{{RISKS}}": risks,
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic funnel design report")
    parser.add_argument("--input", required=True, help="Structured funnel design JSON")
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
