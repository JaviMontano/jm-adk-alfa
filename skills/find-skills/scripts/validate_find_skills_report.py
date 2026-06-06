#!/usr/bin/env python3
"""Validate deterministic find-skills recommendation report fixtures."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def has_evidence(value: Any, allowed: set[str]) -> bool:
    if isinstance(value, str):
        return any(tag in value for tag in allowed)
    if isinstance(value, list):
        return any(has_evidence(item, allowed) for item in value)
    if isinstance(value, dict):
        return any(has_evidence(item, allowed) for item in value.values())
    return False


def require_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if obj.get(field) in ("", [], None):
            errors.append(f"{label} missing {field}")


def validate_iso_date(value: str, field: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must be ISO date: {value}")


def validate_no_moving_terms(report: dict[str, Any], terms: list[str], errors: list[str]) -> None:
    body = json.dumps(report, ensure_ascii=False)
    for term in terms:
        if re.search(rf"\b{re.escape(term)}\b", body, flags=re.IGNORECASE):
            errors.append(f"report must avoid moving time term: {term}")


def validate_score(candidate: dict[str, Any], rubric: dict[str, Any], errors: list[str]) -> None:
    cid = candidate.get("id", "<missing-id>")
    breakdown = candidate.get("score_breakdown")
    if not isinstance(candidate.get("score_total"), int):
        errors.append(f"candidate {cid} score_total must be an integer")
        return
    if candidate["score_total"] < 0 or candidate["score_total"] > 100:
        errors.append(f"candidate {cid} score_total must be between 0 and 100")
    if not isinstance(breakdown, dict):
        errors.append(f"candidate {cid} score_breakdown must be an object")
        return
    total = 0
    for field, max_score in rubric["score_dimensions"].items():
        value = breakdown.get(field)
        if not isinstance(value, int):
            errors.append(f"candidate {cid} score_breakdown {field} must be integer")
            continue
        if value < 0 or value > max_score:
            errors.append(f"candidate {cid} score_breakdown {field} out of range")
        total += value
    if total != candidate["score_total"]:
        errors.append(f"candidate {cid} score_total does not match score_breakdown")


def validate_candidates(
    report: dict[str, Any],
    contract: dict[str, Any],
    sources: dict[str, Any],
    rubric: dict[str, Any],
    install_policy: dict[str, Any],
    allowed_tags: set[str],
    errors: list[str],
) -> set[str]:
    candidates = report.get("candidates")
    mode = report.get("mode")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        return set()
    if mode != "no-match" and not candidates:
        errors.append("non no-match reports require candidates")
    if len(candidates) > rubric["max_candidates_default"]:
        errors.append("candidate list exceeds default maximum")

    ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append("each candidate must be an object")
            continue
        cid = str(candidate.get("id", ""))
        ids.add(cid)
        require_fields(candidate, contract["required_candidate_fields"], f"candidate {cid or '<missing-id>'}", errors)
        if candidate.get("source_type") not in sources["source_types"]:
            errors.append(f"candidate {cid} invalid source_type")
        if candidate.get("quality_tier") not in rubric["quality_tiers"]:
            errors.append(f"candidate {cid} invalid quality_tier")
        if candidate.get("moat_depth") not in rubric["moat_depths"]:
            errors.append(f"candidate {cid} invalid moat_depth")
        if candidate.get("install_action") not in install_policy["allowed_install_actions"]:
            errors.append(f"candidate {cid} invalid install_action")
        if candidate.get("install_action") in install_policy["forbidden_install_actions"]:
            errors.append(f"candidate {cid} uses forbidden install_action")
        if candidate.get("source_type") == "remote":
            if not candidate.get("remote_snapshot_date"):
                errors.append(f"candidate {cid} remote source requires remote_snapshot_date")
            else:
                validate_iso_date(str(candidate["remote_snapshot_date"]), f"candidate {cid} remote_snapshot_date", errors)
            if candidate.get("requires_confirmation") is not True:
                errors.append(f"candidate {cid} remote install requires confirmation")
        if not isinstance(candidate.get("evidence_refs"), list) or not has_evidence(candidate.get("evidence_refs"), allowed_tags):
            errors.append(f"candidate {cid} evidence_refs must include evidence tag")
        validate_score(candidate, rubric, errors)
    return ids


def validate_recommendation(
    report: dict[str, Any],
    candidate_ids: set[str],
    rubric: dict[str, Any],
    allowed_tags: set[str],
    errors: list[str],
) -> None:
    recommendation = report.get("recommendation")
    if not isinstance(recommendation, dict):
        errors.append("recommendation must be an object")
        return
    require_fields(recommendation, ["selected_candidate_id", "rationale", "confidence", "next_action"], "recommendation", errors)
    selected = recommendation.get("selected_candidate_id")
    if report.get("mode") == "no-match":
        if selected not in ("none", None):
            errors.append("no-match recommendation selected_candidate_id must be none")
    elif selected not in candidate_ids:
        errors.append("recommendation selected_candidate_id must reference a candidate")
    if recommendation.get("confidence") not in rubric["confidence"]:
        errors.append("recommendation confidence is invalid")
    if not has_evidence(recommendation.get("rationale"), allowed_tags):
        errors.append("recommendation rationale must include evidence tag")
    if not has_evidence(recommendation.get("next_action"), allowed_tags):
        errors.append("recommendation next_action must include evidence tag")

    candidates = report.get("candidates", [])
    selected_candidate = next(
        (candidate for candidate in candidates if isinstance(candidate, dict) and candidate.get("id") == selected),
        None,
    )
    if selected_candidate and selected_candidate.get("quality_tier") == "F":
        errors.append("Tier F candidate cannot be recommended")


def validate_install_policy(
    report: dict[str, Any],
    install_policy: dict[str, Any],
    errors: list[str],
) -> None:
    policy = report.get("install_policy")
    if not isinstance(policy, dict):
        errors.append("install_policy must be an object")
        return
    if policy.get("auto_install") is not False:
        errors.append("install_policy auto_install must be false")
    if policy.get("user_confirmation_required") is not True:
        errors.append("install_policy user_confirmation_required must be true")
    if policy.get("allowed_action") != "present_command_only":
        errors.append("install_policy allowed_action must be present_command_only")
    if install_policy.get("auto_install_allowed") is not False:
        errors.append("asset install policy must disallow auto install")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a find-skills recommendation report JSON file")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    contract = load_json(ASSETS / "report-contract.json")
    sources = load_json(ASSETS / "source-policy.json")
    rubric = load_json(ASSETS / "scoring-rubric.json")
    install_policy = load_json(ASSETS / "install-policy.json")
    allowed_tags = set(contract["allowed_evidence_tags"])

    report = load_json(args.report)
    errors: list[str] = []
    if not isinstance(report, dict):
        errors.append("report root must be an object")
    else:
        for field in contract["required_top_level"]:
            if field not in report:
                errors.append(f"missing top-level field: {field}")
        if report.get("skill") != "find-skills":
            errors.append("skill must be find-skills")
        if report.get("mode") not in contract["modes"]:
            errors.append("mode is not allowed")
        if report.get("scope") not in sources["scopes"]:
            errors.append("scope is not allowed")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    validate_iso_date(str(report["reference_date"]), "reference_date", errors)
    validate_no_moving_terms(report, contract["moving_time_terms"], errors)
    for section in ("summary", "validation", "risks"):
        if not has_evidence(report.get(section), allowed_tags):
            errors.append(f"{section} must include evidence tag")

    intent = report.get("intent")
    if not isinstance(intent, dict):
        errors.append("intent must be an object")
    else:
        require_fields(intent, sources["required_intent_fields"], "intent", errors)
        if intent.get("source_scope") != report.get("scope"):
            errors.append("intent source_scope must match report scope")
        if intent.get("evidence_tag") not in allowed_tags:
            errors.append("intent evidence_tag is invalid")

    candidate_ids = validate_candidates(report, contract, sources, rubric, install_policy, allowed_tags, errors)
    validate_recommendation(report, candidate_ids, rubric, allowed_tags, errors)
    validate_install_policy(report, install_policy, errors)

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"PASS {args.report.name}: candidates={len(report['candidates'])} mode={report['mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
