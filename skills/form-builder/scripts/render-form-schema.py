#!/usr/bin/env python3
"""Render semantic form HTML from a structured form schema."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("schema must be a JSON object")
    return data


def load_policy(base: Path) -> dict[str, object]:
    data = load_json(base / "assets" / "validation-policy.json")
    return data


def validate_schema(schema: dict[str, object], policy: dict[str, object]) -> None:
    if not str(schema.get("title", "")).strip():
        raise ValueError("schema.title is required")
    steps = schema.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError("schema.steps must be a non-empty list")
    allowed = set(policy.get("allowed_field_types", []))
    seen_fields: set[str] = set()
    for step in steps:
        if not isinstance(step, dict):
            raise ValueError("each step must be an object")
        if not NAME_RE.match(str(step.get("id", ""))):
            raise ValueError("step.id must be snake_case")
        if not str(step.get("title", "")).strip():
            raise ValueError("step.title is required")
        fields = step.get("fields")
        if not isinstance(fields, list) or not fields:
            raise ValueError(f"step {step.get('id')} must contain fields")
        for field in fields:
            if not isinstance(field, dict):
                raise ValueError("each field must be an object")
            name = str(field.get("name", ""))
            if not NAME_RE.match(name):
                raise ValueError("field.name must be snake_case")
            if name in seen_fields:
                raise ValueError(f"duplicate field name: {name}")
            seen_fields.add(name)
            field_type = str(field.get("type", ""))
            if field_type not in allowed:
                raise ValueError(f"unsupported field type for {name}: {field_type}")
            if not str(field.get("label", "")).strip():
                raise ValueError(f"field.label is required for {name}")
            if field_type == "select" and not field.get("options"):
                raise ValueError(f"select field requires options: {name}")
            show_if = field.get("show_if")
            if show_if is not None:
                if not isinstance(show_if, dict):
                    raise ValueError(f"show_if must be an object for {name}")
                driver = str(show_if.get("field", ""))
                if driver not in seen_fields:
                    raise ValueError(f"show_if driver must appear before {name}: {driver}")
                if "equals" not in show_if:
                    raise ValueError(f"show_if.equals is required for {name}")


def field_html(field: dict[str, object]) -> str:
    name = html.escape(str(field["name"]), quote=True)
    label = html.escape(str(field["label"]))
    field_type = str(field["type"])
    required = bool(field.get("required", False))
    hint = str(field.get("hint", "")).strip()
    describedby = f' aria-describedby="{name}_hint"' if hint else ""
    required_attr = " required" if required else ""
    required_mark = ' <span class="required">*</span>' if required else ""
    conditional = ""
    show_if = field.get("show_if")
    if isinstance(show_if, dict):
        conditional = (
            f' data-show-if="{html.escape(str(show_if["field"]), quote=True)}"'
            f' data-show-equals="{html.escape(str(show_if["equals"]), quote=True)}"'
        )

    control = ""
    if field_type == "textarea":
        control = f'<textarea id="{name}" name="{name}"{required_attr}{describedby}></textarea>'
    elif field_type == "select":
        options = []
        for option in field.get("options", []):  # type: ignore[union-attr]
            value = html.escape(str(option.get("value", "")), quote=True) if isinstance(option, dict) else html.escape(str(option), quote=True)
            text = html.escape(str(option.get("label", value))) if isinstance(option, dict) else html.escape(str(option))
            options.append(f'<option value="{value}">{text}</option>')
        control = f'<select id="{name}" name="{name}"{required_attr}{describedby}>' + "".join(options) + "</select>"
    elif field_type == "checkbox":
        control = f'<input id="{name}" name="{name}" type="checkbox"{required_attr}{describedby}>'
    else:
        input_type = html.escape(field_type, quote=True)
        autocomplete = html.escape(str(field.get("autocomplete", "")), quote=True)
        autocomplete_attr = f' autocomplete="{autocomplete}"' if autocomplete else ""
        control = f'<input id="{name}" name="{name}" type="{input_type}"{required_attr}{describedby}{autocomplete_attr}>'

    hint_html = f'<div id="{name}_hint" class="hint">{html.escape(hint)}</div>' if hint else ""
    return f'<div class="field"{conditional}><label for="{name}">{label}{required_mark}</label>{control}{hint_html}</div>'


def render(schema: dict[str, object], base: Path) -> str:
    css = (base / "assets" / "form-control.css").read_text(encoding="utf-8")
    step_template = (base / "assets" / "form-step-template.html").read_text(encoding="utf-8")
    parts = []
    for step in schema["steps"]:  # type: ignore[index]
        fields = "\n".join(field_html(field) for field in step["fields"])  # type: ignore[index]
        rendered_step = (
            step_template.replace("{{STEP_ID}}", html.escape(str(step["id"]), quote=True))
            .replace("{{STEP_TITLE}}", html.escape(str(step["title"])))
            .replace("{{FIELDS}}", fields)
        )
        parts.append(rendered_step)
    submit_label = html.escape(str(schema.get("submit_label", "Submit")))
    title = html.escape(str(schema["title"]))
    return (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">\n"
        f"<title>{title}</title>\n<style>\n{css}\n</style>\n</head>\n<body>\n"
        f"<form class=\"form-shell\" method=\"post\" novalidate>\n<h1>{title}</h1>\n"
        + "\n".join(parts)
        + f"\n<div class=\"actions\"><button type=\"submit\">{submit_label}</button></div>\n"
        "</form>\n</body>\n</html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render semantic form HTML from JSON schema")
    parser.add_argument("--schema", required=True, help="Form schema JSON")
    parser.add_argument("--output", help="Write HTML to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    schema = load_json(Path(args.schema))
    policy = load_policy(base)
    validate_schema(schema, policy)
    output = render(schema, base)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
