#!/usr/bin/env python3
"""Compile deterministic adaptive investigation reports from structured JSON."""

from __future__ import annotations

import argparse
import json
import re
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


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


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


def validate_budget(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    budget = as_dict(spec.get("budget"))
    validate_required_fields(budget, schema["requiredBudgetFields"], "budget", errors)
    total = budget.get("total")
    used = budget.get("used")
    require(isinstance(total, int), "budget.total must be integer", errors)
    require(isinstance(used, int), "budget.used must be integer", errors)
    if isinstance(total, int):
        require(policy["budget"]["minTotal"] <= total <= policy["budget"]["maxTotal"], "budget.total outside policy range", errors)
    if isinstance(total, int) and isinstance(used, int):
        require(0 <= used <= total, "budget.used must be between 0 and total", errors)
    require(budget.get("unit") in policy["budget"]["allowedUnits"], "budget.unit unsupported", errors)


def validate_surface_map(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    entries = [as_dict(item) for item in as_list(spec.get("surfaceMap"))]
    require(len(entries) >= policy["minimums"]["surfaceMapEntries"], "surfaceMap requires at least one entry", errors)
    allowed = set(policy["cheapMapTools"])
    ids: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        label = f"surfaceMap {index}"
        validate_required_fields(entry, schema["requiredSurfaceMapFields"], label, errors)
        ids.add(str(entry.get("id", "")))
        require(entry.get("tool") in allowed, f"{label} must use a cheap map tool", errors)
        require(bool(as_list(entry.get("candidateNodes"))), f"{label} requires candidateNodes", errors)
        require(nonempty(entry.get("evidence")), f"{label} requires evidence", errors)
    require(len(ids) == len(entries), "surfaceMap ids must be unique", errors)


def validate_hypotheses(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> set[str]:
    hypotheses = [as_dict(item) for item in as_list(spec.get("hypotheses"))]
    require(len(hypotheses) >= policy["minimums"]["hypotheses"], "hypotheses requires at least one item", errors)
    statuses = set(policy["allowedHypothesisStatuses"])
    ids: set[str] = set()
    for index, item in enumerate(hypotheses, start=1):
        label = f"hypothesis {index}"
        validate_required_fields(item, schema["requiredHypothesisFields"], label, errors)
        hyp_id = str(item.get("id", ""))
        ids.add(hyp_id)
        require(item.get("status") in statuses, f"{label} status unsupported", errors)
        require(isinstance(item.get("priority"), int), f"{label} priority must be integer", errors)
        require(isinstance(item.get("cost"), int), f"{label} cost must be integer", errors)
        require(bool(as_list(item.get("candidateNodes"))), f"{label} requires candidateNodes", errors)
    require(len(ids) == len(hypotheses), "hypothesis ids must be unique", errors)
    return ids


def validate_deep_dives(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], hypothesis_ids: set[str], errors: list[str]) -> None:
    dives = [as_dict(item) for item in as_list(spec.get("deepDives"))]
    require(len(dives) >= policy["minimums"]["deepDives"], "deepDives requires at least one item", errors)
    require(len(dives) == as_dict(spec.get("budget")).get("used"), "budget.used must equal number of deepDives", errors)
    allowed_tools = set(policy["expensiveDiveTools"])
    effects = set(policy["allowedDeepDiveEffects"])
    ids: set[str] = set()
    for index, item in enumerate(dives, start=1):
        label = f"deepDive {index}"
        validate_required_fields(item, schema["requiredDeepDiveFields"], label, errors)
        ids.add(str(item.get("id", "")))
        require(item.get("hypothesisId") in hypothesis_ids, f"{label} references unknown hypothesis", errors)
        require(item.get("tool") in allowed_tools, f"{label} must use an expensive dive tool", errors)
        require(item.get("effect") in effects, f"{label} effect unsupported", errors)
        require(nonempty(item.get("finding")), f"{label} requires finding", errors)
    require(len(ids) == len(dives), "deepDive ids must be unique", errors)


def validate_replan_log(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], hypothesis_ids: set[str], errors: list[str]) -> None:
    rows = [as_dict(item) for item in as_list(spec.get("replanLog"))]
    triggers = set(policy["allowedReplanTriggers"])
    for index, item in enumerate(rows, start=1):
        label = f"replanLog {index}"
        validate_required_fields(item, schema["requiredReplanFields"], label, errors)
        require(item.get("trigger") in triggers, f"{label} trigger unsupported; replan only allowed on hypothesis_invalidated", errors)
        require(item.get("hypothesisId") in hypothesis_ids, f"{label} references unknown hypothesis", errors)
        require(nonempty(item.get("decision")), f"{label} requires decision", errors)
        require(nonempty(item.get("evidence")), f"{label} requires evidence", errors)


def validate_stop_condition(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    stop = as_dict(spec.get("stopCondition"))
    validate_required_fields(stop, schema["requiredStopConditionFields"], "stopCondition", errors)
    reason = stop.get("reason")
    require(reason in policy["allowedStopReasons"], "stopCondition.reason unsupported", errors)
    if reason == "goal_resolved":
        require(nonempty(spec.get("deliverable")), "goal_resolved requires a deliverable", errors)
    if reason == "budget_exhausted":
        budget = as_dict(spec.get("budget"))
        require(budget.get("used") == budget.get("total"), "budget_exhausted requires used == total", errors)
    require(len(as_list(spec.get("risks"))) >= policy["minimums"]["risks"], "risks requires at least one item", errors)


def validate_antipatterns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    joined = "\n".join(flatten_strings(spec)).lower()
    for token in policy["blockedAntiPatterns"]:
        if re.search(rf"\b{re.escape(token.lower())}\b", joined):
            errors.append(f"blocked anti-pattern token present: {token}")


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "investigation-schema.json")
    policy = load_json(ASSET_DIR / "investigation-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "investigation", errors)
    if errors:
        raise ValueError("\n".join(errors))
    require(nonempty(spec.get("goal")), "goal must be specific", errors)
    validate_budget(spec, schema, policy, errors)
    validate_surface_map(spec, schema, policy, errors)
    hypothesis_ids = validate_hypotheses(spec, schema, policy, errors)
    validate_deep_dives(spec, schema, policy, hypothesis_ids, errors)
    validate_replan_log(spec, schema, policy, hypothesis_ids, errors)
    validate_stop_condition(spec, schema, policy, errors)
    validate_antipatterns(spec, policy, errors)
    if errors:
        raise ValueError("\n".join(errors))


def table(headers: list[str], rows: list[list[Any]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def render_markdown(spec: dict[str, Any]) -> str:
    budget = spec["budget"]
    stop = spec["stopCondition"]
    surface_rows = [
        [item["id"], item["tool"], item["query"], ", ".join(item["candidateNodes"]), item["evidence"]]
        for item in spec["surfaceMap"]
    ]
    hypothesis_rows = [
        [item["id"], item["priority"], item["cost"], item["status"], item["claim"], ", ".join(item["candidateNodes"])]
        for item in spec["hypotheses"]
    ]
    dive_rows = [
        [item["id"], item["hypothesisId"], item["node"], item["tool"], item["effect"], item["finding"]]
        for item in spec["deepDives"]
    ]
    replan_rows = [
        [item["trigger"], item["hypothesisId"], item["decision"], item["evidence"]]
        for item in spec["replanLog"]
    ] or [["none", "n/a", "No hypothesis invalidated.", "Replan not triggered."]]
    return "\n\n".join(
        [
            f"# Adaptive Investigation Report: {spec['goal']}",
            "## Summary\n\n"
            + "\n".join(
                [
                    f"- Budget: `{budget['used']}/{budget['total']} {budget['unit']}`",
                    f"- Stop reason: `{stop['reason']}`",
                    f"- Surface map entries: `{len(spec['surfaceMap'])}`",
                    f"- Hypotheses: `{len(spec['hypotheses'])}`",
                    f"- Deep-dives: `{len(spec['deepDives'])}`",
                    f"- Replans: `{len(spec['replanLog'])}`",
                ]
            ),
            "## Surface Map\n\n" + table(["ID", "Tool", "Query", "Candidate nodes", "Evidence"], surface_rows),
            "## Hypotheses\n\n" + table(["ID", "Priority", "Cost", "Status", "Claim", "Candidate nodes"], hypothesis_rows),
            "## Deep-Dives\n\n" + table(["ID", "Hypothesis", "Node", "Tool", "Effect", "Finding"], dive_rows),
            "## Replan Log\n\n" + table(["Trigger", "Hypothesis", "Decision", "Evidence"], replan_rows),
            "## Deliverable\n\n" + spec["deliverable"],
            "## Risks\n\n" + "\n".join(f"- {risk}" for risk in spec["risks"]),
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an adaptive investigation report")
    parser.add_argument("--input", required=True, help="Path to investigation JSON")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Optional output file")
    args = parser.parse_args()

    try:
        spec = load_json(Path(args.input))
        validate(spec)
        rendered = json.dumps(spec, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else render_markdown(spec)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
