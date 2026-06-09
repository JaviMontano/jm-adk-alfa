#!/usr/bin/env python3
"""Validate deterministic tool-use design reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


GENERIC_MARKERS = (
    "analyzes content",
    "processes the file",
    "does stuff",
    "handles data",
    "works with files",
)
REQUIRED_STRATEGY = ["grep", "read", "edit"]


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def text(value: Any) -> str:
    return str(value or "").strip()


def all_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(all_text(v) for v in value)
    return text(value)


def as_dict(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def as_list(data: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{key} must be a non-empty list")
        return []
    out: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
        else:
            out.append(item)
    return out


def str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [text(item) for item in value if text(item)]


def validate_tool_contracts(contracts: list[dict[str, Any]], errors: list[str]) -> None:
    if len(contracts) < 2:
        errors.append("tool_contracts must contain at least two tools")
    names: list[str] = []
    for index, contract in enumerate(contracts, start=1):
        label = f"tool_contracts[{index}]"
        name = text(contract.get("name"))
        if not name:
            errors.append(f"{label}.name is required")
        if name in names:
            errors.append(f"{label}.name must be unique: {name}")
        names.append(name)
        for key in ("purpose", "input_format"):
            if not text(contract.get(key)):
                errors.append(f"{label}.{key} is required")
        examples = str_list(contract.get("examples"))
        if not examples:
            errors.append(f"{label}.examples must include at least one example")
        boundary = contract.get("boundary")
        if not isinstance(boundary, dict):
            errors.append(f"{label}.boundary must be an object")
            boundary = {}
        for key in ("use_for", "not_for"):
            if not text(boundary.get(key)):
                errors.append(f"{label}.boundary.{key} is required")
        delegates = str_list(boundary.get("delegate_to"))
        if not delegates:
            errors.append(f"{label}.boundary.delegate_to must reference at least one neighboring tool")
        for target in delegates:
            if target not in names and target not in [text(c.get("name")) for c in contracts]:
                errors.append(f"{label}.boundary.delegate_to target missing: {target}")
        if any(marker in all_text(contract).lower() for marker in GENERIC_MARKERS):
            errors.append(f"{label} contains generic description marker")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("skill") != "tool-use-design":
        errors.append("skill must be tool-use-design")

    if any(marker in all_text(data).lower() for marker in GENERIC_MARKERS):
        errors.append("generic description language is forbidden")

    validate_tool_contracts(as_list(data, "tool_contracts", errors), errors)

    overload = as_dict(data, "overload_resolution", errors)
    if text(overload.get("decision")) != "rename_split":
        errors.append("overload_resolution.decision must be rename_split")
    if overload.get("resolved_by_prose") not in (False, None):
        errors.append("overload_resolution.resolved_by_prose must be false")
    split_tools = str_list(overload.get("split_tools"))
    if len(split_tools) < 2:
        errors.append("overload_resolution.split_tools must list at least two tool names")

    strategy = as_dict(data, "repo_strategy", errors)
    if str_list(strategy.get("sequence")) != REQUIRED_STRATEGY:
        errors.append("repo_strategy.sequence must be ['grep', 'read', 'edit']")
    if strategy.get("read_all_upfront") not in (False, None):
        errors.append("repo_strategy.read_all_upfront must be false")
    if strategy.get("glob_all_then_read_all") not in (False, None):
        errors.append("repo_strategy.glob_all_then_read_all must be false")

    edit_safety = as_dict(data, "edit_safety", errors)
    if edit_safety.get("unique_anchor_required") is not True:
        errors.append("edit_safety.unique_anchor_required must be true")
    if text(edit_safety.get("failure_mode")) != "non_unique_anchor":
        errors.append("edit_safety.failure_mode must be non_unique_anchor")
    if text(edit_safety.get("fallback")) != "read_write_full_rewrite":
        errors.append("edit_safety.fallback must be read_write_full_rewrite")

    validation = as_dict(data, "validation", errors)
    if validation.get("offline") is not True:
        errors.append("validation.offline must be true")
    if validation.get("network_required") not in (False, None):
        errors.append("validation.network_required must be false")
    if validation.get("deterministic") is not True:
        errors.append("validation.deterministic must be true")
    if text(validation.get("result")) not in {"pass", "blocked"}:
        errors.append("validation.result must be pass or blocked")
    if errors and text(validation.get("result")) == "pass":
        errors.append("validation.result must not be pass when errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate tool-use-design JSON report")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        data = load_json(Path(args.input))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"tool_use_design_report={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
