#!/usr/bin/env python3
"""Validate deterministic structured-output-design packages."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


SKILL = "structured-output-design"
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


def type_has_null(schema: Any) -> bool:
    if not isinstance(schema, dict):
        return False
    field_type = schema.get("type")
    return isinstance(field_type, list) and "null" in field_type and len(field_type) >= 2


def has_forbidden_default(schema: Any, forbidden: list[Any]) -> bool:
    if isinstance(schema, dict):
        if "default" in schema and schema["default"] in forbidden:
            return True
        return any(has_forbidden_default(value, forbidden) for value in schema.values())
    if isinstance(schema, list):
        return any(has_forbidden_default(item, forbidden) for item in schema)
    return False


def schema_valid(
    package: dict[str, Any],
    schema_policy: dict[str, Any],
    nullable_policy: dict[str, Any],
    enum_policy: dict[str, Any],
) -> tuple[dict[str, bool], dict[str, Any]]:
    tool = package.get("tool")
    if not isinstance(tool, dict):
        return {
            "schema_closed": False,
            "required_fields_grounded": False,
            "nullable_union_used": False,
            "enum_escape_present": False,
            "error_channel_present": False,
            "no_false_defaults": False,
        }, {}
    input_schema = tool.get("input_schema")
    controls = package.get("schema_controls")
    if not isinstance(input_schema, dict) or not isinstance(controls, dict):
        return {
            "schema_closed": False,
            "required_fields_grounded": False,
            "nullable_union_used": False,
            "enum_escape_present": False,
            "error_channel_present": False,
            "no_false_defaults": False,
        }, {}
    properties = input_schema.get("properties")
    required = input_schema.get("required")
    required_fields = controls.get("required_fields")
    nullable_fields = controls.get("nullable_fields")
    enum_fields = controls.get("enum_fields")
    error_channel = controls.get("error_channel")

    schema_closed = (
        input_schema.get("type") == schema_policy["root_type"]
        and input_schema.get("additionalProperties") is schema_policy["additional_properties"]
        and isinstance(properties, dict)
        and bool(properties)
    )
    required_fields_grounded = (
        isinstance(required, list)
        and bool(required)
        and isinstance(required_fields, list)
        and set(required) == set(required_fields)
        and isinstance(properties, dict)
        and all(isinstance(field, str) and field in properties for field in required)
        and controls.get("required_fields_grounded") is True
    )
    nullable_union_used = (
        isinstance(nullable_fields, list)
        and isinstance(properties, dict)
        and all(field in properties and type_has_null(properties[field]) for field in nullable_fields)
        and controls.get("nullable_union_used") is True
    )
    no_false_defaults = not has_forbidden_default(input_schema, nullable_policy["forbidden_defaults"]) and controls.get("no_false_defaults") is True

    enum_ok = isinstance(enum_fields, list) and isinstance(properties, dict) and controls.get("enum_escape_present") is True
    if enum_ok:
        for field in enum_fields:
            prop = properties.get(field)
            details = properties.get(f"{field}{enum_policy['details_suffix']}")
            enum_values = prop.get("enum") if isinstance(prop, dict) else None
            if not isinstance(enum_values, list) or not any(value in enum_values for value in enum_policy["escape_values"]):
                enum_ok = False
                break
            if not type_has_null(details):
                enum_ok = False
                break
    error_channel_present = (
        non_empty_string(error_channel)
        and isinstance(properties, dict)
        and error_channel in properties
        and type_has_null(properties[error_channel])
        and controls.get("error_channel_present") is True
    )
    schema_versioned = controls.get("schema_versioned") is True and non_empty_string(input_schema.get("$id"))
    checks = {
        "schema_closed": schema_closed,
        "required_fields_grounded": required_fields_grounded,
        "nullable_union_used": nullable_union_used,
        "enum_escape_present": enum_ok,
        "error_channel_present": error_channel_present,
        "no_false_defaults": no_false_defaults,
        "schema_versioned": schema_versioned,
    }
    return checks, input_schema


def tool_valid(package: dict[str, Any], policy: dict[str, Any], refusal_policy: dict[str, Any]) -> dict[str, bool]:
    tool = package.get("tool")
    if not isinstance(tool, dict):
        return {
            "tool_choice_forced": False,
            "typed_parse_source": False,
            "free_text_fallback_blocked": False,
            "failure_route_present": False,
        }
    name = tool.get("name")
    choice = tool.get("tool_choice")
    consumer = tool.get("consumer")
    tool_choice_forced = (
        non_empty_string(name)
        and isinstance(choice, dict)
        and choice.get("type") == policy["forced_tool_choice"]["type"]
        and choice.get("name") == name
    )
    typed_parse_source = isinstance(consumer, dict) and consumer.get("parse_from") == refusal_policy["parse_from"]
    free_text_fallback_blocked = isinstance(consumer, dict) and consumer.get("free_text_fallback_blocked") is policy["free_text_fallback_blocked"]
    failure_route_present = (
        isinstance(consumer, dict)
        and consumer.get("failure_route") in refusal_policy["allowed_failure_routes"]
        and consumer.get("validate_before_accept") is refusal_policy["validate_before_accept"]
    )
    return {
        "tool_choice_forced": tool_choice_forced,
        "typed_parse_source": typed_parse_source,
        "free_text_fallback_blocked": free_text_fallback_blocked,
        "failure_route_present": failure_route_present,
    }


def test_cases_valid(package: dict[str, Any], refusal_policy: dict[str, Any]) -> bool:
    cases = package.get("test_cases")
    if not isinstance(cases, list) or len(cases) < refusal_policy["minimum_test_cases"]:
        return False
    ids: set[str] = set()
    has_positive = False
    has_negative = False
    for case in cases:
        if not isinstance(case, dict):
            return False
        case_id = case.get("id")
        if not non_empty_string(case_id) or case_id in ids:
            return False
        ids.add(str(case_id))
        if not isinstance(case.get("expected_checks"), list) or not case["expected_checks"]:
            return False
        if case.get("expected_valid") is True:
            has_positive = True
        elif case.get("expected_valid") is False:
            has_negative = True
        else:
            return False
    return has_positive and has_negative


def validate(package: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["package must be a JSON object"]

    contract = asset("structured-output-design-contract.json")["json_contract"]
    schema_policy = asset("json-schema-policy.json")
    nullable_policy = asset("nullable-policy.json")
    enum_policy = asset("enum-escape-policy.json")
    tool_choice_policy = asset("tool-choice-policy.json")
    refusal_policy = asset("refusal-error-policy.json")

    for field in contract["required_top_level_fields"]:
        if field not in package:
            errors.append(f"missing required field: {field}")
    if package.get("schema") != contract["schema_version"]:
        errors.append("schema must be 1")
    if package.get("skill") != SKILL:
        errors.append(f"skill must be {SKILL}")
    if not non_empty_string(package.get("design_id")):
        errors.append("design_id must be non-empty")
    tool = package.get("tool")
    if not isinstance(tool, dict):
        errors.append("tool must be an object")
        tool = {}
    for field in contract["required_tool_fields"]:
        if field not in tool:
            errors.append(f"missing tool field: {field}")

    schema_checks, _input_schema = schema_valid(package, schema_policy, nullable_policy, enum_policy)
    tool_checks = tool_valid(package, tool_choice_policy, refusal_policy)
    tests_ok = test_cases_valid(package, refusal_policy)
    checks = {
        "schema_closed": schema_checks["schema_closed"],
        "required_fields_grounded": schema_checks["required_fields_grounded"],
        "nullable_union_used": schema_checks["nullable_union_used"],
        "enum_escape_present": schema_checks["enum_escape_present"],
        "tool_choice_forced": tool_checks["tool_choice_forced"],
        "typed_parse_source": tool_checks["typed_parse_source"],
        "free_text_fallback_blocked": tool_checks["free_text_fallback_blocked"],
        "error_channel_present": schema_checks["error_channel_present"] and tool_checks["failure_route_present"],
        "no_false_defaults": schema_checks["no_false_defaults"],
        "schema_versioned": schema_checks["schema_versioned"],
        "test_cases_present": tests_ok,
        "deterministic_script_passed": True,
    }

    validation = package.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
    for field, expected in checks.items():
        if not expected:
            errors.append(f"{field} is false")
        if validation.get(field) is not expected:
            errors.append(f"validation.{field} must be {expected}")

    guardian = package.get("guardian")
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
    base = invalid_spec["base_package"]
    invalid_count = 0
    for case in invalid_spec["mutations"]:
        package = copy.deepcopy(base)
        for mutation in case["set"]:
            set_path(package, mutation["path"], mutation["value"])
        if not validate(package):
            raise AssertionError(f"{case['id']} should fail")
        invalid_count += 1
    return valid_count, invalid_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a structured-output-design JSON package")
    parser.add_argument("package", nargs="?", type=Path)
    parser.add_argument("--fixture-suite", type=Path)
    args = parser.parse_args()
    try:
        if args.fixture_suite:
            valid_count, invalid_count = run_fixture_suite(args.fixture_suite)
            print(f"structured-output-design check passed: valid={valid_count} invalid={invalid_count}")
            return 0
        if args.package is None:
            raise ValueError("package path or --fixture-suite is required")
        errors = validate(load_json(args.package))
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {args.package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
