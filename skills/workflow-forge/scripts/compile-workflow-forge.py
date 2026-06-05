#!/usr/bin/env python3
"""Compile and validate Workflow Forge specs.

This script is intentionally offline and deterministic. It reads a local JSON
spec, applies local assets/workflow-policy.json, and emits Markdown or JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_policy() -> dict[str, Any]:
    return load_json(skill_dir() / "assets" / "workflow-policy.json")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def non_empty_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def contains_prohibited_stack(spec: dict[str, Any], prohibited_terms: list[str]) -> list[str]:
    text = json.dumps(spec, ensure_ascii=False)
    found: list[str] = []
    for term in prohibited_terms:
        if re.search(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE):
            found.append(term)
    return sorted(set(found), key=str.lower)


def validate_spec(spec: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "workflow_id",
        "title",
        "command",
        "description",
        "deliverable",
        "skills_involved",
        "agents_coordinated",
        "phases",
        "quality_gates",
        "example_dialogue",
    ]
    for field in required:
        if field not in spec:
            errors.append(f"missing required field: {field}")

    workflow_id = str(spec.get("workflow_id", ""))
    if workflow_id and not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", workflow_id):
        errors.append("workflow_id must be kebab-case")

    command = str(spec.get("command", ""))
    if command and not command.startswith("/"):
        errors.append("command must start with /")

    if "skills_involved" in spec and not non_empty_strings(spec.get("skills_involved")):
        errors.append("skills_involved must be a non-empty list of strings")
    if "agents_coordinated" in spec and not non_empty_strings(spec.get("agents_coordinated")):
        errors.append("agents_coordinated must be a non-empty list of strings")
    if "quality_gates" in spec and not non_empty_strings(spec.get("quality_gates")):
        errors.append("quality_gates must be a non-empty list of strings")

    phases = as_list(spec.get("phases"))
    min_phases = int(policy.get("min_phases", 2))
    if len(phases) < min_phases:
        errors.append(f"workflow must have at least {min_phases} phases")

    phase_required = as_list(policy.get("phase_required_fields"))
    for index, phase in enumerate(phases, start=1):
        if not isinstance(phase, dict):
            errors.append(f"phase {index} must be an object")
            continue
        for field in phase_required:
            if field not in phase:
                errors.append(f"phase {index} missing required field: {field}")
        for list_field in ["agents", "inputs", "outputs", "checkpoint"]:
            if list_field in phase and not non_empty_strings(phase.get(list_field)):
                errors.append(f"phase {index} {list_field} must be a non-empty list of strings")

    if phases and isinstance(phases[0], dict):
        first_kind = str(phases[0].get("kind", "")).lower()
        allowed = [str(kind).lower() for kind in as_list(policy.get("allowed_first_phase_kinds"))]
        if first_kind not in allowed:
            errors.append(f"first phase kind must be one of: {', '.join(allowed)}")

    if phases and isinstance(phases[-1], dict):
        final_kind = str(phases[-1].get("kind", "")).lower()
        required_final = str(policy.get("required_final_phase_kind", "verification")).lower()
        if final_kind != required_final:
            errors.append(f"final phase kind must be {required_final}")

    declared_agents = {str(agent) for agent in as_list(spec.get("agents_coordinated"))}
    for phase in phases:
        if isinstance(phase, dict):
            for agent in as_list(phase.get("agents")):
                if str(agent) not in declared_agents:
                    phase_id = phase.get("id", "?")
                    errors.append(f"phase {phase_id} references undeclared agent: {agent}")

    dialogue = as_list(spec.get("example_dialogue"))
    if dialogue:
        for index, turn in enumerate(dialogue, start=1):
            if not isinstance(turn, dict) or not str(turn.get("user", "")).strip() or not str(turn.get("assistant", "")).strip():
                errors.append(f"example_dialogue turn {index} must include user and assistant")
    elif "example_dialogue" in spec:
        errors.append("example_dialogue must be a non-empty list")

    prohibited = contains_prohibited_stack(spec, [str(term) for term in as_list(policy.get("prohibited_stack_terms"))])
    if prohibited:
        errors.append(f"prohibited stack reference: {', '.join(prohibited)}")

    return errors


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def simple_list(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_phase_map(phases: list[dict[str, Any]]) -> str:
    rows = ["| # | Phase | Kind | Agents | Output | Checkpoint |", "|---:|---|---|---|---|---|"]
    for index, phase in enumerate(phases, start=1):
        agents = ", ".join(as_list(phase.get("agents")))
        outputs = "; ".join(as_list(phase.get("outputs")))
        checkpoint = "; ".join(as_list(phase.get("checkpoint")))
        rows.append(
            f"| {index} | {phase.get('title', '')} | {phase.get('kind', '')} | {agents} | {outputs} | {checkpoint} |"
        )
    return "\n".join(rows)


def render_checkpoints(phases: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for phase in phases:
        lines.append(f"- **{phase.get('title', '')}:** {'; '.join(as_list(phase.get('checkpoint')))}")
    return "\n".join(lines)


def render_dialogue(dialogue: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for turn in dialogue:
        lines.append(f"- User: {turn.get('user', '')}")
        lines.append(f"- Assistant: {turn.get('assistant', '')}")
    return "\n".join(lines)


def build_output(spec: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    phases = [phase for phase in as_list(spec.get("phases")) if isinstance(phase, dict)]
    validation = {
        "valid": not errors,
        "errors": errors,
        "phase_count": len(phases),
    }
    return {
        "frontmatter": {
            "description": spec.get("description", ""),
            "command": spec.get("command", ""),
            "skills_involved": as_list(spec.get("skills_involved")),
            "agents_coordinated": as_list(spec.get("agents_coordinated")),
        },
        "phase_map": phases,
        "checkpoints": [
            {"phase": phase.get("id", ""), "checkpoint": as_list(phase.get("checkpoint"))}
            for phase in phases
        ],
        "quality_gates": as_list(spec.get("quality_gates")),
        "failure_handling": as_list(spec.get("failure_handling")),
        "example_dialogue": as_list(spec.get("example_dialogue")),
        "validation": validation,
    }


def render_markdown(spec: dict[str, Any], output: dict[str, Any]) -> str:
    template = (skill_dir() / "assets" / "workflow-output-template.md").read_text(encoding="utf-8")
    phases = [phase for phase in as_list(spec.get("phases")) if isinstance(phase, dict)]
    summary = (
        f"`{spec.get('command', '')}` produces {spec.get('deliverable', '')} "
        f"through {len(phases)} phases."
    )
    validation = output["validation"]
    validation_lines = [
        f"- valid: {str(validation['valid']).lower()}",
        f"- phase_count: {validation['phase_count']}",
    ]
    for error in validation["errors"]:
        validation_lines.append(f"- error: {error}")
    if not validation["errors"]:
        validation_lines.append("- errors: none")

    return template.format(
        title=spec.get("title", ""),
        summary=summary,
        description=spec.get("description", ""),
        command=spec.get("command", ""),
        skills_involved=bullet_list(as_list(spec.get("skills_involved"))),
        agents_coordinated=bullet_list(as_list(spec.get("agents_coordinated"))),
        phase_map=render_phase_map(phases),
        checkpoints=render_checkpoints(phases),
        quality_gates=simple_list(as_list(spec.get("quality_gates"))),
        failure_handling=simple_list(as_list(spec.get("failure_handling"))) or "- None declared",
        example_dialogue=render_dialogue(as_list(spec.get("example_dialogue"))),
        validation="\n".join(validation_lines),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a Workflow Forge JSON spec")
    parser.add_argument("--input", required=True, help="Path to workflow spec JSON")
    parser.add_argument("--output", help="Optional output path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    input_path = Path(args.input)
    spec = load_json(input_path)
    if not isinstance(spec, dict):
        print("workflow spec root must be an object", file=sys.stderr)
        return 1

    policy = load_policy()
    errors = validate_spec(spec, policy)
    output = build_output(spec, errors)

    if args.format == "json":
        rendered = json.dumps(output, indent=2, ensure_ascii=False) + "\n"
    else:
        rendered = render_markdown(spec, output)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
