#!/usr/bin/env python3
"""Validate deterministic safe-scripting-and-bash reports."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


SKILL = "safe-scripting-and-bash"
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def asset(name: str) -> dict[str, Any]:
    data = load_json(ASSETS_DIR / name)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object")
    return data


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def set_path(data: Any, dotted_path: str, value: Any) -> None:
    cursor = data
    parts = dotted_path.split(".")
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    last = parts[-1]
    if isinstance(cursor, list):
        cursor[int(last)] = value
    else:
        cursor[last] = value


def write_surface_valid(report: dict[str, Any], policy: dict[str, Any]) -> bool:
    surface = report.get("write_surface")
    if not isinstance(surface, dict):
        return False
    for field in policy["required_fields"]:
        if field not in surface:
            return False
    if surface.get("scope") not in policy["allowed_scopes"]:
        return False
    if not isinstance(surface.get("paths"), list):
        return False
    if surface.get("scope") != "read_only" and not surface["paths"]:
        return False
    if surface.get("scope") == "broad_write" and surface.get("overwrites_possible") is True:
        controls = report.get("safety_controls") if isinstance(report.get("safety_controls"), dict) else {}
        return controls.get("force_required_for_overwrite") is True
    return True


def command_contract_valid(report: dict[str, Any]) -> bool:
    contract = report.get("command_contract")
    if not isinstance(contract, dict):
        return False
    if not non_empty_string(contract.get("entrypoint")):
        return False
    if not isinstance(contract.get("arguments"), list):
        return False
    return contract.get("repo_root_detection") is True and contract.get("idempotent") is True


def safety_valid(report: dict[str, Any], dry_policy: dict[str, Any], destructive_policy: dict[str, Any]) -> bool:
    controls = report.get("safety_controls")
    if not isinstance(controls, dict):
        return False
    for flag in dry_policy["required_flags"]:
        if controls.get(flag) is not True:
            return False
    if controls.get("apply_flag") not in dry_policy["allowed_apply_flags"]:
        return False
    if controls.get("force_flag") not in dry_policy["allowed_force_flags"]:
        return False
    dangerous = controls.get("dangerous_patterns")
    if not isinstance(dangerous, list):
        return False
    if any(pattern in destructive_policy["forbidden_patterns"] for pattern in dangerous):
        return False
    secret_controls = set(controls.get("secret_controls", [])) if isinstance(controls.get("secret_controls"), list) else set()
    if not set(destructive_policy["required_secret_controls"]).issubset(secret_controls):
        return False
    return controls.get("network_required") is False


def portability_valid(report: dict[str, Any], policy: dict[str, Any]) -> bool:
    portability = report.get("portability")
    if not isinstance(portability, dict):
        return False
    for flag in policy["required_flags"]:
        if portability.get(flag) is not True:
            return False
    paths = portability.get("literal_paths", [])
    if not isinstance(paths, list):
        return False
    return not any(str(path).startswith(tuple(policy["blocked_path_prefixes"])) for path in paths)


def validation_valid(report: dict[str, Any], policy: dict[str, Any]) -> bool:
    validation = report.get("validation")
    if not isinstance(validation, dict):
        return False
    return all(validation.get(flag) is True for flag in policy["required_flags"])


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    contract = asset("safe-scripting-and-bash-contract.json")["json_contract"]
    write_policy = asset("write-surface-policy.json")
    dry_policy = asset("dry-run-policy.json")
    destructive_policy = asset("destructive-command-policy.json")
    portability_policy = asset("portability-policy.json")
    validation_policy = asset("validation-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in report:
            errors.append(f"missing required field: {field}")
    if report.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if report.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(report.get("script_id")):
        errors.append("script_id must be non-empty")
    if not non_empty_string(report.get("purpose")):
        errors.append("purpose must be non-empty")

    checks = {
        "write_surface_declared": write_surface_valid(report, write_policy),
        "command_contract_complete": command_contract_valid(report),
        "dry_run_and_force_guarded": safety_valid(report, dry_policy, destructive_policy),
        "portability_controls_present": portability_valid(report, portability_policy),
        "offline_validation_present": validation_valid(report, validation_policy),
        "deterministic_script_passed": True,
    }
    for field, ok in checks.items():
        if not ok:
            errors.append(f"{field} is false")

    validation = report.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    for field, expected in checks.items():
        if validation.get(field) is not expected:
            errors.append(f"validation.{field} must be {expected}")

    guardian = report.get("guardian")
    if not isinstance(guardian, dict):
        errors.append("guardian must be an object")
        guardian = {}
    decision = guardian.get("decision")
    if decision not in contract["guardian_decisions"]:
        errors.append("guardian.decision is not allowed")
    if not non_empty_string(guardian.get("reason")):
        errors.append("guardian.reason must be non-empty")
    blocking_needed = any(value is False for value in checks.values())
    if decision == "pass" and blocking_needed:
        errors.append("guardian pass requires all validation flags true")
    if decision == "block" and not blocking_needed:
        errors.append("guardian block requires validation failure")
    return errors


def run_fixture_suite(fixtures_dir: Path) -> tuple[int, int]:
    valid_count = 0
    for fixture in sorted(fixtures_dir.glob("valid-*.json")):
        errors = validate(load_json(fixture))
        if errors:
            raise AssertionError(f"{fixture.name} should pass: {errors}")
        valid_count += 1
    invalid_spec = load_json(fixtures_dir / "invalid-mutations.json")
    base = invalid_spec["base_report"]
    invalid_count = 0
    for case in invalid_spec["mutations"]:
        report = copy.deepcopy(base)
        for mutation in case["set"]:
            set_path(report, mutation["path"], mutation["value"])
        if not validate(report):
            raise AssertionError(f"{case['id']} should fail")
        invalid_count += 1
    return valid_count, invalid_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a safe-scripting-and-bash JSON report")
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--fixture-suite", type=Path)
    args = parser.parse_args()
    try:
        if args.fixture_suite:
            valid_count, invalid_count = run_fixture_suite(args.fixture_suite)
            print(f"safe-scripting-and-bash check passed: valid={valid_count} invalid={invalid_count}")
            return 0
        if args.report is None:
            raise ValueError("report path or --fixture-suite is required")
        errors = validate(load_json(args.report))
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
