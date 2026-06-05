#!/usr/bin/env python3
"""Validate deterministic agent constitution Markdown files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["missing YAML frontmatter"]
    rest = text[4:]
    end = rest.find("\n---")
    if end < 0:
        return {}, text, ["unterminated YAML frontmatter"]
    raw = rest[:end]
    body = rest[end + 4 :]
    frontmatter: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter, body, errors


def markdown_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def count_bullets(section: str) -> int:
    return sum(1 for line in section.splitlines() if re.match(r"^\s*-\s+", line))


def count_table_rows(section: str, header_token: str) -> int:
    rows = 0
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        lowered = stripped.lower()
        if header_token.lower() in lowered:
            continue
        if re.fullmatch(r"\|[\s:\-|]+\|", stripped):
            continue
        rows += 1
    return rows


def extract_code_items(section: str) -> list[str]:
    return [item.strip() for item in re.findall(r"`([^`]+)`", section) if item.strip()]


def normalize_registry(value: str | None) -> set[str]:
    if not value:
        return set()
    return {part.strip() for part in value.split(",") if part.strip()}


def validate(schema: dict, text: str, registry: set[str]) -> list[str]:
    errors: list[str] = []
    frontmatter, body, frontmatter_errors = parse_frontmatter(text)
    errors.extend(frontmatter_errors)
    sections = markdown_sections(body)

    for key in schema["frontmatter_required"]:
        if not frontmatter.get(key):
            errors.append(f"missing frontmatter field: {key}")
    if frontmatter.get("id") and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", frontmatter["id"]):
        errors.append("frontmatter id must be kebab-case")
    if frontmatter.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+", frontmatter["version"]):
        errors.append("frontmatter version must be semver")

    for section in schema["required_sections"]:
        if section not in sections:
            errors.append(f"missing section: {section}")
        elif not sections[section].strip():
            errors.append(f"empty section: {section}")

    lowered = text.lower()
    for phrase in schema.get("blocked_phrases", []):
        if phrase.lower() in lowered:
            errors.append(f"blocked phrase present: {phrase}")

    if not any(tag in text for tag in schema.get("allowed_evidence_tags", [])):
        errors.append("missing evidence tags")

    decision = sections.get("Decision Rights", "")
    for term in schema.get("required_decision_terms", []):
        if term not in decision:
            errors.append(f"Decision Rights missing term: {term}")

    allowed = sections.get("Allowed Tools", "")
    allowed_tools = extract_code_items(allowed)
    if not allowed_tools:
        errors.append("Allowed Tools must list explicit backticked tool names")
    for tool in allowed_tools:
        if tool == "*" or tool.lower() in {"all", "all tools", "any available tool"}:
            errors.append(f"wildcard allowed tool: {tool}")
        if registry and tool not in registry:
            errors.append(f"tool not present in registry: {tool}")

    if "Forbidden Tools" in sections and not extract_code_items(sections["Forbidden Tools"]):
        errors.append("Forbidden Tools must list explicit backticked tool names")

    security = sections.get("Security Policy", "")
    for checkpoint in schema.get("required_security_checkpoints", []):
        if checkpoint not in security:
            errors.append(f"Security Policy missing checkpoint: {checkpoint}")

    escalation = sections.get("Escalation Rules", "")
    for term in schema.get("required_escalation_terms", []):
        if term not in escalation:
            errors.append(f"Escalation Rules missing term: {term}")

    minimums = schema.get("minimums", {})
    if count_bullets(sections.get("Non-Goals", "")) < int(minimums.get("non_goals", 0)):
        errors.append("Non-Goals must include at least three bullets")
    if count_table_rows(sections.get("Failure Handling", ""), "Failure Mode") < int(minimums.get("failure_modes", 0)):
        errors.append("Failure Handling must include at least three data rows")
    if count_table_rows(sections.get("KPIs", ""), "Metric") < int(minimums.get("kpis", 0)):
        errors.append("KPIs must include at least three data rows")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an agent constitution Markdown file")
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--constitution", required=True, type=Path)
    parser.add_argument("--tool-registry", help="Comma-separated list of registry-backed tool names")
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    try:
        schema = load_json(args.schema)
        text = args.constitution.read_text(encoding="utf-8")
        errors = validate(schema, text, normalize_registry(args.tool_registry))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    status = "fail" if errors else "pass"
    print(json.dumps({"status": status, "errors": errors}, indent=2, ensure_ascii=False))
    if args.expect:
        if status != args.expect:
            print(f"ERROR: expected {args.expect}, observed {status}", file=sys.stderr)
            return 1
        return 0
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
