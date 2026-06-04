#!/usr/bin/env python3
"""Compile deterministic calibrated evaluation confidence reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_required_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        require(field in obj and obj[field] not in ("", None), f"{label} missing required field: {field}", errors)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(flatten_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(flatten_strings(item))
        return strings
    return []


def validate_labeled_set(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    labeled = as_dict(spec.get("labeledSet"))
    validate_required_fields(labeled, schema["requiredLabeledSetFields"], "labeledSet", errors)
    total = labeled.get("totalExamples")
    require(isinstance(total, int) and total >= policy["labeledSet"]["minTotalExamples"], "labeledSet.totalExamples below minimum", errors)
    require(labeled.get("labelField"), "labeledSet.labelField must be non-empty", errors)
    strata = [as_dict(item) for item in as_list(labeled.get("strata"))]
    require(bool(strata), "labeledSet.strata must be non-empty", errors)
    counted = 0
    seen: set[str] = set()
    for index, stratum in enumerate(strata, start=1):
        label = f"stratum {index}"
        validate_required_fields(stratum, schema["requiredStratumFields"], label, errors)
        name = str(stratum.get("name", ""))
        require(name not in seen, f"duplicate stratum: {name}", errors)
        seen.add(name)
        examples = stratum.get("examples")
        positive = stratum.get("positive")
        negative = stratum.get("negative")
        require(isinstance(examples, int) and examples >= policy["labeledSet"]["minExamplesPerStratum"], f"{label}.examples below minimum", errors)
        require(isinstance(positive, int) and isinstance(negative, int), f"{label} positive/negative must be integers", errors)
        if isinstance(examples, int) and isinstance(positive, int) and isinstance(negative, int):
            require(positive + negative == examples, f"{label} positive + negative must equal examples", errors)
            require(positive > 0 and negative > 0, f"{label} must contain both labels", errors)
            counted += examples
    if isinstance(total, int):
        require(counted == total, "sum of stratum examples must equal totalExamples", errors)


def validate_sampling(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    sampling = as_dict(spec.get("sampling"))
    labeled = as_dict(spec.get("labeledSet"))
    validate_required_fields(sampling, schema["requiredSamplingFields"], "sampling", errors)
    require(sampling.get("method") == policy["sampling"]["requiredMethod"], "sampling.method must be stratified", errors)
    require(sampling.get("stratificationField") == labeled.get("stratificationField"), "sampling field must match labeledSet stratificationField", errors)
    minimum = sampling.get("perStratumMinimum")
    require(isinstance(minimum, int) and minimum >= policy["labeledSet"]["minExamplesPerStratum"], "sampling.perStratumMinimum below policy minimum", errors)


def validate_calibration(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    calibration = as_dict(spec.get("calibration"))
    validate_required_fields(calibration, schema["requiredCalibrationFields"], "calibration", errors)
    require(calibration.get("method") in policy["calibration"]["allowedMethods"], "calibration.method unsupported", errors)
    require(calibration.get("rawScoreField") != calibration.get("calibratedScoreField"), "raw and calibrated score fields must differ", errors)
    bins = [as_dict(item) for item in as_list(calibration.get("bins"))]
    require(len(bins) >= 2, "calibration.bins requires at least two bins", errors)
    last_upper = -1.0
    for index, bin_item in enumerate(bins, start=1):
        label = f"calibration bin {index}"
        validate_required_fields(bin_item, schema["requiredCalibrationBinFields"], label, errors)
        raw_upper = bin_item.get("rawUpper")
        observed = bin_item.get("observedPrecision")
        require(isinstance(raw_upper, (int, float)) and raw_upper > last_upper, f"{label}.rawUpper must be increasing", errors)
        require(isinstance(observed, (int, float)) and 0 <= observed <= 1, f"{label}.observedPrecision must be 0..1", errors)
        if isinstance(raw_upper, (int, float)):
            last_upper = float(raw_upper)


def validate_categories(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    categories = [as_dict(item) for item in as_list(spec.get("categories"))]
    require(bool(categories), "categories must be non-empty", errors)
    disabled = set(str(item) for item in as_list(as_dict(spec.get("decision")).get("disabledCategories")))
    seen: set[str] = set()
    required_severities = set(policy["categories"]["requiredSeverityLevels"])
    for index, category in enumerate(categories, start=1):
        label = f"category {index}"
        validate_required_fields(category, schema["requiredCategoryFields"], label, errors)
        name = str(category.get("name", ""))
        require(name not in seen, f"duplicate category: {name}", errors)
        seen.add(name)
        criteria = as_dict(category.get("severityCriteria"))
        missing = sorted(required_severities - set(criteria.keys()))
        require(not missing, f"{label} missing severity criteria: {', '.join(missing)}", errors)
        positives = as_list(category.get("positiveExamples"))
        negatives = as_list(category.get("negativeExamples"))
        require(len(positives) >= policy["categories"]["minPositiveExamples"], f"{label} needs positive examples", errors)
        require(len(negatives) >= policy["categories"]["minNegativeExamples"], f"{label} needs negative examples", errors)
        fp_rate = category.get("fpRate")
        require(isinstance(fp_rate, (int, float)) and 0 <= fp_rate <= 1, f"{label}.fpRate must be 0..1", errors)
        if isinstance(fp_rate, (int, float)) and fp_rate > policy["categories"]["maxFpRateBeforeDisable"]:
            require(category.get("enabled") is False and name in disabled, f"{label} high-FP category must be disabled", errors)
    for item in disabled:
        require(item in seen, f"disabled category not found: {item}", errors)


def validate_decision(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    decision = as_dict(spec.get("decision"))
    validate_required_fields(decision, schema["requiredDecisionFields"], "decision", errors)
    threshold = decision.get("threshold")
    require(isinstance(threshold, (int, float)), "decision.threshold must be numeric", errors)
    if isinstance(threshold, (int, float)):
        require(policy["calibration"]["minThreshold"] <= threshold <= policy["calibration"]["maxThreshold"], "decision.threshold outside policy range", errors)
    require(decision.get("thresholdOn") == policy["calibration"]["requiredThresholdOn"], "decision.thresholdOn must be calibrated_confidence", errors)


def validate_metrics(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    metrics = as_dict(spec.get("metrics"))
    validate_required_fields(metrics, schema["requiredMetricsFields"], "metrics", errors)
    require(metrics.get("reportAggregateAccuracy") == "secondary", "aggregate accuracy must be secondary", errors)
    require(metrics.get("reportByStratum") is True, "metrics.reportByStratum must be true", errors)
    require(metrics.get("reportFpByCategory") is True, "metrics.reportFpByCategory must be true", errors)


def validate_validation(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    validation = as_dict(spec.get("validation"))
    validate_required_fields(validation, schema["requiredValidationFields"], "validation", errors)
    for field in schema["requiredValidationFields"]:
        require(validation.get(field) is True, f"validation.{field} must be true", errors)


def validate_antipatterns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    joined = "\n".join(flatten_strings(spec)).lower()
    for token in policy["blockedAntiPatterns"]:
        if token in joined:
            errors.append(f"blocked anti-pattern token present: {token}")


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "evaluation-schema.json")
    policy = load_json(ASSET_DIR / "confidence-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "evaluation", errors)
    if errors:
        raise ValueError("\n".join(errors))
    require(nonempty(spec.get("evaluator")), "evaluator must be non-empty", errors)
    validate_labeled_set(spec, schema, policy, errors)
    validate_sampling(spec, schema, policy, errors)
    validate_calibration(spec, schema, policy, errors)
    validate_decision(spec, schema, policy, errors)
    validate_categories(spec, schema, policy, errors)
    validate_metrics(spec, schema, errors)
    validate_validation(spec, schema, errors)
    require(bool(as_list(spec.get("risks"))), "risks requires at least one item", errors)
    validate_antipatterns(spec, policy, errors)
    if errors:
        raise ValueError("\n".join(errors))


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_sampling(spec: dict[str, Any]) -> str:
    labeled = spec["labeledSet"]
    sampling = spec["sampling"]
    lines = [
        f"- Method: `{sampling['method']}` by `{sampling['stratificationField']}`.",
        f"- Minimum per stratum: `{sampling['perStratumMinimum']}`.",
    ]
    for stratum in labeled["strata"]:
        lines.append(f"- `{stratum['name']}`: {stratum['examples']} examples ({stratum['positive']} positive / {stratum['negative']} negative).")
    return "\n".join(lines)


def render_calibration(spec: dict[str, Any]) -> str:
    lines = [f"- Method: `{spec['calibration']['method']}`."]
    for bin_item in spec["calibration"]["bins"]:
        lines.append(f"- raw <= `{bin_item['rawUpper']}` -> observed precision `{bin_item['observedPrecision']}`.")
    return "\n".join(lines)


def render_categories(spec: dict[str, Any]) -> str:
    lines: list[str] = []
    for category in spec["categories"]:
        status = "active" if category["enabled"] else "disabled"
        lines.append(f"### {category['name']} ({status})")
        lines.append("")
        lines.append(f"- FP rate: `{category['fpRate']}`.")
        lines.append(f"- Severity criteria: {', '.join(f'{k}={v}' for k, v in category['severityCriteria'].items())}.")
        lines.append(f"- Positive examples: {', '.join(category['positiveExamples'])}.")
        lines.append(f"- Negative examples: {', '.join(category['negativeExamples'])}.")
        lines.append("")
    return "\n".join(lines).strip()


def render_report(spec: dict[str, Any]) -> str:
    template = (ASSET_DIR / "confidence-report-template.md").read_text(encoding="utf-8")
    labeled = spec["labeledSet"]
    decision = spec["decision"]
    metrics = spec["metrics"]
    return template.format(
        evaluator=spec["evaluator"],
        totalExamples=labeled["totalExamples"],
        stratificationField=labeled["stratificationField"],
        strataNames=", ".join(item["name"] for item in labeled["strata"]),
        calibrationMethod=spec["calibration"]["method"],
        threshold=decision["threshold"],
        thresholdOn=decision["thresholdOn"],
        disabledCategories=", ".join(decision["disabledCategories"]) or "none",
        samplingMarkdown=render_sampling(spec),
        calibrationMarkdown=render_calibration(spec),
        categoryMarkdown=render_categories(spec),
        reportAggregateAccuracy=metrics["reportAggregateAccuracy"],
        reportByStratum=metrics["reportByStratum"],
        reportFpByCategory=metrics["reportFpByCategory"],
        risksMarkdown=bullet_list(spec["risks"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a calibrated evaluation confidence plan")
    parser.add_argument("input", type=Path, help="Path to evaluation confidence JSON spec")
    parser.add_argument("--output", type=Path, help="Write generated report")
    args = parser.parse_args()
    try:
        spec = load_json(args.input)
        validate(spec)
        report = render_report(spec)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
