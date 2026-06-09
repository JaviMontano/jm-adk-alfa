#!/usr/bin/env python3
"""Validate deterministic mock-interview feedback reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DIMS = ("substance", "english", "presence")
LANGUAGES = {"es", "en"}
SUCCESS_TERMS = (
    "guaranteed pass",
    "definitely pass",
    "will get hired",
    "hired for sure",
    "pasas seguro",
    "contratacion garantizada",
)
FABRICATION_TERMS = ("invent", "fabricate", "make up experience", "mentir", "inventar experiencia")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def text(value: Any) -> str:
    return str(value or "").strip()


def all_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(all_text(v) for v in value)
    return text(value)


def contains_any(data: Any, terms: tuple[str, ...]) -> bool:
    haystack = all_text(data).lower()
    return any(term in haystack for term in terms)


def weakest_dimension(scores: dict[str, Any]) -> str | None:
    parsed: dict[str, int] = {}
    for dim in DIMS:
        item = scores.get(dim)
        if not isinstance(item, dict):
            return None
        parsed[dim] = int(item.get("score", 0))
    return min(DIMS, key=lambda dim: parsed[dim])


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("skill") != "simulador-entrevista":
        errors.append("skill must be simulador-entrevista")
    if any(key in data for key in ("overall_score", "average_score", "final_score")):
        errors.append("overall or average scores are forbidden")
    if contains_any(data, SUCCESS_TERMS):
        errors.append("success guarantee language is forbidden")
    if contains_any(data, FABRICATION_TERMS):
        errors.append("fabricated experience guidance is forbidden")

    session = data.get("session")
    if not isinstance(session, dict):
        errors.append("session must be an object")
    else:
        if text(session.get("language")) not in LANGUAGES:
            errors.append("session.language must be es or en")
        if session.get("one_question_mode") is not True:
            errors.append("session.one_question_mode must be true")
        if not isinstance(session.get("turn"), int) or int(session.get("turn", 0)) < 1:
            errors.append("session.turn must be a positive integer")
        if not text(session.get("role")):
            errors.append("session.role is required")

    question = data.get("question")
    if not isinstance(question, dict):
        errors.append("question must be an object")
    else:
        for key in ("id", "angle", "prompt"):
            if not text(question.get(key)):
                errors.append(f"question.{key} is required")
        if isinstance(question.get("prompts"), list) and len(question.get("prompts", [])) > 1:
            errors.append("only one question is allowed per turn")

    if not text(data.get("answer_summary")):
        errors.append("answer_summary is required")

    evidence = data.get("evidence_snippets")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence_snippets must be a non-empty list")
        evidence = []
    evidence_ids: list[str] = []
    for item in evidence:
        if not isinstance(item, dict):
            errors.append("evidence snippet must be an object")
            continue
        ev_id = text(item.get("id"))
        evidence_ids.append(ev_id)
        if not ev_id:
            errors.append("evidence_snippet.id is required")
        if not text(item.get("snippet")):
            errors.append(f"{ev_id}.snippet is required")
    evidence_id_set = set(evidence_ids)

    scores = data.get("scores")
    low_dims: list[str] = []
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
        scores = {}
    for dim in DIMS:
        item = scores.get(dim)
        if not isinstance(item, dict):
            errors.append(f"scores.{dim} must be an object")
            continue
        score = item.get("score")
        if not isinstance(score, int) or not 1 <= score <= 5:
            errors.append(f"scores.{dim}.score must be an integer from 1 to 5")
            continue
        if score < 2:
            low_dims.append(dim)
            errors.append(f"scores.{dim}.score below floor: {score}")
        ref = text(item.get("evidence_ref"))
        if ref not in evidence_id_set:
            errors.append(f"scores.{dim}.evidence_ref is unresolved: {ref}")
        if not text(item.get("rationale")):
            errors.append(f"scores.{dim}.rationale is required")

    flags = data.get("flags", [])
    if not isinstance(flags, list):
        errors.append("flags must be a list")
        flags = []
    if low_dims and not any(text(flag.get("type")) == "below_floor" for flag in flags if isinstance(flag, dict)):
        errors.append("below_floor flag is required when a score is below floor")

    next_step = data.get("next_step")
    weakest = weakest_dimension(scores) if isinstance(scores, dict) else None
    if not isinstance(next_step, dict):
        errors.append("next_step must be an object")
    else:
        target = text(next_step.get("target_dimension"))
        if target not in DIMS:
            errors.append("next_step.target_dimension must be substance, english, or presence")
        elif weakest and target != weakest:
            errors.append(f"next_step.target_dimension must target weakest dimension: {weakest}")
        for key in ("action", "practice_prompt"):
            if not text(next_step.get(key)):
                errors.append(f"next_step.{key} is required")

    validation = data.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("offline") is not True:
            errors.append("validation.offline must be true")
        if validation.get("network_used") not in (False, None):
            errors.append("validation.network_used must be false")
        if text(validation.get("result")) not in {"pass", "blocked"}:
            errors.append("validation.result must be pass or blocked")

    if errors and isinstance(validation, dict) and text(validation.get("result")) == "pass":
        errors.append("validation.result must not be pass when errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate simulador-entrevista JSON feedback")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        data = load_json(Path(args.input))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"interview_feedback={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
