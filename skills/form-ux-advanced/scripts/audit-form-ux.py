#!/usr/bin/env python3
"""Audit advanced form UX journeys with deterministic friction scoring."""

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


def validate_journey(journey: dict[str, Any], heuristics: dict[str, Any]) -> None:
    if not str(journey.get("title", "")).strip():
        raise ValueError("title is required")
    steps = require_list(journey, "steps")
    allowed_timing = set(heuristics["allowed_validation_timing"])
    for step in steps:
        if not isinstance(step, dict):
            raise ValueError("each step must be an object")
        fields = step.get("fields")
        if not isinstance(fields, list) or not fields:
            raise ValueError(f"step fields must be non-empty: {step.get('id')}")
        for field in fields:
            if not isinstance(field, dict):
                raise ValueError("each field must be an object")
            if not str(field.get("name", "")).strip():
                raise ValueError("field.name is required")
            if not str(field.get("label", "")).strip():
                raise ValueError(f"field.label is required: {field.get('name')}")
            timing = field.get("validation_timing", "submit")
            if timing not in allowed_timing and timing != "keypress":
                raise ValueError(f"unsupported validation timing: {timing}")
    capabilities = journey.get("capabilities")
    if not isinstance(capabilities, dict):
        raise ValueError("capabilities must be an object")
    missing = [key for key in heuristics["required_capabilities"] if key not in capabilities]
    if missing:
        raise ValueError(f"capabilities missing keys: {missing}")


def score_journey(journey: dict[str, Any], heuristics: dict[str, Any]) -> tuple[int, list[str]]:
    penalties = heuristics["friction_penalties"]
    score = 100
    findings: list[str] = []
    steps = journey["steps"]
    field_count = 0
    required_count = 0
    smart_defaults = 0
    for step in steps:
        for field in step["fields"]:
            field_count += 1
            score -= int(penalties["field"])
            if field.get("required", False):
                required_count += 1
                score -= int(penalties["required_field"])
            if field.get("smart_default"):
                smart_defaults += 1
            timing = field.get("validation_timing", "submit")
            if timing == "keypress":
                score -= int(penalties["keypress_validation"])
                findings.append(f"`{field['name']}` validates on keypress; use debounced or blur feedback.")
    if len(steps) > 3:
        over = len(steps) - 3
        score -= over * int(penalties["step_after_three"])
        findings.append(f"{len(steps)} steps increases completion friction; consolidate if possible.")
    if smart_defaults == 0:
        score -= int(penalties["missing_smart_default"])
        findings.append("No smart defaults are declared.")
    capabilities = journey["capabilities"]
    capability_penalty = {
        "progress": "missing_progress",
        "back_navigation": "missing_back_navigation",
        "draft_preservation": "missing_draft_preservation",
        "error_summary": "missing_error_summary",
        "retry": "missing_retry",
    }
    for key, penalty_name in capability_penalty.items():
        if not capabilities.get(key):
            score -= int(penalties[penalty_name])
            findings.append(f"Missing capability: {key}.")
    if required_count > max(3, field_count // 2 + 1):
        findings.append("Required fields dominate the journey; defer nonessential questions.")
    return max(0, score), findings


def rating(score: int, thresholds: dict[str, int]) -> str:
    if score >= thresholds["pass"]:
        return "pass"
    if score >= thresholds["watch"]:
        return "watch"
    return "fail"


def render(journey: dict[str, Any], score: int, findings: list[str], assets: Path, thresholds: dict[str, int]) -> str:
    lines = [
        f"# {journey['title']} Form UX Audit",
        "",
        f"- Score: {score}",
        f"- Rating: {rating(score, thresholds)}",
        f"- Steps: {len(journey['steps'])}",
        "",
        "## Findings",
    ]
    if findings:
        lines.extend(f"- {finding}" for finding in findings)
    else:
        lines.append("- No blocking UX issues detected by the heuristic audit.")
    lines.extend(
        [
            "",
            "## Recommended Assets",
            "- `assets/wizard-progress-template.html` for step progress.",
            "- `assets/inline-validation-copy.json` for actionable validation copy.",
            "- `assets/error-recovery-checklist.md` for recovery behavior.",
            f"- Asset base: `{assets}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit advanced multi-step form UX")
    parser.add_argument("--journey", required=True, help="Form journey JSON")
    parser.add_argument("--output", help="Write audit Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        journey = load_json(Path(args.journey))
        heuristics = load_json(base / "assets" / "ux-heuristics.json")
        validate_journey(journey, heuristics)
        score, findings = score_journey(journey, heuristics)
        output = render(journey, score, findings, base / "assets", heuristics["score_thresholds"])
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
