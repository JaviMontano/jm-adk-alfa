#!/usr/bin/env python3
"""Score professional offers with deterministic acceptance filters.

Input JSON:
{
  "schema": 1,
  "skill": "negociacion-oferta",
  "floor_usd": 7000,
  "exclusive_exception_floor_usd": 10000,
  "evidence": [{"type": "written_offer", "detail": "..."}],
  "offers": [
    {
      "name": "Offer A",
      "monthly_usd": 7600,
      "allows_parallel_streams": true,
      "relocation_ok": true,
      "hustle_culture": false,
      "pivote": {
        "purpose": 8,
        "income": 8,
        "viability": 7,
        "optionality": 7,
        "traction": 8,
        "energy": 7
      },
      "notes": "Scope confirmed in writing."
    }
  ],
  "counterproposal": {
    "target_monthly_usd": 8200,
    "rationale": "Scope includes advisory plus delivery leadership.",
    "competing_offer_claim": false
  }
}

Exit 0 if at least one valid offer passes every filter.
Exit 1 for validation issues or no passing offers.
Exit 3 for missing file or bad JSON.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

PIVOTE_DIMENSIONS = ["purpose", "income", "viability", "optionality", "traction", "energy"]
EVIDENCE_TYPES = {
    "written_offer",
    "recruiter_statement",
    "contract_clause",
    "user_constraint",
    "documented_competing_offer",
    "scope_detail",
    "market_source",
}
PRESSURE_PATTERNS = [
    "ultima oportunidad",
    "solo por hoy",
    "actua ya",
    "antes de que sea tarde",
    "si no aceptan pierden",
]
HUSTLE_PATTERNS = ["24/7", "sin descanso", "no dormir", "always-on", "hustle"]


def normalize(text: str) -> str:
    replacements = str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")
    return text.translate(replacements).lower()


def number(value: Any, field: str, issues: list[str], minimum: float = 0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        issues.append(f"{field} must be numeric")
        return 0.0
    if result < minimum:
        issues.append(f"{field} must be >= {minimum:g}")
    return result


def bool_field(value: Any, field: str, issues: list[str]) -> bool:
    if not isinstance(value, bool):
        issues.append(f"{field} must be boolean")
        return False
    return value


def contains_any(text: str, patterns: list[str]) -> list[str]:
    low = normalize(text)
    return [pattern for pattern in patterns if pattern in low]


def validate_evidence(items: Any) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    if not isinstance(items, list) or not items:
        return [], ["evidence must contain at least one item"]
    clean: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            issues.append(f"evidence[{index}] must be an object")
            continue
        item_type = item.get("type")
        detail = str(item.get("detail", "")).strip()
        if item_type not in EVIDENCE_TYPES:
            issues.append(f"unsupported evidence type: {item_type}")
        if len(detail.split()) < 3:
            issues.append(f"evidence[{index}].detail must be specific")
        clean.append(item)
    return clean, issues


def pivote_score(value: Any, offer_name: str, issues: list[str]) -> tuple[float, bool]:
    if not isinstance(value, dict):
        issues.append(f"{offer_name}.pivote must be an object")
        return 0.0, False
    scores: list[float] = []
    for dim in PIVOTE_DIMENSIONS:
        score = number(value.get(dim), f"{offer_name}.pivote.{dim}", issues, 0)
        if score > 10:
            issues.append(f"{offer_name}.pivote.{dim} must be <= 10")
        scores.append(score)
    avg = sum(scores) / len(PIVOTE_DIMENSIONS)
    passes = avg >= 7 and min(scores) >= 5
    return avg, passes


def evaluate_offer(offer: dict[str, Any], floor: float, exception_floor: float) -> tuple[bool, list[str], float]:
    issues: list[str] = []
    name = str(offer.get("name", "")).strip() or "offer"
    monthly = number(offer.get("monthly_usd"), f"{name}.monthly_usd", issues, 0)
    allows_streams = bool_field(offer.get("allows_parallel_streams"), f"{name}.allows_parallel_streams", issues)
    relocation_ok = bool_field(offer.get("relocation_ok"), f"{name}.relocation_ok", issues)
    hustle = bool_field(offer.get("hustle_culture"), f"{name}.hustle_culture", issues)
    pivote_avg, pivote_pass = pivote_score(offer.get("pivote"), name, issues)
    notes = str(offer.get("notes", ""))

    fails: list[str] = []
    if monthly < floor:
        fails.append("below_floor")
    documented_exception = offer.get("exclusivity_exception") == "documented_exception" and monthly >= exception_floor
    if not allows_streams and not documented_exception:
        fails.append("blocks_parallel_streams")
    if not pivote_pass:
        fails.append("pivote_gate")
    if hustle or contains_any(notes, HUSTLE_PATTERNS):
        fails.append("hustle_culture")
    if not relocation_ok:
        fails.append("relocation_block")

    return not issues and not fails, issues + fails, pivote_avg


def validate_counterproposal(value: Any, evidence: list[dict[str, Any]]) -> list[str]:
    if value in (None, {}):
        return []
    if not isinstance(value, dict):
        return ["counterproposal must be an object"]
    issues: list[str] = []
    text = " ".join(str(value.get(field, "")) for field in ["rationale", "draft", "ask"])
    pressure = contains_any(text, PRESSURE_PATTERNS)
    if pressure:
        issues.append(f"pressure language: {pressure}")
    target = value.get("target_monthly_usd")
    if target is not None:
        number(target, "counterproposal.target_monthly_usd", issues, 0)
    if value.get("competing_offer_claim") is True:
        has_competing = any(item.get("type") == "documented_competing_offer" for item in evidence)
        if not has_competing:
            issues.append("competing_offer_claim requires documented_competing_offer evidence")
    if value.get("market_rate_claim") is True:
        has_market = any(item.get("type") == "market_source" for item in evidence)
        if not has_market:
            issues.append("market_rate_claim requires market_source evidence")
    return issues


def validate_packet(data: dict[str, Any]) -> tuple[list[tuple[str, bool, list[str], float]], list[str]]:
    issues: list[str] = []
    if data.get("schema") != 1:
        issues.append("schema must be 1")
    if data.get("skill") != "negociacion-oferta":
        issues.append("skill must be negociacion-oferta")
    floor = number(data.get("floor_usd"), "floor_usd", issues, 0)
    exception_floor = number(data.get("exclusive_exception_floor_usd", 10000), "exclusive_exception_floor_usd", issues, 0)
    evidence, evidence_issues = validate_evidence(data.get("evidence"))
    issues.extend(evidence_issues)
    offers = data.get("offers")
    if not isinstance(offers, list) or not offers:
        issues.append("offers must contain at least one offer")
        offers = []

    results: list[tuple[str, bool, list[str], float]] = []
    seen: set[str] = set()
    for index, offer in enumerate(offers):
        if not isinstance(offer, dict):
            results.append((f"offer[{index}]", False, ["offer must be an object"], 0.0))
            continue
        name = str(offer.get("name", "")).strip()
        if not name:
            results.append((f"offer[{index}]", False, ["name is required"], 0.0))
            continue
        if name in seen:
            results.append((name, False, ["duplicate offer name"], 0.0))
            continue
        seen.add(name)
        ok, offer_issues, pivote_avg = evaluate_offer(offer, floor, exception_floor)
        results.append((name, ok, offer_issues, pivote_avg))

    issues.extend(validate_counterproposal(data.get("counterproposal"), evidence))
    return results, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Score offers vs deterministic negotiation filters")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: not found: {path}")
        return 3
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: bad JSON: {exc}")
        return 3
    if not isinstance(data, dict):
        print("ERROR: JSON root must be an object")
        return 3

    results, packet_issues = validate_packet(data)
    passing = [(name, pivote) for name, ok, _, pivote in results if ok]

    for name, ok, issues, pivote_avg in results:
        label = "PASS" if ok else "FAIL"
        suffix = "" if ok else f" reasons={','.join(issues)}"
        print(f"{name}: {label} pivote={pivote_avg:.2f}{suffix}")

    if packet_issues:
        print("PACKET ISSUES:")
        for issue in packet_issues:
            print(f"  {issue}")
        return 1

    if not passing:
        print("No offer passes every acceptance filter.")
        return 1

    passing.sort(key=lambda item: item[1], reverse=True)
    print("RANKING:")
    for index, (name, pivote_avg) in enumerate(passing, 1):
        print(f"  {index}. {name} pivote={pivote_avg:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
