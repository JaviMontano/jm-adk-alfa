#!/usr/bin/env python3
"""Compile a deterministic six-tool functional analysis report."""

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


def validate_event_storming(data: dict[str, Any]) -> None:
    event_storming = data.get("event_storming")
    if not isinstance(event_storming, dict):
        raise ValueError("event_storming must be an object")
    for key in ["events", "commands", "actors", "aggregates", "hot_spots"]:
        require_list(event_storming, key)


def validate_story_mapping(data: dict[str, Any]) -> None:
    story_mapping = data.get("story_mapping")
    if not isinstance(story_mapping, dict):
        raise ValueError("story_mapping must be an object")
    activities = require_list(story_mapping, "activities")
    story_ids: set[str] = set()
    for activity in activities:
        if not isinstance(activity, dict):
            raise ValueError("each story map activity must be an object")
        stories = require_list(activity, "stories")
        for story in stories:
            if not isinstance(story, dict):
                raise ValueError("each story must be an object")
            for key in ["id", "title", "release", "value"]:
                if not str(story.get(key, "")).strip():
                    raise ValueError(f"story missing {key}")
            story_ids.add(str(story["id"]))
    if len(story_ids) < 4:
        raise ValueError("story_mapping must contain at least 4 stories")


def validate_business_rules(data: dict[str, Any]) -> None:
    rules = require_list(data, "business_rules")
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("each business rule must be an object")
        for key in ["id", "type", "condition", "action", "use_cases"]:
            if key not in rule:
                raise ValueError(f"business rule missing {key}")
        if not isinstance(rule["use_cases"], list) or not rule["use_cases"]:
            raise ValueError(f"business rule {rule['id']} must link use cases")


def validate_acceptance(data: dict[str, Any]) -> None:
    scenarios = require_list(data, "acceptance_criteria")
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            raise ValueError("each acceptance scenario must be an object")
        for key in ["id", "title", "given", "when", "then"]:
            if not str(scenario.get(key, "")).strip():
                raise ValueError(f"acceptance scenario missing {key}")


def validate_traceability(data: dict[str, Any], schema: dict[str, Any]) -> None:
    rows = require_list(data, "traceability_matrix")
    required = set(schema["required_fields"])
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each traceability row must be an object")
        missing = required - set(row)
        if missing:
            raise ValueError(f"traceability row missing fields: {sorted(missing)}")
        for key in ["use_cases", "flows", "tests", "acceptance"]:
            if not isinstance(row[key], list) or not row[key]:
                raise ValueError(f"traceability row for {row.get('requirement')} has empty {key}")


def validate_anti_patterns(data: dict[str, Any], ruleset: dict[str, Any]) -> None:
    findings = require_list(data, "anti_pattern_detection")
    categories = set(ruleset["categories"])
    severities = set(ruleset["severities"])
    required = set(ruleset["required_fields"])
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("each anti-pattern finding must be an object")
        missing = required - set(finding)
        if missing:
            raise ValueError(f"anti-pattern finding missing fields: {sorted(missing)}")
        if finding["category"] not in categories:
            raise ValueError(f"unsupported anti-pattern category: {finding['category']}")
        if finding["severity"] not in severities:
            raise ValueError(f"unsupported anti-pattern severity: {finding['severity']}")


def validate_input(data: dict[str, Any], base: Path) -> None:
    if not str(data.get("domain", "")).strip():
        raise ValueError("domain is required")
    registry = load_json(base / "assets" / "toolbelt-tools.json")
    missing = [tool for tool in registry["required_tools"] if tool not in data]
    if missing:
        raise ValueError(f"missing required tool sections: {missing}")
    validate_event_storming(data)
    validate_story_mapping(data)
    validate_business_rules(data)
    validate_acceptance(data)
    validate_traceability(data, load_json(base / "assets" / "traceability-matrix-schema.json"))
    validate_anti_patterns(data, load_json(base / "assets" / "anti-pattern-rules.json"))


def render(data: dict[str, Any]) -> str:
    lines: list[str] = [f"# Functional Toolbelt Report: {data['domain']}", ""]
    es = data["event_storming"]
    lines.extend(["## Tool 1: Event Storming", ""])
    for event in es["events"]:
        lines.append(f"- Event: {event['name']} | actor: {event['actor']} | aggregate: {event['aggregate']}")
    lines.append(f"- Hot spots: {', '.join(item['name'] for item in es['hot_spots'])}")
    lines.extend(["", "## Tool 2: Story Mapping", ""])
    for activity in data["story_mapping"]["activities"]:
        lines.append(f"### {activity['name']}")
        for story in activity["stories"]:
            lines.append(f"- `{story['id']}` [{story['release']}]: {story['title']} -> {story['value']}")
    lines.extend(["", "## Tool 3: Business Rule Extraction", ""])
    for rule in data["business_rules"]:
        lines.append(
            f"- `{rule['id']}` [{rule['type']}]: IF {rule['condition']} THEN {rule['action']} "
            f"(use cases: {', '.join(rule['use_cases'])})"
        )
    lines.extend(["", "## Tool 4: Acceptance Criteria", ""])
    for scenario in data["acceptance_criteria"]:
        lines.append(f"### {scenario['id']} - {scenario['title']}")
        lines.append(f"Given {scenario['given']}")
        lines.append(f"When {scenario['when']}")
        lines.append(f"Then {scenario['then']}")
    lines.extend(["", "## Tool 5: Traceability Matrix", ""])
    lines.append("| Requirement | Use Cases | Flows | Tests | Acceptance |")
    lines.append("|---|---|---|---|---|")
    for row in data["traceability_matrix"]:
        lines.append(
            f"| {row['requirement']} | {', '.join(row['use_cases'])} | {', '.join(row['flows'])} | "
            f"{', '.join(row['tests'])} | {', '.join(row['acceptance'])} |"
        )
    lines.extend(["", "## Tool 6: Anti-Pattern Detection", ""])
    for finding in data["anti_pattern_detection"]:
        lines.append(f"- `{finding['id']}` [{finding['severity']}/{finding['category']}]: {finding['text']} -> {finding['fix']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic functional toolbelt report")
    parser.add_argument("--input", required=True, help="Structured six-tool input JSON")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        data = load_json(Path(args.input))
        validate_input(data, base)
        output = render(data)
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
