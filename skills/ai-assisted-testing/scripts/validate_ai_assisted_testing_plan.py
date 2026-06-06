#!/usr/bin/env python3
"""Validate AI Assisted Testing plan packets offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.ai-assisted-testing.plan.v1"
REQUIRED_TOP = {
    "schema",
    "target",
    "scope",
    "evidence",
    "candidate_tests",
    "coverage_plan",
    "fuzzing_plan",
    "mutation_plan",
    "risks",
    "validation",
}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
TEST_TYPES = {"unit", "integration", "property", "fuzz", "mutation", "regression"}
STATUSES = {"proposed", "generated", "executed"}
CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "test_oracles",
    "evidence_required",
    "bounded_fuzzing",
    "mutation_contract",
    "coverage_targets",
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


def percent(value: Any) -> bool:
    return isinstance(value, (int, float)) and 0 <= value <= 100


def validate_evidence(data: dict[str, Any], errors: list[str]) -> set[str]:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    evidence_ids: set[str] = set()
    for item in evidence:
        eid = item.get("id")
        require(isinstance(eid, str) and bool(eid), errors, "evidence id required")
        if isinstance(eid, str):
            require(eid not in evidence_ids, errors, f"duplicate evidence id {eid}")
            evidence_ids.add(eid)
        require(item.get("tag") in TAGS, errors, f"evidence {eid} invalid tag")
        require(bool(item.get("source")), errors, f"evidence {eid} source required")
        require(bool(item.get("summary")), errors, f"evidence {eid} summary required")
    return evidence_ids


def validate_candidate_tests(data: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    tests = objects(data.get("candidate_tests"), "candidate_tests", errors)
    require(bool(tests), errors, "candidate_tests required")
    execution_evidence = {
        item.get("id")
        for item in data.get("evidence", [])
        if isinstance(item, dict) and item.get("kind") == "execution"
    }
    for test in tests:
        tid = test.get("id")
        for field in ("id", "target", "rationale", "oracle"):
            require(bool(test.get(field)), errors, f"candidate test {tid} missing {field}")
        require(test.get("type") in TEST_TYPES, errors, f"candidate test {tid} invalid type")
        require(test.get("status") in STATUSES, errors, f"candidate test {tid} invalid status")
        refs = test.get("evidence_ids")
        require(isinstance(refs, list) and bool(refs), errors, f"candidate test {tid} evidence_ids required")
        if isinstance(refs, list):
            for ref in refs:
                require(ref in evidence_ids, errors, f"candidate test {tid} references unknown evidence {ref}")
            if test.get("status") == "executed":
                require(bool(set(refs) & execution_evidence), errors, f"candidate test {tid} executed without execution evidence")


def validate_coverage(data: dict[str, Any], errors: list[str]) -> None:
    coverage = data.get("coverage_plan")
    require(isinstance(coverage, dict), errors, "coverage_plan must be object")
    if not isinstance(coverage, dict):
        return
    targets = objects(coverage.get("targets"), "coverage_plan.targets", errors)
    require(bool(targets), errors, "coverage_plan.targets required")
    for target in targets:
        name = target.get("file")
        require(bool(name), errors, "coverage target file required")
        current = target.get("current_percent")
        desired = target.get("target_percent")
        require(percent(current), errors, f"coverage {name} current_percent invalid")
        require(percent(desired), errors, f"coverage {name} target_percent invalid")
        if percent(current) and percent(desired):
            require(desired >= current, errors, f"coverage {name} target lower than current")
        require(isinstance(target.get("missing_areas"), list) and target["missing_areas"], errors, f"coverage {name} missing_areas required")


def validate_fuzzing(data: dict[str, Any], errors: list[str]) -> None:
    fuzzing = data.get("fuzzing_plan")
    require(isinstance(fuzzing, dict), errors, "fuzzing_plan must be object")
    if not isinstance(fuzzing, dict):
        return
    enabled = fuzzing.get("enabled")
    require(isinstance(enabled, bool), errors, "fuzzing_plan.enabled must be boolean")
    if not enabled:
        require(bool(fuzzing.get("reason")), errors, "disabled fuzzing_plan requires reason")
        return
    for field in ("domain", "safety_boundary", "target_environment", "oracle"):
        require(bool(fuzzing.get(field)), errors, f"fuzzing_plan.{field} required")
    require(isinstance(fuzzing.get("seeds"), list) and fuzzing["seeds"], errors, "fuzzing_plan.seeds required")
    iterations = fuzzing.get("iterations")
    timeout = fuzzing.get("timeout_seconds")
    require(isinstance(iterations, int) and 1 <= iterations <= 10000, errors, "fuzzing_plan.iterations must be 1..10000")
    require(isinstance(timeout, int) and 1 <= timeout <= 300, errors, "fuzzing_plan.timeout_seconds must be 1..300")
    environment = str(fuzzing.get("target_environment", "")).lower()
    require(environment not in {"production", "prod"}, errors, "fuzzing_plan target_environment must not be production")


def validate_mutation(data: dict[str, Any], errors: list[str]) -> None:
    mutation = data.get("mutation_plan")
    require(isinstance(mutation, dict), errors, "mutation_plan must be object")
    if not isinstance(mutation, dict):
        return
    enabled = mutation.get("enabled")
    require(isinstance(enabled, bool), errors, "mutation_plan.enabled must be boolean")
    if not enabled:
        require(bool(mutation.get("reason")), errors, "disabled mutation_plan requires reason")
        return
    require(mutation.get("baseline_status") == "passing", errors, "mutation_plan.baseline_status must be passing")
    require(isinstance(mutation.get("operators"), list) and mutation["operators"], errors, "mutation_plan.operators required")
    require(bool(mutation.get("kill_criteria")), errors, "mutation_plan.kill_criteria required")
    require(bool(mutation.get("surviving_mutant_policy")), errors, "mutation_plan.surviving_mutant_policy required")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(bool(data.get("target")), errors, "target required")
    require(isinstance(data.get("scope"), dict) and bool(data["scope"].get("includes")), errors, "scope.includes required")
    evidence_ids = validate_evidence(data, errors)
    validate_candidate_tests(data, evidence_ids, errors)
    validate_coverage(data, errors)
    validate_fuzzing(data, errors)
    validate_mutation(data, errors)
    require(isinstance(data.get("risks"), list), errors, "risks must be list")
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if isinstance(validation, dict):
        require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
        checks = validation.get("checks")
        require(isinstance(checks, list), errors, "validation.checks must be list")
        if isinstance(checks, list):
            require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_ai_assisted_testing_plan.py <plan.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data if isinstance(data, dict) else {})
    print(f"plan={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
