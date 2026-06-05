#!/usr/bin/env python3
"""Compile a structured custom-agent spec into deterministic Markdown."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from string import Template


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def as_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field}: expected non-empty list")
    items = [str(item).strip() for item in value]
    if any(not item for item in items):
        raise ValueError(f"{field}: list items must be non-empty")
    return items


def require_section(data: dict, name: str) -> dict:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ValueError(f"{name}: section is required")
    return value


def require_text(section: dict, field: str, label: str | None = None) -> str:
    value = str(section.get(field, "")).strip()
    if not value:
        raise ValueError(f"{label or field}: required")
    return value


def bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))


def contains_negative_boundary(items: list[str]) -> bool:
    pattern = re.compile(r"\b(do not|never|must not|no modificar|no borrar)\b", re.I)
    return any(pattern.search(item) for item in items)


def validate_spec(spec: dict) -> None:
    schema = load_json(ASSETS_DIR / "agent-spec-schema.json")
    tools_policy = load_json(ASSETS_DIR / "tool-policy.json")
    model_policy = load_json(ASSETS_DIR / "model-selection-policy.json")
    trigger_policy = load_json(ASSETS_DIR / "description-trigger-policy.json")

    agent = require_section(spec, "agent")
    routing = require_section(spec, "routing")
    behavior = require_section(spec, "behavior")
    quality = require_section(spec, "quality")
    evidence = require_section(spec, "evidence")

    for section_name, section_schema in schema.items():
        if not isinstance(section_schema, dict) or "required" not in section_schema:
            continue
        section = require_section(spec, section_name)
        for field in section_schema["required"]:
            if field not in section:
                raise ValueError(f"{section_name}.{field}: required")

    name = require_text(agent, "name", "agent.name")
    name_pattern = str(schema["agent"]["name_pattern"])
    if not re.match(name_pattern, name):
        raise ValueError("agent.name: must be kebab-case and start with a letter")
    if name.lower() in set(schema["agent"]["reserved_names"]):
        raise ValueError(f"agent.name: reserved built-in collision: {name}")

    non_goals = as_list(agent.get("non_goals"), "agent.non_goals")
    if len(non_goals) < int(schema["agent"]["minimum_non_goals"]):
        raise ValueError("agent.non_goals: expected at least two non-goals")

    triggers = as_list(routing.get("triggers"), "routing.triggers")
    if len(triggers) < int(trigger_policy["minimum_trigger_phrases"]):
        raise ValueError("routing.triggers: expected at least two trigger phrases")
    negative_triggers = as_list(routing.get("negative_triggers"), "routing.negative_triggers")
    if len(negative_triggers) < int(trigger_policy["minimum_negative_triggers"]):
        raise ValueError("routing.negative_triggers: expected at least one negative trigger")

    destination = require_text(routing, "destination", "routing.destination")
    if destination not in schema["routing"]["destinations"]:
        raise ValueError("routing.destination: must be project or global")

    model = require_text(routing, "model", "routing.model")
    if model not in model_policy["models"]:
        raise ValueError("routing.model: must be haiku, sonnet, or opus")

    tools = as_list(routing.get("tools"), "routing.tools")
    allowed_tools = set(tools_policy["allowed_tools"])
    forbidden = {token.lower() for token in tools_policy["forbidden_tokens"]}
    for tool in tools:
        if tool.lower() in forbidden:
            raise ValueError(f"routing.tools: forbidden wildcard or inheritance token: {tool}")
        if tool not in allowed_tools:
            raise ValueError(f"routing.tools: unsupported tool: {tool}")

    process = as_list(behavior.get("process"), "behavior.process")
    if len(process) < int(schema["behavior"]["minimum_process_steps"]):
        raise ValueError("behavior.process: expected at least four concrete steps")
    constraints = as_list(behavior.get("constraints"), "behavior.constraints")
    if len(constraints) < int(schema["behavior"]["minimum_constraints"]):
        raise ValueError("behavior.constraints: expected at least two constraints")
    if schema["behavior"]["requires_negative_boundary"] and not contains_negative_boundary(constraints):
        raise ValueError("behavior.constraints: expected at least one do-not or never boundary")
    require_text(behavior, "task", "behavior.task")
    require_text(behavior, "output_format", "behavior.output_format")
    require_text(behavior, "reasoning_discipline", "behavior.reasoning_discipline")

    quality_bar = as_list(quality.get("quality_bar"), "quality.quality_bar")
    if len(quality_bar) < int(schema["quality"]["minimum_quality_items"]):
        raise ValueError("quality.quality_bar: expected at least three items")
    validation_checks = as_list(quality.get("validation_checks"), "quality.validation_checks")
    if len(validation_checks) < int(schema["quality"]["minimum_validation_checks"]):
        raise ValueError("quality.validation_checks: expected at least three checks")
    escalation = as_list(quality.get("escalation_triggers"), "quality.escalation_triggers")
    if len(escalation) < int(schema["quality"]["minimum_escalation_triggers"]):
        raise ValueError("quality.escalation_triggers: expected at least two triggers")
    as_list(quality.get("residual_risks"), "quality.residual_risks")

    tags = as_list(evidence.get("tags"), "evidence.tags")
    allowed_tags = set(schema["evidence"]["allowed_tags"])
    invalid_tags = sorted(set(tags) - allowed_tags)
    if invalid_tags:
        raise ValueError(f"evidence.tags: unsupported tags: {', '.join(invalid_tags)}")


def render_markdown(spec: dict) -> str:
    agent = spec["agent"]
    routing = spec["routing"]
    behavior = spec["behavior"]
    quality = spec["quality"]
    description = (
        "Spawn when "
        + ", ".join(routing["triggers"])
        + ". Do not spawn when "
        + "; ".join(routing["negative_triggers"])
        + "."
    )
    template = Template((ASSETS_DIR / "agent-template.md").read_text(encoding="utf-8"))
    body = template.safe_substitute(
        display_name=agent["display_name"],
        role=agent["role"],
        task=behavior["task"],
        scope=agent["scope"],
        non_goals=", ".join(agent["non_goals"]),
        process=numbered(behavior["process"]),
        output_format=behavior["output_format"],
        constraints=bullet(behavior["constraints"]),
        reasoning_discipline=behavior["reasoning_discipline"],
        quality_bar=bullet(quality["quality_bar"]),
        escalation_triggers=bullet(quality["escalation_triggers"]),
    )
    frontmatter = [
        "---",
        f"name: {agent['name']}",
        f"description: {json.dumps(description, ensure_ascii=True)}",
        f"model: {routing['model']}",
        f"color: {json.dumps(str(routing.get('color', '#64748B')), ensure_ascii=True)}",
        f"tools: {json.dumps(routing['tools'], ensure_ascii=True)}",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + body.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a Claude Code custom agent definition")
    parser.add_argument("--input", required=True, help="Path to agent spec JSON")
    parser.add_argument("--output", help="Optional output file")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        spec = load_json(Path(args.input))
        validate_spec(spec)
        output = (
            json.dumps(spec, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
            if args.format == "json"
            else render_markdown(spec)
        )
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
