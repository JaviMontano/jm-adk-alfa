#!/usr/bin/env python3
"""Compile a robust form engineering contract from a structured JSON spec."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def validate_spec(spec: dict[str, Any], policy: dict[str, Any]) -> None:
    for section in policy["required_sections"]:
        if section not in spec:
            raise ValueError(f"missing required section: {section}")
    if not NAME_RE.match(str(spec.get("name", ""))):
        raise ValueError("name must be snake_case")
    if not str(spec.get("title", "")).strip():
        raise ValueError("title is required")

    allowed_types = set(policy["allowed_field_types"])
    parity_keys = set(policy["validation_parity"]["required_rule_keys"])
    field_names: set[str] = set()
    for field in require_list(spec, "fields"):
        if not isinstance(field, dict):
            raise ValueError("each field must be an object")
        name = str(field.get("name", ""))
        if not NAME_RE.match(name):
            raise ValueError("field.name must be snake_case")
        if name in field_names:
            raise ValueError(f"duplicate field: {name}")
        field_names.add(name)
        if not str(field.get("label", "")).strip():
            raise ValueError(f"field.label is required: {name}")
        field_type = str(field.get("type", ""))
        if field_type not in allowed_types:
            raise ValueError(f"unsupported field type for {name}: {field_type}")
        rules = field.get("rules")
        if not isinstance(rules, list) or not rules:
            raise ValueError(f"field.rules must be non-empty: {name}")
        for rule in rules:
            if not isinstance(rule, dict):
                raise ValueError(f"field rule must be an object: {name}")
            missing = parity_keys - set(rule)
            if missing:
                raise ValueError(f"rule for {name} missing parity keys: {sorted(missing)}")
            if not rule.get("client") or not rule.get("server"):
                raise ValueError(f"rule for {name} must define client and server checks")
            if not str(rule.get("message", "")).strip():
                raise ValueError(f"rule for {name} must include an actionable message")
        if field_type == "file":
            upload = field.get("upload")
            if not isinstance(upload, dict):
                raise ValueError(f"file field requires upload object: {name}")
            missing = set(policy["file_upload"]["required_keys"]) - set(upload)
            if missing:
                raise ValueError(f"file upload for {name} missing keys: {sorted(missing)}")
            if not isinstance(upload.get("accept"), list) or not upload["accept"]:
                raise ValueError(f"file upload accept must be non-empty: {name}")
            if float(upload.get("max_mb", 0)) <= 0:
                raise ValueError(f"file upload max_mb must be positive: {name}")

    used_fields: set[str] = set()
    for step in require_list(spec, "steps"):
        if not isinstance(step, dict):
            raise ValueError("each step must be an object")
        if not NAME_RE.match(str(step.get("id", ""))):
            raise ValueError("step.id must be snake_case")
        fields = step.get("fields")
        if not isinstance(fields, list) or not fields:
            raise ValueError(f"step.fields must be non-empty: {step.get('id')}")
        for name in fields:
            if name not in field_names:
                raise ValueError(f"step references unknown field: {name}")
            if name in used_fields:
                raise ValueError(f"field appears in multiple steps: {name}")
            used_fields.add(str(name))
    missing_from_steps = field_names - used_fields
    if missing_from_steps:
        raise ValueError(f"fields missing from steps: {sorted(missing_from_steps)}")

    accessibility = require_object(spec, "accessibility")
    missing_a11y = set(policy["accessibility"]["required_keys"]) - set(accessibility)
    if missing_a11y:
        raise ValueError(f"accessibility missing keys: {sorted(missing_a11y)}")
    if not all(bool(accessibility.get(key)) for key in policy["accessibility"]["required_keys"]):
        raise ValueError("accessibility keys must be truthy")

    optimistic = require_object(spec, "optimistic_submission")
    missing_optimistic = set(policy["optimistic_submission"]["required_keys"]) - set(optimistic)
    if missing_optimistic:
        raise ValueError(f"optimistic_submission missing keys: {sorted(missing_optimistic)}")
    if optimistic.get("retry_strategy") not in policy["optimistic_submission"]["retry_strategies"]:
        raise ValueError("optimistic_submission.retry_strategy is unsupported")

    errors = require_object(spec, "errors")
    for key in ["field", "summary", "server", "network"]:
        if not str(errors.get(key, "")).strip():
            raise ValueError(f"errors.{key} is required")

    submission = require_object(spec, "submission")
    for key in ["endpoint", "method", "server_validation", "idempotency"]:
        if not str(submission.get(key, "")).strip():
            raise ValueError(f"submission.{key} is required")


def render_markdown(spec: dict[str, Any], patterns: dict[str, Any], base: Path) -> str:
    lines: list[str] = []
    lines.append(f"# {spec['title']} Form Engineering Contract")
    lines.append("")
    lines.append("## Validation Parity")
    for field in spec["fields"]:
        lines.append(f"- `{field['name']}` ({field['type']}): {field['label']}")
        for rule in field["rules"]:
            lines.append(f"  - Client: {rule['client']}")
            lines.append(f"  - Server: {rule['server']}")
            lines.append(f"  - Message: {rule['message']}")
        if field["type"] == "file":
            upload = field["upload"]
            lines.append(
                "  - Upload: accept "
                + ", ".join(upload["accept"])
                + f"; max {upload['max_mb']} MB; storage {upload['storage_boundary']}"
            )
    lines.append("")
    lines.append("## Flow")
    for index, step in enumerate(spec["steps"], start=1):
        lines.append(f"{index}. `{step['id']}`: {', '.join(step['fields'])}")
    lines.append("")
    lines.append("## Error System")
    error_patterns = patterns["patterns"]
    lines.append(f"- Field errors: {spec['errors']['field']}")
    lines.append(f"- Summary: {spec['errors']['summary']} (pattern: {error_patterns['summary']})")
    lines.append(f"- Server: {spec['errors']['server']}")
    lines.append(f"- Network: {spec['errors']['network']}")
    lines.append("")
    lines.append("## Accessibility Hooks")
    for key, value in spec["accessibility"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Optimistic Submission")
    optimistic = spec["optimistic_submission"]
    lines.append(f"- Pending label: {optimistic['pending_label']}")
    lines.append(f"- Success message: {optimistic['success_message']}")
    lines.append(f"- Failure message: {optimistic['failure_message']}")
    lines.append(f"- Retry strategy: {optimistic['retry_strategy']}")
    lines.append("")
    lines.append("## Asset Hooks")
    lines.append("- `assets/optimistic-submit-template.ts` for submit state implementation.")
    lines.append("- `assets/upload-control-template.html` for accessible upload controls.")
    lines.append(f"- Asset base: `{base}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic form engineering contract")
    parser.add_argument("--spec", required=True, help="Structured form engineering JSON spec")
    parser.add_argument("--output", help="Write contract Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        spec = load_json(Path(args.spec))
        policy = load_json(base / "assets" / "form-engineering-policy.json")
        patterns = load_json(base / "assets" / "error-message-patterns.json")
        validate_spec(spec, policy)
        output = render_markdown(spec, patterns, base)
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
