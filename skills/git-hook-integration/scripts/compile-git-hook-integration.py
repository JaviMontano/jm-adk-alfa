#!/usr/bin/env python3
"""Compile a deterministic Git hook integration plan from structured JSON."""

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


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def validate_required(data: dict[str, Any], required: list[str], label: str) -> None:
    missing = [field for field in required if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def validate_input(data: dict[str, Any], schema: dict[str, Any]) -> None:
    validate_required(data, schema["required_root_fields"], "root")
    if data["hook_manager"] not in schema["allowed_hook_managers"]:
        raise ValueError(f"unsupported hook_manager: {data['hook_manager']}")
    if data["install_mode"] not in schema["allowed_install_modes"]:
        raise ValueError(f"unsupported install_mode: {data['install_mode']}")

    hooks = require_list(data, "hooks")
    seen_stages = set()
    for hook in hooks:
        if not isinstance(hook, dict):
            raise ValueError("each hook must be an object")
        validate_required(hook, schema["required_hook_fields"], "hook")
        if hook["stage"] not in schema["allowed_hook_stages"]:
            raise ValueError(f"unsupported hook stage: {hook['stage']}")
        if not isinstance(hook["blocking"], bool):
            raise ValueError(f"hook.blocking must be boolean for {hook['name']}")
        seen_stages.add(hook["stage"])
    required_stages = set(schema["allowed_hook_stages"])
    missing_stages = required_stages - seen_stages
    if missing_stages:
        raise ValueError(f"hooks missing required stages: {sorted(missing_stages)}")

    commit_policy = require_object(data, "conventional_commits")
    validate_required(commit_policy, schema["required_commit_policy_fields"], "conventional_commits")
    if not isinstance(commit_policy["enabled"], bool):
        raise ValueError("conventional_commits.enabled must be boolean")
    if commit_policy["enabled"] and "commit-msg" not in seen_stages:
        raise ValueError("conventional commits require a commit-msg hook")
    if not isinstance(commit_policy["max_header_length"], int) or commit_policy["max_header_length"] < 1:
        raise ValueError("conventional_commits.max_header_length must be a positive integer")

    for command in require_list(data, "validation_commands"):
        if not isinstance(command, dict):
            raise ValueError("each validation command must be an object")
        validate_required(command, schema["required_validation_fields"], "validation_command")
        if command["stage"] not in schema["allowed_hook_stages"]:
            raise ValueError(f"unsupported validation command stage: {command['stage']}")
        if not isinstance(command["required"], bool):
            raise ValueError(f"validation_command.required must be boolean for {command['name']}")

    evidence = require_object(data, "evidence")
    validate_required(evidence, schema["required_evidence_fields"], "evidence")


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def hook_matrix(data: dict[str, Any], stage_model: dict[str, Any]) -> str:
    stage_order = [stage["stage"] for stage in stage_model["stages"]]
    hooks = sorted(data["hooks"], key=lambda hook: (stage_order.index(hook["stage"]), hook["name"]))
    lines = [
        "| Stage | Hook | Blocking | Command | Purpose |",
        "|---|---|---|---|---|",
    ]
    for hook in hooks:
        lines.append(
            f"| {hook['stage']} | {hook['name']} | {hook['blocking']} | `{hook['command']}` | {hook['purpose']} |"
        )
    return "\n".join(lines)


def commit_policy_lines(data: dict[str, Any], default_policy: dict[str, Any]) -> str:
    policy = data["conventional_commits"]
    types = policy["types"] if policy.get("types") else default_policy["types"]
    scopes = policy.get("scopes", [])
    examples = "; ".join(default_policy["examples"])
    return "\n".join(
        [
            f"- [CODE] Enabled: {policy['enabled']}.",
            f"- [CODE] Allowed types: {', '.join(types)}.",
            f"- [CODE] Allowed scopes: {', '.join(scopes) if scopes else 'not restricted'}.",
            f"- [CODE] Max header length: {policy['max_header_length']}.",
            f"- [CODE] Header regex: `{default_policy['header_regex']}`.",
            f"- [CODE] Examples: {examples}.",
        ]
    )


def validation_command_table(data: dict[str, Any]) -> str:
    lines = [
        "| Name | Stage | Required | Command |",
        "|---|---|---|---|",
    ]
    for command in sorted(data["validation_commands"], key=lambda item: (item["stage"], item["name"])):
        lines.append(
            f"| {command['name']} | {command['stage']} | {command['required']} | `{command['command']}` |"
        )
    return "\n".join(lines)


def installation_plan(data: dict[str, Any], install_model: dict[str, Any]) -> str:
    manager = data["hook_manager"]
    strategy = next(item for item in install_model["strategies"] if item["manager"] == manager)
    guardrails = "\n".join(f"- [CODE] {rule}" for rule in install_model["guardrails"])
    return "\n".join(
        [
            f"- [CODE] Strategy: {strategy['manager']} — {strategy['best_for']}.",
            f"- [CODE] Install command: `{strategy['install_command']}`.",
            f"- [CODE] Requested mode: {data['install_mode']}.",
            "",
            "### Guardrails",
            guardrails,
        ]
    )


def validation_lines(data: dict[str, Any]) -> str:
    required = {"pre-commit", "commit-msg", "pre-push"}
    present = {hook["stage"] for hook in data["hooks"]}
    return "\n".join(
        [
            f"- [CODE] Required hook stages present: {', '.join(sorted(required & present))}.",
            "- [CODE] Conventional Commit policy is backed by a commit-msg hook.",
            "- [CODE] Validation commands map to declared hook stages.",
            "- [CODE] Installation mode is explicit and non-destructive by default.",
            "- [CODE] Hook commands are rendered as plan output; this script does not install hooks.",
        ]
    )


def risk_lines(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "- [INFERENCE] Hook plans still require repository-specific review before installation.",
            "- [INFERENCE] Developers can bypass Git hooks with --no-verify unless server-side protection exists.",
            "- [ASSUMPTION] Commands supplied in input are trusted project-local validation commands.",
        ]
    )


def render(data: dict[str, Any], base: Path) -> str:
    stage_model = load_json(base / "assets" / "hook-stage-model.json")
    commit_policy = load_json(base / "assets" / "conventional-commit-policy.json")
    install_model = load_json(base / "assets" / "install-strategy-model.json")
    template = (base / "assets" / "git-hook-integration-template.md").read_text(encoding="utf-8")
    replacements = {
        "{{REPO_NAME}}": str(data["repo_name"]),
        "{{HOOK_MANAGER}}": str(data["hook_manager"]),
        "{{INSTALL_MODE}}": str(data["install_mode"]),
        "{{HOOK_DIRECTORY}}": str(data["hook_directory"]),
        "{{CONVENTIONAL_STATUS}}": "enabled" if data["conventional_commits"]["enabled"] else "disabled",
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{HOOK_MATRIX}}": hook_matrix(data, stage_model),
        "{{COMMIT_POLICY}}": commit_policy_lines(data, commit_policy),
        "{{VALIDATION_COMMANDS}}": validation_command_table(data),
        "{{INSTALLATION_PLAN}}": installation_plan(data, install_model),
        "{{VALIDATION}}": validation_lines(data),
        "{{RISKS}}": risk_lines(data),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic Git hook integration plan")
    parser.add_argument("--input", required=True, help="Structured Git hook integration JSON")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        data = load_json(Path(args.input))
        schema = load_json(base / "assets" / "git-hook-integration-schema.json")
        validate_input(data, schema)
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
