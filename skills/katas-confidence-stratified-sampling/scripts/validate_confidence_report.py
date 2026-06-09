#!/usr/bin/env python3
"""Validate deterministic confidence calibration reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.katas-confidence-stratified-sampling.report.v1"
REQUIRED_TOP = {
    "schema",
    "skill",
    "extraction_task",
    "labeled_validation_set",
    "calibration",
    "sampling",
    "accuracy_report",
    "routing",
    "evidence",
    "validation",
    "risks",
}
TAGS = {"[CODIGO]", "[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]"}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "labeled_validation_set",
    "calibration_buckets",
    "stratified_sampling",
    "segmented_accuracy",
    "calibrated_routing",
    "evidence_required",
}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def object_at(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    require(isinstance(value, dict), errors, f"{key} must be object")
    return value if isinstance(value, dict) else {}


def objects(value: Any, ctx: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{ctx}[{index}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def text_list(value: Any, ctx: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for index, item in enumerate(value):
        require(is_text(item), errors, f"{ctx}[{index}] must be non-empty string")
        if is_text(item):
            out.append(item)
    return out


def is_probability(value: Any) -> bool:
    return isinstance(value, (int, float)) and 0 <= float(value) <= 1


def validate_labeled_set(data: dict[str, Any], errors: list[str]) -> tuple[set[str], set[str]]:
    labeled = object_at(data, "labeled_validation_set", errors)
    require(isinstance(labeled.get("size"), int) and labeled.get("size") > 0, errors, "labeled_validation_set.size must be positive")
    fields = set(text_list(labeled.get("fields"), "labeled_validation_set.fields", errors))
    doc_types = set(text_list(labeled.get("document_types"), "labeled_validation_set.document_types", errors))
    require(bool(fields), errors, "labeled_validation_set.fields required")
    require(bool(doc_types), errors, "labeled_validation_set.document_types required")
    return fields, doc_types


def validate_calibration(data: dict[str, Any], errors: list[str]) -> None:
    calibration = object_at(data, "calibration", errors)
    require(calibration.get("method") == "empirical-bucket-calibration", errors, "calibration.method invalid")
    require(calibration.get("uses_raw_confidence_for_routing") is False, errors, "raw confidence cannot be used for routing")
    buckets = objects(calibration.get("buckets"), "calibration.buckets", errors)
    require(bool(buckets), errors, "calibration.buckets required")
    for index, bucket in enumerate(buckets):
        ctx = f"calibration.buckets[{index}]"
        require(is_text(bucket.get("bucket")), errors, f"{ctx}.bucket required")
        require(isinstance(bucket.get("sample_count"), int) and bucket.get("sample_count") > 0, errors, f"{ctx}.sample_count must be positive")
        require(is_probability(bucket.get("empirical_accuracy")), errors, f"{ctx}.empirical_accuracy must be 0..1")
        require(is_probability(bucket.get("calibrated_confidence")), errors, f"{ctx}.calibrated_confidence must be 0..1")


def validate_sampling(data: dict[str, Any], doc_types: set[str], errors: list[str]) -> None:
    sampling = object_at(data, "sampling", errors)
    require(sampling.get("strategy") == "stratified", errors, "sampling.strategy must be stratified")
    require(sampling.get("random_total_only") is False, errors, "sampling.random_total_only must be false")
    require(sampling.get("includes_minority_segments") is True, errors, "sampling.includes_minority_segments must be true")
    strata = objects(sampling.get("strata"), "sampling.strata", errors)
    require(bool(strata), errors, "sampling.strata required")
    covered_doc_types: set[str] = set()
    for index, stratum in enumerate(strata):
        ctx = f"sampling.strata[{index}]"
        doc_type = stratum.get("document_type")
        covered_doc_types.add(doc_type) if isinstance(doc_type, str) else None
        require(doc_type in doc_types, errors, f"{ctx}.document_type unknown")
        require(is_text(stratum.get("score_bucket")), errors, f"{ctx}.score_bucket required")
        sample_size = stratum.get("sample_size")
        population_size = stratum.get("population_size")
        require(isinstance(sample_size, int) and sample_size > 0, errors, f"{ctx}.sample_size must be positive")
        require(isinstance(population_size, int) and population_size >= sample_size, errors, f"{ctx}.population_size invalid")
    require(doc_types.issubset(covered_doc_types), errors, "sampling.strata must cover every document_type")


def validate_accuracy(data: dict[str, Any], fields: set[str], doc_types: set[str], errors: list[str]) -> None:
    report = object_at(data, "accuracy_report", errors)
    require(report.get("aggregate_only") is False, errors, "accuracy_report.aggregate_only must be false")
    rows = objects(report.get("rows"), "accuracy_report.rows", errors)
    require(bool(rows), errors, "accuracy_report.rows required")
    for index, row in enumerate(rows):
        ctx = f"accuracy_report.rows[{index}]"
        require(row.get("document_type") in doc_types, errors, f"{ctx}.document_type unknown")
        require(row.get("field") in fields, errors, f"{ctx}.field unknown")
        require(is_probability(row.get("accuracy")), errors, f"{ctx}.accuracy must be 0..1")
        require(isinstance(row.get("n"), int) and row.get("n") > 0, errors, f"{ctx}.n must be positive")


def validate_routing(data: dict[str, Any], fields: set[str], doc_types: set[str], errors: list[str]) -> None:
    routing = object_at(data, "routing", errors)
    require(routing.get("basis") == "calibrated_confidence", errors, "routing.basis must be calibrated_confidence")
    require(is_probability(routing.get("auto_threshold")), errors, "routing.auto_threshold must be 0..1")
    require(is_probability(routing.get("human_review_threshold")), errors, "routing.human_review_threshold must be 0..1")
    decisions = objects(routing.get("decisions"), "routing.decisions", errors)
    require(bool(decisions), errors, "routing.decisions required")
    for index, decision in enumerate(decisions):
        ctx = f"routing.decisions[{index}]"
        require(decision.get("document_type") in doc_types, errors, f"{ctx}.document_type unknown")
        require(decision.get("field") in fields, errors, f"{ctx}.field unknown")
        require(is_probability(decision.get("calibrated_confidence")), errors, f"{ctx}.calibrated_confidence must be 0..1")
        require(decision.get("route") in {"auto", "human_review", "control_sample"}, errors, f"{ctx}.route invalid")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> None:
    evidence = objects(data.get("evidence"), "evidence", errors)
    require(bool(evidence), errors, "evidence required")
    for index, item in enumerate(evidence):
        ctx = f"evidence[{index}]"
        require(is_text(item.get("claim")), errors, f"{ctx}.claim required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        require(is_text(item.get("source")), errors, f"{ctx}.source required")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = object_at(data, "validation", errors)
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    require(validation.get("offline") is True, errors, "validation.offline must be true")
    require(validation.get("network_required") is False, errors, "validation.network_required must be false")
    require(validation.get("deterministic") is True, errors, "validation.deterministic must be true")
    require(validation.get("uses_randomness") is False, errors, "validation.uses_randomness must be false")
    checks = set(text_list(validation.get("checks"), "validation.checks", errors))
    require(REQUIRED_CHECKS.issubset(checks), errors, "validation.checks missing required checks")


def validate_risks(data: dict[str, Any], errors: list[str]) -> None:
    risks = object_at(data, "risks", errors)
    require(isinstance(risks.get("remaining"), list), errors, "risks.remaining must be list")
    forbidden = set(text_list(risks.get("forbidden_patterns"), "risks.forbidden_patterns", errors))
    require(not {"global_accuracy_only", "raw_confidence_routing", "random_sampling_only"}.intersection(forbidden), errors, "forbidden anti-pattern present")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "katas-confidence-stratified-sampling", errors, "skill must be katas-confidence-stratified-sampling")
    require(is_text(data.get("extraction_task")), errors, "extraction_task required")
    fields, doc_types = validate_labeled_set(data, errors)
    validate_calibration(data, errors)
    validate_sampling(data, doc_types, errors)
    validate_accuracy(data, fields, doc_types, errors)
    validate_routing(data, fields, doc_types, errors)
    validate_evidence(data, errors)
    validate_validation(data, errors)
    validate_risks(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_confidence_report.py <report.json>", file=sys.stderr)
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
