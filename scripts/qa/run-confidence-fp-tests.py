#!/usr/bin/env python3
"""Confidence calibration + stratified sampling + false-positive criteria checks
(Katas 29 & 30). Stdlib only; deterministic; CI-safe (no model calls).

Validates two things:
  1. The reliability/schema artifacts that back the katas exist and are well-formed.
  2. The reference algorithms behave as the katas require:
     - calibration buckets raw confidence against a labeled set (raw != truth);
     - stratified sampling draws proportionally per segment (not uniform);
     - false-positive criteria are categorical with positive AND negative examples.

Exit non-zero on any failure.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True,
                         text=True, stdout=subprocess.PIPE).stdout.strip()
    return Path(out)


# --- Kata 29: calibration -------------------------------------------------

def calibrate(predictions, labeled_set, thresholds=(0.5, 0.7, 0.9)):
    """Group predictions into confidence buckets and compute empirical accuracy
    per bucket. Returns {bucket_floor: accuracy or None}."""
    buckets = {t: [] for t in thresholds}
    truth = {row["id"]: row["correct"] for row in labeled_set}
    for pred in predictions:
        conf = pred["field_confidence"]
        floor = max([t for t in thresholds if conf >= t], default=None)
        if floor is not None and pred["id"] in truth:
            buckets[floor].append(truth[pred["id"]])
    return {t: (sum(v) / len(v) if v else None) for t, v in buckets.items()}


# --- Kata 29: stratified sampling ----------------------------------------

def stratified_sample(extractions, n_per_type=2):
    """Sample proportionally per document_type (NOT uniform), so minority types
    are represented. Deterministic: takes the first n per type."""
    by_type = defaultdict(list)
    for e in extractions:
        by_type[e["doc_type"]].append(e)
    sample = []
    for _, items in sorted(by_type.items()):
        sample.extend(items[:n_per_type])
    return sample


# --- Kata 30: false-positive criteria ------------------------------------

def criteria_are_categorical(criteria):
    """A valid FP-reduction criterion is categorical with a positive AND a
    negative example (not a vague 'be conservative')."""
    problems = []
    for c in criteria:
        if not c.get("rule_id"):
            problems.append("criterion missing rule_id")
        if not c.get("positive_example"):
            problems.append(f"{c.get('rule_id','?')}: missing positive_example")
        if not c.get("negative_example"):
            problems.append(f"{c.get('rule_id','?')}: missing negative_example")
        vague = {"be conservative", "high confidence", "only report important"}
        if str(c.get("rule_id", "")).lower() in vague:
            problems.append(f"{c['rule_id']}: vague, not categorical")
    return problems


def main() -> int:
    root = repo_root()
    failures: list[str] = []

    # 1. Artifacts exist + valid JSON.
    for rel in ["references/schemas/annotations.schema.json",
                "references/schemas/annotations.example.json",
                "references/guardrails/tool-policy.json"]:
        path = root / rel
        if not path.exists():
            failures.append(f"missing artifact: {rel}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            failures.append(f"invalid JSON {rel}: {exc}")

    # 2. Calibration: raw confidence is NOT the same as empirical accuracy.
    preds = [{"id": "a", "field_confidence": 0.95}, {"id": "b", "field_confidence": 0.95},
             {"id": "c", "field_confidence": 0.6}]
    labels = [{"id": "a", "correct": 1}, {"id": "b", "correct": 0}, {"id": "c", "correct": 1}]
    cal = calibrate(preds, labels)
    if cal[0.9] is None or cal[0.9] >= 0.95:
        failures.append(f"calibration should expose 0.95-raw bucket as <0.95 empirical, got {cal[0.9]}")

    # 3. Stratified sampling covers minority segments.
    extractions = ([{"doc_type": "invoice", "id": i} for i in range(10)] +
                   [{"doc_type": "receipt", "id": 100}])
    sample = stratified_sample(extractions, n_per_type=2)
    types = {s["doc_type"] for s in sample}
    if "receipt" not in types:
        failures.append("stratified sample dropped minority segment 'receipt'")

    # 4. FP criteria must be categorical with +/- examples.
    good = [{"rule_id": "security.hardcoded_secret",
             "positive_example": "OPENAI_KEY='sk-abc'",
             "negative_example": "OPENAI_KEY=os.environ['OPENAI_KEY']"}]
    bad = [{"rule_id": "be conservative"}]
    if criteria_are_categorical(good):
        failures.append("valid categorical criteria flagged as invalid")
    if not criteria_are_categorical(bad):
        failures.append("vague criteria 'be conservative' should be rejected")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1
    print("OK: confidence calibration, stratified sampling, and FP-criteria checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
