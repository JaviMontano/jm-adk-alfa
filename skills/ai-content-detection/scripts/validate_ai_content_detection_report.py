#!/usr/bin/env python3
"""Validate deterministic AI content detection report packets offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.ai-content-detection.report.v1"
REQUIRED_TOP = {
    "schema",
    "content",
    "scope",
    "evidence",
    "signals",
    "assessment",
    "watermark",
    "human_ai_strategy",
    "decision_policy",
    "validation",
    "risks",
}
TAGS = {"[EXPLICIT]", "[INFERRED]", "[OPEN]"}
SIGNAL_TYPES = {"model-detector", "stylometry", "metadata", "watermark", "provenance", "citation-integrity", "edit-history", "disclosure"}
DIRECTIONS = {"ai", "human", "mixed", "unknown"}
WATERMARK_STATUSES = {"present", "absent", "not-checked"}
FINAL_ACTIONS = {"no-action", "human-review", "request-disclosure", "editorial-review", "policy-review"}
DISALLOWED_ACTIONS = {"accuse-author", "automatic-penalty", "ban", "punish"}
CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "false_positive_control",
    "threshold_policy",
    "evidence_required",
    "no_authorship_claim",
}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def objects(value: Any, name: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for i, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{name}[{i}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def non_empty_strings(value: Any, name: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out = [item for item in value if isinstance(item, str) and item]
    require(len(out) == len(value), errors, f"{name} must contain only non-empty strings")
    return out


def bounded(value: Any) -> bool:
    return isinstance(value, (int, float)) and 0 <= value <= 1


def expected_class(likelihood: float) -> str:
    if likelihood >= 0.80:
        return "likely-ai"
    if likelihood >= 0.55:
        return "mixed"
    if likelihood <= 0.25:
        return "likely-human"
    return "inconclusive"


def validate_refs(refs: Any, known: set[str], owner: str, errors: list[str], required: bool = False) -> None:
    ids = non_empty_strings(refs, f"{owner}.evidence_ids", errors)
    if required:
        require(bool(ids), errors, f"{owner}.evidence_ids required")
    for ref in ids:
        require(ref in known, errors, f"{owner} references unknown evidence {ref}")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> set[str]:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    ids: set[str] = set()
    for item in evidence:
        eid = item.get("id")
        require(isinstance(eid, str) and bool(eid), errors, "evidence id required")
        if isinstance(eid, str):
            require(eid not in ids, errors, f"duplicate evidence id {eid}")
            ids.add(eid)
        require(item.get("tag") in TAGS, errors, f"evidence {eid} invalid tag")
        require(bool(item.get("source")), errors, f"evidence {eid} source required")
        require(bool(item.get("summary")), errors, f"evidence {eid} summary required")
    return ids


def validate_content_scope(data: dict[str, Any], errors: list[str]) -> None:
    content = data.get("content")
    require(isinstance(content, dict), errors, "content must be object")
    if isinstance(content, dict):
        for field in ("id", "type", "language"):
            require(isinstance(content.get(field), str) and bool(content.get(field)), errors, f"content.{field} required")
        require(isinstance(content.get("sample_size"), int) and content["sample_size"] >= 0, errors, "content.sample_size must be non-negative integer")
    scope = data.get("scope")
    require(isinstance(scope, dict), errors, "scope must be object")
    if isinstance(scope, dict):
        require(bool(scope.get("purpose")), errors, "scope.purpose required")
        require(scope.get("allowed_use") in {"review-only", "policy", "editorial", "compliance", "education", "moderation"}, errors, "scope.allowed_use invalid")
        require(isinstance(scope.get("high_stakes"), bool), errors, "scope.high_stakes must be boolean")


def validate_signals(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    signals = objects(data.get("signals"), "signals", errors)
    require(bool(signals), errors, "signals required")
    seen: set[str] = set()
    for signal in signals:
        sid = signal.get("id")
        require(isinstance(sid, str) and bool(sid), errors, "signal id required")
        if isinstance(sid, str):
            require(sid not in seen, errors, f"duplicate signal id {sid}")
            seen.add(sid)
        require(signal.get("type") in SIGNAL_TYPES, errors, f"signal {sid} invalid type")
        require(bounded(signal.get("score")), errors, f"signal {sid} score must be 0..1")
        require(bounded(signal.get("weight")), errors, f"signal {sid} weight must be 0..1")
        require(signal.get("direction") in DIRECTIONS, errors, f"signal {sid} invalid direction")
        require(bool(signal.get("notes")), errors, f"signal {sid} notes required")
        validate_refs(signal.get("evidence_ids"), evidence_ids, f"signal {sid}", errors, required=True)


def validate_assessment(data: dict[str, Any], errors: list[str]) -> None:
    assessment = data.get("assessment")
    require(isinstance(assessment, dict), errors, "assessment must be object")
    if not isinstance(assessment, dict):
        return
    likelihood = assessment.get("ai_likelihood")
    require(bounded(likelihood), errors, "assessment.ai_likelihood must be 0..1")
    require(bounded(assessment.get("confidence")), errors, "assessment.confidence must be 0..1")
    if bounded(likelihood):
        require(assessment.get("classification") == expected_class(float(likelihood)), errors, "assessment.classification does not match threshold policy")
    require(assessment.get("authorship_claim") == "not-determined", errors, "assessment.authorship_claim must be not-determined")
    require(bool(assessment.get("rationale")), errors, "assessment.rationale required")
    require(isinstance(assessment.get("limitations"), list), errors, "assessment.limitations must be list")


def validate_watermark(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    watermark = data.get("watermark")
    require(isinstance(watermark, dict), errors, "watermark must be object")
    if not isinstance(watermark, dict):
        return
    status = watermark.get("status")
    require(status in WATERMARK_STATUSES, errors, "watermark.status invalid")
    refs = watermark.get("evidence_ids")
    validate_refs(refs, evidence_ids, "watermark", errors, required=status == "present")
    if status == "present":
        require(bool(watermark.get("method")), errors, "watermark.method required when present")
    if status == "not-checked":
        require(bool(watermark.get("notes")), errors, "watermark.notes required when not-checked")


def validate_strategy_and_decision(data: dict[str, Any], errors: list[str]) -> None:
    strategy = data.get("human_ai_strategy")
    require(isinstance(strategy, dict), errors, "human_ai_strategy must be object")
    if isinstance(strategy, dict):
        require(bool(strategy.get("recommended_label")), errors, "human_ai_strategy.recommended_label required")
        require(bool(non_empty_strings(strategy.get("review_steps"), "human_ai_strategy.review_steps", errors)), errors, "human_ai_strategy.review_steps required")

    policy = data.get("decision_policy")
    require(isinstance(policy, dict), errors, "decision_policy must be object")
    if not isinstance(policy, dict):
        return
    final_action = policy.get("final_action")
    require(final_action in FINAL_ACTIONS, errors, "decision_policy.final_action invalid")
    allowed = set(non_empty_strings(policy.get("allowed_actions"), "decision_policy.allowed_actions", errors))
    disallowed = set(non_empty_strings(policy.get("disallowed_actions"), "decision_policy.disallowed_actions", errors))
    require(not (allowed & DISALLOWED_ACTIONS), errors, "decision_policy.allowed_actions contains disallowed action")
    require(DISALLOWED_ACTIONS.intersection(disallowed), errors, "decision_policy.disallowed_actions must include at least one punitive action")
    if isinstance(data.get("scope"), dict) and data["scope"].get("high_stakes"):
        require(final_action in {"human-review", "policy-review"}, errors, "high-stakes scope requires human-review or policy-review")
    language = str(policy.get("user_facing_language", "")).lower()
    require(bool(language), errors, "decision_policy.user_facing_language required")
    for blocked in ("definitely ai", "the author used ai", "punish", "ban this author"):
        require(blocked not in language, errors, f"decision_policy.user_facing_language contains accusatory phrase: {blocked}")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if not isinstance(validation, dict):
        return
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    checks = validation.get("checks")
    require(isinstance(checks, list), errors, "validation.checks must be list")
    if isinstance(checks, list):
        require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    evidence_ids = validate_evidence(data, errors)
    validate_content_scope(data, errors)
    validate_signals(data, evidence_ids, errors)
    validate_assessment(data, errors)
    validate_watermark(data, evidence_ids, errors)
    validate_strategy_and_decision(data, errors)
    validate_validation(data, errors)
    require(isinstance(data.get("risks"), list), errors, "risks must be list")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_ai_content_detection_report.py <report.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data if isinstance(data, dict) else {})
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
