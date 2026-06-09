#!/usr/bin/env python3
"""Validate deterministic validation retry loop plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_ERROR_FIELDS = {"code", "message", "path", "recoverability"}
REQUIRED_RETRY_PROMPT = {"previous_output", "exact_error", "correction_instruction"}
RECOVERABLE = {"invalid_json", "schema_mismatch", "field_out_of_range"}
NOT_RECOVERABLE = {"source_missing", "irreconcilable_ambiguity", "permission_denied"}
ESCALATION_REASONS = {"not_recoverable", "budget_exhausted", "systematic_repeat_error"}
BLOCKED_TEXT = (
    "retry original prompt unchanged",
    "boolean only validator",
    "return failed output as success",
    "accept failed output",
)


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


def as_dict(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def str_list(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {text(item) for item in value if text(item)}


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("skill") != "validation-retry-design":
        errors.append("skill must be validation-retry-design")
    lowered = all_text(data).lower()
    for marker in BLOCKED_TEXT:
        if marker in lowered:
            errors.append(f"blocked anti-pattern text: {marker}")

    validator = as_dict(data, "validator", errors)
    error_fields = str_list(validator.get("error_fields"))
    missing_error_fields = REQUIRED_ERROR_FIELDS - error_fields
    if missing_error_fields:
        errors.append(f"validator.error_fields missing: {sorted(missing_error_fields)}")
    if validator.get("boolean_only") not in (False, None):
        errors.append("validator.boolean_only must be false")

    retry_feedback = as_dict(data, "retry_feedback", errors)
    retry_prompt_fields = str_list(retry_feedback.get("prompt_includes"))
    missing_prompt = REQUIRED_RETRY_PROMPT - retry_prompt_fields
    if missing_prompt:
        errors.append(f"retry_feedback.prompt_includes missing: {sorted(missing_prompt)}")
    if retry_feedback.get("reuses_original_prompt_unchanged") not in (False, None):
        errors.append("retry_feedback.reuses_original_prompt_unchanged must be false")

    classification = as_dict(data, "failure_classification", errors)
    recoverable = str_list(classification.get("recoverable"))
    not_recoverable = str_list(classification.get("not_recoverable"))
    if not RECOVERABLE.intersection(recoverable):
        errors.append("failure_classification.recoverable must include a known recoverable error")
    if not NOT_RECOVERABLE.intersection(not_recoverable):
        errors.append("failure_classification.not_recoverable must include a known not-recoverable error")
    if classification.get("retry_not_recoverable") not in (False, None):
        errors.append("failure_classification.retry_not_recoverable must be false")

    budget = as_dict(data, "retry_budget", errors)
    max_retries = budget.get("max_retries")
    if not isinstance(max_retries, int) or max_retries < 1 or max_retries > 3:
        errors.append("retry_budget.max_retries must be 1..3")
    if budget.get("tracks_attempt_count") is not True:
        errors.append("retry_budget.tracks_attempt_count must be true")
    if budget.get("stores_error_chain") is not True:
        errors.append("retry_budget.stores_error_chain must be true")

    systematic = as_dict(data, "systematic_detection", errors)
    repeat_threshold = systematic.get("repeat_threshold")
    if not isinstance(repeat_threshold, int) or repeat_threshold < 2 or repeat_threshold > 3:
        errors.append("systematic_detection.repeat_threshold must be 2..3")
    if systematic.get("structural_fix_hint") is not True:
        errors.append("systematic_detection.structural_fix_hint must be true")

    escalation = as_dict(data, "escalation", errors)
    required_escalation = {"reason", "error_chain", "last_output", "recommended_next_step"}
    escalation_fields = str_list(escalation.get("fields"))
    missing_escalation = required_escalation - escalation_fields
    if missing_escalation:
        errors.append(f"escalation.fields missing: {sorted(missing_escalation)}")
    reasons = str_list(escalation.get("reasons"))
    if not ESCALATION_REASONS.issubset(reasons):
        errors.append("escalation.reasons must include not_recoverable, budget_exhausted, and systematic_repeat_error")
    if escalation.get("return_failed_output_as_success") not in (False, None):
        errors.append("escalation.return_failed_output_as_success must be false")

    validation = as_dict(data, "validation", errors)
    if validation.get("offline") is not True:
        errors.append("validation.offline must be true")
    if validation.get("network_required") not in (False, None):
        errors.append("validation.network_required must be false")
    if validation.get("deterministic") is not True:
        errors.append("validation.deterministic must be true")
    if text(validation.get("result")) not in {"pass", "blocked"}:
        errors.append("validation.result must be pass or blocked")
    if errors and text(validation.get("result")) == "pass":
        errors.append("validation.result must not be pass when errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate validation-retry-design JSON plan")
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
    print(f"validation_retry_plan={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
