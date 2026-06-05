#!/usr/bin/env python3
"""Validate deterministic prompt artifacts produced by prompt-creator."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "type",
    "owningAgent",
    "sourceAgentMd",
    "version",
    "createdBy",
    "validationStatus",
}
HANDLED_TYPES = {
    "meta_prompt",
    "system_user_pair",
    "handoff_prompt",
    "committee_deliberation",
    "committee_synthesis",
    "validation_prompt",
    "fallback_prompt",
}
REQUIRED_SECTIONS = {
    "Purpose",
    "Inputs",
    "Output Contract",
    "Validation Gate",
    "Failure Handling",
    "Downstream Boundary",
}
GENERIC_PLACEHOLDERS = {"x", "var", "value", "thing", "placeholder"}


def load_text(args: argparse.Namespace) -> str:
    if args.fixture:
        data = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        artifact = data.get("artifact")
        if not isinstance(artifact, str):
            raise ValueError(f"{args.fixture}: fixture must contain string field 'artifact'")
        return artifact
    if not args.path:
        raise ValueError("provide a prompt path or --fixture")
    return Path(args.path).read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, ["frontmatter must start at first line"]
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, text, ["frontmatter closing marker missing"]

    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            errors.append(f"invalid frontmatter line: {raw}")
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    body = "\n".join(lines[end + 1 :])
    return meta, body, errors


def headings(body: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^##\s+(.+)$", body, re.MULTILINE)}


def validate_placeholders(text: str) -> list[str]:
    errors: list[str] = []
    for placeholder in re.findall(r"\{\{([^{}]+)\}\}", text):
        name = placeholder.strip()
        if name in GENERIC_PLACEHOLDERS:
            errors.append(f"generic placeholder: {{{{{name}}}}}")
        if not re.fullmatch(r"[a-z][a-z0-9_]{2,}", name):
            errors.append(f"placeholder must be descriptive snake_case: {{{{{name}}}}}")
    return errors


def validate_type_specific(prompt_type: str, body: str, present: set[str]) -> list[str]:
    errors: list[str] = []
    lower = body.lower()
    if prompt_type == "meta_prompt":
        for section in {"Framework", "Constraints"} - present:
            errors.append(f"missing meta_prompt section: {section}")
    elif prompt_type == "system_user_pair":
        for section in {"System", "User"} - present:
            errors.append(f"missing system_user_pair section: {section}")
    elif prompt_type == "handoff_prompt":
        for section in {"Context to Pass", "Context to Omit", "Success Criteria"} - present:
            errors.append(f"missing handoff_prompt section: {section}")
    elif prompt_type == "committee_deliberation":
        for section in {"Independent Evaluation", "Rubric"} - present:
            errors.append(f"missing committee_deliberation section: {section}")
        if "independent" not in lower:
            errors.append("committee_deliberation must require independent first-pass evaluation")
    elif prompt_type == "committee_synthesis":
        for section in {"Redundancy Removal", "Conflict Resolution", "Confidence Weighting"} - present:
            errors.append(f"missing committee_synthesis section: {section}")
    elif prompt_type == "validation_prompt":
        for section in {"Severity Levels"} - present:
            errors.append(f"missing validation_prompt section: {section}")
        for level in ["critical", "major", "minor"]:
            if level not in lower:
                errors.append(f"validation_prompt missing severity level: {level}")
    elif prompt_type == "fallback_prompt":
        for section in {"Trigger Conditions", "Preservation Priorities", "User Communication", "Escalation Path"} - present:
            errors.append(f"missing fallback_prompt section: {section}")
    return errors


def validate(text: str) -> list[str]:
    meta, body, errors = parse_frontmatter(text)
    missing = sorted(REQUIRED_FRONTMATTER - set(meta))
    if missing:
        errors.append(f"missing frontmatter fields: {', '.join(missing)}")

    prompt_type = meta.get("type", "")
    if prompt_type not in HANDLED_TYPES:
        errors.append(f"unsupported generated prompt type: {prompt_type}")
    if meta.get("createdBy") != "prompt-creator":
        errors.append("createdBy must be prompt-creator")
    if meta.get("validationStatus") not in {"draft", "validated"}:
        errors.append("validationStatus must be draft or validated")

    present = headings(body)
    for section in sorted(REQUIRED_SECTIONS - present):
        errors.append(f"missing required section: {section}")
    if "https://fonts.googleapis.com" in body or "http://fonts.googleapis.com" in body:
        errors.append("remote font dependency is not allowed")
    errors.extend(validate_placeholders(text))
    if prompt_type in HANDLED_TYPES:
        errors.extend(validate_type_specific(prompt_type, body, present))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a prompt-creator artifact")
    parser.add_argument("path", nargs="?", help="Markdown prompt artifact path")
    parser.add_argument("--fixture", help="JSON fixture with an artifact field")
    args = parser.parse_args()

    try:
        text = load_text(args)
        errors = validate(text)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    for error in errors:
        print(f"ERROR: {error}")
    print(f"prompt_artifact={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

