#!/usr/bin/env python3
"""Compile deterministic Claude Code custom tooling extension plans."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_required_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        require(field in obj and obj[field] not in ("", None), f"{label} missing required field: {field}", errors)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(flatten_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(flatten_strings(item))
        return strings
    return []


def validate_artifact(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    artifact = as_dict(spec.get("artifact"))
    validate_required_fields(artifact, schema["requiredArtifactFields"], "artifact", errors)
    artifact_type = str(artifact.get("type", ""))
    trigger = str(artifact.get("trigger", ""))
    path = str(artifact.get("path", ""))
    require(artifact_type in policy["artifact"]["allowedTypes"], "artifact.type unsupported", errors)
    require(trigger in {"explicit", "contextual"}, "artifact.trigger must be explicit or contextual", errors)
    if trigger == "explicit":
        require(artifact_type == policy["artifact"]["explicitTriggerType"], "explicit trigger requires slash_command", errors)
        require(path.startswith(policy["artifact"]["commandPathPrefix"]) and path.endswith(".md"), "slash_command path must be .claude/commands/*.md", errors)
    if trigger == "contextual":
        require(artifact_type == policy["artifact"]["contextualTriggerType"], "contextual trigger requires skill", errors)
        require(path.startswith(policy["artifact"]["skillPathPrefix"]) and path.endswith(policy["artifact"]["skillPathSuffix"]), "skill path must be .claude/skills/<name>/SKILL.md", errors)


def validate_scope(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    scope = as_dict(spec.get("scope"))
    validate_required_fields(scope, schema["requiredScopeFields"], "scope", errors)
    scope_type = str(scope.get("type", ""))
    replicates = scope.get("replicatesToTeam")
    require(scope_type in {policy["scope"]["teamScope"], policy["scope"]["personalScope"]}, "scope.type unsupported", errors)
    if replicates is True:
        require(scope_type == policy["scope"]["teamScope"], "team-replicated artifacts require project scope", errors)


def validate_interface(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    interface = as_dict(spec.get("interface"))
    validate_required_fields(interface, schema["requiredInterfaceFields"], "interface", errors)
    require(len(str(interface.get("description", "")).strip()) >= 40, "interface.description must be routing-grade", errors)
    require(nonempty(interface.get("argumentHint")), "interface.argumentHint must be non-empty", errors)


def validate_security(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    security = as_dict(spec.get("security"))
    validate_required_fields(security, schema["requiredSecurityFields"], "security", errors)
    tools = [str(item) for item in as_list(security.get("allowedTools"))]
    require(bool(tools), "security.allowedTools must be non-empty", errors)
    blocked = sorted(set(tools).intersection(set(policy["tools"]["blocked"])))
    require(not blocked, f"blocked tool(s) declared: {', '.join(blocked)}", errors)
    allowed = set(policy["tools"]["readOnly"]).union(set(policy["tools"]["allowedWithJustification"]))
    unknown = sorted(set(tools) - allowed)
    require(not unknown, f"unknown tool(s): {', '.join(unknown)}", errors)
    if "Bash" in tools:
        require(nonempty(security.get("bashJustification")), "Bash requires explicit read-only or mutation justification", errors)
    if security.get("mutates") is False:
        require(all(tool in allowed for tool in tools), "read-only extension must use explicit minimal tools", errors)


def validate_context(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    context = as_dict(spec.get("context"))
    artifact = as_dict(spec.get("artifact"))
    validate_required_fields(context, schema["requiredContextFields"], "context", errors)
    if artifact.get("type") == "skill":
        require(context.get("fork") is True, "non-trivial skill requires context.fork true", errors)
        require(nonempty(context.get("reason")), "context.reason must explain fork usage", errors)


def validate_conventions(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    conventions = as_dict(spec.get("conventions"))
    validate_required_fields(conventions, schema["requiredConventionsFields"], "conventions", errors)
    require(conventions.get("permanentRulesInClaudeMd") is True, "permanent rules must stay in CLAUDE.md", errors)
    require(conventions.get("skillContainsOnlyConditionalCapability") is True, "skill must contain only conditional capability", errors)


def validate_validation(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    validation = as_dict(spec.get("validation"))
    validate_required_fields(validation, schema["requiredValidationFields"], "validation", errors)
    for field in schema["requiredValidationFields"]:
        require(validation.get(field) is True, f"validation.{field} must be true", errors)


def validate_antipatterns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    joined = "\n".join(flatten_strings(spec)).lower()
    for token in policy["blockedAntiPatterns"]:
        if token in joined:
            errors.append(f"blocked anti-pattern token present: {token}")


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "extension-schema.json")
    policy = load_json(ASSET_DIR / "extension-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "extension", errors)
    if errors:
        raise ValueError("\n".join(errors))
    require(bool(re.match(r"^[a-z0-9][a-z0-9-]*$", str(spec.get("name", "")))), "name must be slug-like", errors)
    require(nonempty(spec.get("intent")), "intent must be non-empty", errors)
    validate_artifact(spec, schema, policy, errors)
    validate_scope(spec, schema, policy, errors)
    validate_interface(spec, schema, errors)
    validate_security(spec, schema, policy, errors)
    validate_context(spec, schema, errors)
    validate_conventions(spec, schema, errors)
    validate_validation(spec, schema, errors)
    require(bool(as_list(spec.get("risks"))), "risks requires at least one item", errors)
    validate_antipatterns(spec, policy, errors)
    if errors:
        raise ValueError("\n".join(errors))


def render_frontmatter(spec: dict[str, Any]) -> str:
    artifact = spec["artifact"]
    interface = spec["interface"]
    security = spec["security"]
    lines = [
        "---",
        f"name: {spec['name']}",
        f"description: \"{interface['description']}\"",
    ]
    if artifact["type"] == "skill":
        lines.append("context: fork")
    lines.append(f"argument-hint: \"{interface['argumentHint']}\"")
    lines.append("allowed-tools:")
    for tool in security["allowedTools"]:
        lines.append(f"  - {tool}")
    lines.append("---")
    return "\n".join(lines)


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_report(spec: dict[str, Any]) -> str:
    template = (ASSET_DIR / "extension-report-template.md").read_text(encoding="utf-8")
    return template.format(
        name=spec["name"],
        artifactType=spec["artifact"]["type"],
        trigger=spec["artifact"]["trigger"],
        scopeType=spec["scope"]["type"],
        path=spec["artifact"]["path"],
        contextFork=spec["context"]["fork"],
        mutates=spec["security"]["mutates"],
        description=spec["interface"]["description"],
        argumentHint=spec["interface"]["argumentHint"],
        allowedTools=", ".join(spec["security"]["allowedTools"]),
        bashJustification=spec["security"]["bashJustification"] or "not needed",
        frontmatter=render_frontmatter(spec),
        risksMarkdown=bullet_list(spec["risks"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a Claude Code custom tooling extension plan")
    parser.add_argument("input", type=Path, help="Path to extension JSON spec")
    parser.add_argument("--output", type=Path, help="Write generated report")
    args = parser.parse_args()
    try:
        spec = load_json(args.input)
        validate(spec)
        report = render_report(spec)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
