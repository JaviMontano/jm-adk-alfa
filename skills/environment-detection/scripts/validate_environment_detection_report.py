#!/usr/bin/env python3
"""Validate environment-detection JSON reports offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


EXPECTED_SCHEMA = "jm-labs.environment-detection.report.v1"
ALLOWED_TAGS = {
    "[CÓDIGO]",
    "[CONFIG]",
    "[DOC]",
    "[INFERENCIA]",
    "[SUPUESTO]",
    "[EXPLICIT]",
    "[INFERRED]",
    "[OPEN]",
}
TRIAD_BY_IDE = {
    "claude-code": "full",
    "codex": "sequential",
    "gemini": "sequential",
    "antigravity": "sequential",
    "cursor": "checklist",
    "windsurf": "checklist",
    "copilot": "suggestion",
    "unknown": "sequential",
}
REJECTED_SOURCE_FRAGMENTS = (
    "http://",
    "https://",
    "web",
    "network",
    "current_time",
    "datetime",
    "random",
    "cookie",
    "account",
    "browser_history",
)
REQUIRED_CHECKS = {
    "signals_have_evidence",
    "mode_matches_capabilities",
    "tier_matches_budget",
    "loading_plan_bounded",
}
VALID_LEVELS = {"L1", "L2", "L3", "SKIP"}
MAX_L3_BY_TIER = {"heavy": 1, "medium": 1, "light": 0, "unknown": 0}
FORBIDDEN_L3_BY_TIER = {
    "medium": {"full-index", "all-skills", "full-history"},
    "light": {"full-index", "all-skills", "full-history", "active skill"},
    "unknown": {"full-index", "all-skills", "full-history", "active skill"},
}
FORBIDDEN_RESOURCES = {"full-transcript", "private-history", "browser-cookies", "account-state"}


def tier_for_budget(value: Any) -> str:
    if value is None:
        return "unknown"
    if not isinstance(value, int) or value <= 0:
        return "invalid"
    if value >= 100000:
        return "heavy"
    if value >= 32000:
        return "medium"
    return "light"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate_report(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top = {
        "schema",
        "environment",
        "signals",
        "capabilities",
        "decisions",
        "conflicts",
        "loading_plan",
        "validation",
        "recommendations",
    }
    missing_top = sorted(required_top - set(data))
    require(not missing_top, errors, f"missing top-level fields: {', '.join(missing_top)}")
    if errors:
        return errors

    require(data["schema"] == EXPECTED_SCHEMA, errors, "schema mismatch")

    env = data.get("environment")
    require(isinstance(env, dict), errors, "environment must be object")
    env = env if isinstance(env, dict) else {}
    for field in ("ide", "model", "model_tier", "triad_mode", "context_budget_tokens", "confidence"):
        require(field in env, errors, f"environment missing {field}")

    ide = env.get("ide")
    triad = env.get("triad_mode")
    model_tier = env.get("model_tier")
    confidence = env.get("confidence")
    budget = env.get("context_budget_tokens")

    require(ide in TRIAD_BY_IDE, errors, f"unsupported ide: {ide}")
    if ide in TRIAD_BY_IDE:
        require(triad == TRIAD_BY_IDE[ide], errors, f"triad_mode {triad} does not match ide {ide}")
    require(model_tier in MAX_L3_BY_TIER, errors, f"unsupported model_tier: {model_tier}")
    require(isinstance(confidence, (int, float)) and 0 <= confidence <= 1, errors, "confidence must be 0..1")
    expected_tier = tier_for_budget(budget)
    require(expected_tier != "invalid", errors, "context_budget_tokens must be positive integer or null")
    if expected_tier != "invalid":
        require(model_tier == expected_tier, errors, f"model_tier {model_tier} does not match budget {budget}")

    capabilities = data.get("capabilities")
    require(isinstance(capabilities, dict), errors, "capabilities must be object")
    capabilities = capabilities if isinstance(capabilities, dict) else {}
    for capability in ("read", "write", "shell", "subagents", "hooks_or_mcp", "network"):
        require(isinstance(capabilities.get(capability), bool), errors, f"capabilities.{capability} must be boolean")
    if triad == "full":
        require(capabilities.get("subagents") is True, errors, "full triad requires subagents")
        require(capabilities.get("hooks_or_mcp") is True, errors, "full triad requires hooks_or_mcp")

    signals = data.get("signals")
    require(isinstance(signals, list) and len(signals) >= 3, errors, "signals must contain at least 3 entries")
    signal_ids: set[str] = set()
    if isinstance(signals, list):
        for index, signal in enumerate(signals):
            require(isinstance(signal, dict), errors, f"signal {index} must be object")
            if not isinstance(signal, dict):
                continue
            for field in ("id", "kind", "source", "value", "evidence_tag"):
                require(field in signal and signal[field] not in ("", None), errors, f"signal {index} missing {field}")
            signal_id = signal.get("id")
            require(isinstance(signal_id, str), errors, f"signal {index} id must be string")
            if isinstance(signal_id, str):
                require(signal_id not in signal_ids, errors, f"duplicate signal id: {signal_id}")
                signal_ids.add(signal_id)
            tag = signal.get("evidence_tag")
            require(tag in ALLOWED_TAGS, errors, f"signal {signal_id} has unsupported evidence tag {tag}")
            source = str(signal.get("source", "")).lower()
            for fragment in REJECTED_SOURCE_FRAGMENTS:
                require(fragment not in source, errors, f"signal {signal_id} uses rejected source fragment: {fragment}")

    decisions = data.get("decisions")
    require(isinstance(decisions, list) and len(decisions) >= 2, errors, "decisions must contain at least 2 entries")
    if isinstance(decisions, list):
        for index, decision in enumerate(decisions):
            require(isinstance(decision, dict), errors, f"decision {index} must be object")
            if not isinstance(decision, dict):
                continue
            require(decision.get("evidence_tag") in ALLOWED_TAGS, errors, f"decision {index} has unsupported evidence tag")
            refs = decision.get("evidence_ids")
            require(isinstance(refs, list) and refs, errors, f"decision {index} missing evidence_ids")
            if isinstance(refs, list):
                for ref in refs:
                    require(ref in signal_ids, errors, f"decision {index} references unknown signal {ref}")

    conflicts = data.get("conflicts")
    require(isinstance(conflicts, list), errors, "conflicts must be list")
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    validation = validation if isinstance(validation, dict) else {}
    status = validation.get("status")
    require(status in {"pass", "warn", "block"}, errors, f"unsupported validation status: {status}")
    checks = validation.get("checks")
    require(isinstance(checks, list), errors, "validation.checks must be list")
    if isinstance(checks, list):
        require(REQUIRED_CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")
    if isinstance(conflicts, list) and conflicts:
        require(status != "pass", errors, "conflicts cannot produce pass status")
        if isinstance(confidence, (int, float)):
            require(confidence <= 0.89, errors, "conflicts require confidence <= 0.89")
    elif status == "pass" and isinstance(confidence, (int, float)):
        require(confidence >= 0.9, errors, "pass status requires confidence >= 0.9")

    loading_plan = data.get("loading_plan")
    require(isinstance(loading_plan, list) and loading_plan, errors, "loading_plan must be non-empty list")
    l3_count = 0
    if isinstance(loading_plan, list):
        for index, item in enumerate(loading_plan):
            require(isinstance(item, dict), errors, f"loading_plan {index} must be object")
            if not isinstance(item, dict):
                continue
            resource = str(item.get("resource", "")).strip()
            level = item.get("level")
            require(resource != "", errors, f"loading_plan {index} missing resource")
            require(level in VALID_LEVELS, errors, f"loading_plan {index} invalid level {level}")
            refs = item.get("evidence_ids")
            require(isinstance(refs, list) and refs, errors, f"loading_plan {index} missing evidence_ids")
            if isinstance(refs, list):
                for ref in refs:
                    require(ref in signal_ids, errors, f"loading_plan {index} references unknown signal {ref}")
            resource_key = resource.lower()
            require(resource_key not in FORBIDDEN_RESOURCES, errors, f"forbidden resource: {resource}")
            if level == "L3":
                l3_count += 1
                forbidden_for_tier = FORBIDDEN_L3_BY_TIER.get(str(model_tier), set())
                require(resource_key not in forbidden_for_tier, errors, f"{model_tier} tier cannot load {resource} at L3")
    max_l3 = MAX_L3_BY_TIER.get(str(model_tier), 0)
    require(l3_count <= max_l3, errors, f"too many L3 resources for tier {model_tier}: {l3_count}>{max_l3}")

    recommendations = data.get("recommendations")
    require(isinstance(recommendations, list) and recommendations, errors, "recommendations must be non-empty list")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_environment_detection_report.py <report.json>", file=sys.stderr)
        return 2
    report_path = Path(argv[1])
    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"report={report_path.name} status=fail errors=1")
        print(f"ERROR invalid json: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print(f"report={report_path.name} status=fail errors=1")
        print("ERROR report must be object", file=sys.stderr)
        return 1
    errors = validate_report(data)
    status = "pass" if not errors else "fail"
    print(f"report={report_path.name} status={status} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
