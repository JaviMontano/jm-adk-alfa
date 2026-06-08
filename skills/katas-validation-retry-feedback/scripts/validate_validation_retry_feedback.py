#!/usr/bin/env python3
"""Validate deterministic validation-retry-feedback reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL = "katas-validation-retry-feedback"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def policy(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_generic_feedback(message: str, forbidden_phrases: list[str]) -> bool:
    lowered = message.lower()
    return any(re.search(rf"\b{re.escape(phrase)}\b", lowered) for phrase in forbidden_phrases)


def validate_feedback(
    feedback: Any,
    error: dict[str, Any],
    policy_data: dict[str, Any],
    index: int,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(feedback, dict):
        return [f"attempt {index} feedback must be an object"]

    for field in policy_data["required_feedback_fields"]:
        if field not in feedback:
            errors.append(f"attempt {index} feedback missing field {field}")
    message = feedback.get("message")
    if not non_empty_string(message):
        errors.append(f"attempt {index} feedback.message must be non-empty")
        message = ""
    if is_generic_feedback(str(message), policy_data["forbidden_generic_phrases"]):
        errors.append(f"attempt {index} feedback.message is generic")

    path = str(error.get("path", ""))
    expected = str(error.get("expected", ""))
    actual = str(error.get("actual", ""))
    for label, value in [("path", path), ("expected", expected), ("previous_value", actual)]:
        if value and value not in str(message):
            errors.append(f"attempt {index} feedback.message must include {label}")

    if feedback.get("path") != error.get("path"):
        errors.append(f"attempt {index} feedback.path must match validator_error.path")
    if feedback.get("expected") != error.get("expected"):
        errors.append(f"attempt {index} feedback.expected must match validator_error.expected")
    if feedback.get("previous_value") != error.get("actual"):
        errors.append(f"attempt {index} feedback.previous_value must match validator_error.actual")
    scope_paths = feedback.get("scope_paths")
    if not isinstance(scope_paths, list) or not scope_paths:
        errors.append(f"attempt {index} feedback.scope_paths must be a non-empty list")
    elif error.get("path") not in scope_paths:
        errors.append(f"attempt {index} feedback.scope_paths must include validator_error.path")
    if not isinstance(feedback.get("allowed_retry"), bool):
        errors.append(f"attempt {index} feedback.allowed_retry must be boolean")
    return errors


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = policy("validation-retry-contract.json")["json_contract"]
    classification_policy = policy("error-classification-policy.json")
    feedback_policy = policy("feedback-specificity-policy.json")
    retry_policy = policy("retry-limit-policy.json")
    evidence_policy = policy("evidence-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    for field in ["report_id", "scenario", "source", "schema_under_validation"]:
        if not non_empty_string(report.get(field)):
            errors.append(f"{field} must be a non-empty string")

    evidence = report.get("evidence")
    accepted_evidence = set(evidence_policy["accepted_evidence_types"])
    seen_evidence_types: set[str] = set()
    if not isinstance(evidence, list) or len(evidence) < evidence_policy["minimum_evidence_items"]:
        errors.append(f"evidence must contain at least {evidence_policy['minimum_evidence_items']} items")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            evidence_type = item.get("type")
            if evidence_type not in accepted_evidence:
                errors.append(f"evidence[{index}].type must be accepted")
            else:
                seen_evidence_types.add(str(evidence_type))
            if not non_empty_string(item.get("detail")):
                errors.append(f"evidence[{index}].detail must be non-empty")

    attempts = report.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        errors.append("attempts must be a non-empty list")
        attempts = []

    recoverable_types = set(classification_policy["recoverable_error_types"])
    nonrecoverable_types = set(classification_policy["nonrecoverable_error_types"])
    known_error_types = recoverable_types | nonrecoverable_types
    failed_errors: list[dict[str, Any]] = []
    recoverable_paths: set[str] = set()
    nonrecoverable_paths: set[str] = set()

    for index, attempt in enumerate(attempts):
        if not isinstance(attempt, dict):
            errors.append(f"attempts[{index}] must be an object")
            continue
        expected_attempt_number = index + 1
        if attempt.get("attempt") != expected_attempt_number:
            errors.append(f"attempts[{index}].attempt must be {expected_attempt_number}")
        status = attempt.get("status")
        if status not in contract["attempt_statuses"]:
            errors.append(f"attempt {expected_attempt_number}.status must be one of {contract['attempt_statuses']}")
        if status == "failed":
            validator_error = attempt.get("validator_error")
            if not isinstance(validator_error, dict):
                errors.append(f"attempt {expected_attempt_number} failed status requires validator_error")
                continue
            for field in classification_policy["required_error_fields"]:
                if field not in validator_error:
                    errors.append(f"attempt {expected_attempt_number}.validator_error missing field {field}")
            error_type = validator_error.get("error_type")
            if error_type not in known_error_types:
                errors.append(f"attempt {expected_attempt_number}.validator_error.error_type is unknown")
            path = validator_error.get("path")
            if not non_empty_string(path):
                errors.append(f"attempt {expected_attempt_number}.validator_error.path must be non-empty")
            if not non_empty_string(validator_error.get("expected")):
                errors.append(f"attempt {expected_attempt_number}.validator_error.expected must be non-empty")
            if "actual" not in validator_error:
                errors.append(f"attempt {expected_attempt_number}.validator_error.actual is required")
            failed_errors.append(validator_error)
            if error_type in recoverable_types and non_empty_string(path):
                recoverable_paths.add(str(path))
            if error_type in nonrecoverable_types and non_empty_string(path):
                nonrecoverable_paths.add(str(path))
            feedback = attempt.get("feedback")
            if feedback is not None:
                errors.extend(validate_feedback(feedback, validator_error, feedback_policy, expected_attempt_number))
                if error_type in nonrecoverable_types and feedback.get("allowed_retry") is True:
                    errors.append(f"attempt {expected_attempt_number} must not allow retry for nonrecoverable error")
                if error_type in nonrecoverable_types and validator_error.get("path") in feedback.get("scope_paths", []):
                    errors.append(f"attempt {expected_attempt_number} must not scope retry to nonrecoverable path")

    if attempts and attempts[-1].get("status") == "failed":
        errors.append("last attempt must be valid or represented by escalated outcome")

    classification = report.get("classification")
    if not isinstance(classification, dict):
        errors.append("classification must be an object")
        classification = {}
    else:
        if classification.get("recoverability") not in contract["recoverability_values"]:
            errors.append("classification.recoverability must be recoverable, nonrecoverable, or mixed")
        for field in ["recoverable_errors", "nonrecoverable_errors"]:
            if not isinstance(classification.get(field), list):
                errors.append(f"classification.{field} must be a list")
        if not isinstance(classification.get("retry_allowed"), bool):
            errors.append("classification.retry_allowed must be boolean")
        if not isinstance(classification.get("escalation_required"), bool):
            errors.append("classification.escalation_required must be boolean")
        if not non_empty_string(classification.get("reason")):
            errors.append("classification.reason must be non-empty")

    if nonrecoverable_paths and classification.get("escalation_required") is not True:
        errors.append("classification.escalation_required must be true when nonrecoverable errors exist")
    if nonrecoverable_paths and "absence_check" not in seen_evidence_types:
        errors.append("source_absent/nonrecoverable cases require absence_check evidence")
    if recoverable_paths and not set(evidence_policy["required_for_retry"]).issubset(seen_evidence_types):
        errors.append("retry cases require validator_error and previous_output evidence")

    outcome = report.get("outcome")
    if not isinstance(outcome, dict):
        errors.append("outcome must be an object")
        outcome = {}
    else:
        if outcome.get("final_status") not in contract["final_statuses"]:
            errors.append("outcome.final_status must be valid or escalated")
        max_attempts = outcome.get("max_attempts")
        if max_attempts not in retry_policy["allowed_total_attempts"]:
            errors.append(f"outcome.max_attempts must be one of {retry_policy['allowed_total_attempts']}")
        retry_count = outcome.get("retry_count")
        expected_retry_count = max(0, len(attempts) - 1)
        if retry_count != expected_retry_count:
            errors.append(f"outcome.retry_count must equal {expected_retry_count}")
        if isinstance(retry_count, int) and retry_count > retry_policy["max_retry_count"]:
            errors.append("outcome.retry_count exceeds max retry count")
        if isinstance(max_attempts, int) and len(attempts) > max_attempts:
            errors.append("attempt count exceeds outcome.max_attempts")
        if not isinstance(outcome.get("needs_human_review"), bool):
            errors.append("outcome.needs_human_review must be boolean")
        if not isinstance(outcome.get("error_chain"), list):
            errors.append("outcome.error_chain must be a list")
        if not isinstance(outcome.get("structural_fix_required"), bool):
            errors.append("outcome.structural_fix_required must be boolean")
        if outcome.get("final_status") == "valid":
            if not attempts or attempts[-1].get("status") != "valid":
                errors.append("valid final_status requires last attempt status valid")
            if outcome.get("needs_human_review") is not False:
                errors.append("valid final_status requires needs_human_review false")
        if outcome.get("final_status") == "escalated":
            if outcome.get("needs_human_review") is not True:
                errors.append("escalated final_status requires needs_human_review true")
            if not outcome.get("error_chain"):
                errors.append("escalated final_status requires non-empty error_chain")
        if (
            isinstance(max_attempts, int)
            and len(attempts) >= max_attempts
            and attempts[-1].get("status") != "valid"
            and outcome.get("final_status") != "escalated"
        ):
            errors.append("exhausted attempts must escalate")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        if validation.get("generic_feedback_count") != 0:
            errors.append("validation.generic_feedback_count must be 0")
        if validation.get("retry_count_with_specific_feedback") != outcome.get("retry_count"):
            errors.append("validation.retry_count_with_specific_feedback must equal outcome.retry_count")
        if validation.get("retry_count_exceeds_cap") is not False:
            errors.append("validation.retry_count_exceeds_cap must be false")
        if validation.get("nonrecoverable_retried") is not False:
            errors.append("validation.nonrecoverable_retried must be false")
        if validation.get("invalid_output_accepted") is not False:
            errors.append("validation.invalid_output_accepted must be false")
        if validation.get("deterministic_script_passed") is not True:
            errors.append("validation.deterministic_script_passed must be true")
        if "exhausted_attempts_escalated" not in validation:
            errors.append("validation.exhausted_attempts_escalated is required")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
    else:
        if guardian.get("decision") not in contract["guardian_decisions"]:
            errors.append(f"guardian.decision must be one of {contract['guardian_decisions']}")
        if not non_empty_string(guardian.get("reason")):
            errors.append("guardian.reason must be non-empty")
        if validation and validation.get("invalid_output_accepted") is True and guardian.get("decision") == "pass":
            errors.append("guardian must not pass when invalid output is accepted")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a validation retry feedback JSON report")
    parser.add_argument("report", type=Path, help="Path to a JSON report")
    args = parser.parse_args()

    try:
        report = load_json(args.report)
        errors = validate(report)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
