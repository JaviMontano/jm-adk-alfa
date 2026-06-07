#!/usr/bin/env python3
"""Validate deterministic analytics events tracking plans."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def refs(errors: list[str], values: Any, known: set[str], path: str) -> None:
    if not isinstance(values, list) or not values:
        errors.append(f"{path}: must be a non-empty list")
        return
    for value in values:
        if value not in known:
            errors.append(f"{path}: unknown evidence id {value}")


def validate_system(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    system = report.get("system")
    require(errors, system, "system", contract["required_system_fields"])
    if not isinstance(system, dict):
        return
    for field in ("name", "scope"):
        if not is_text(system.get(field)):
            errors.append(f"system.{field}: must be non-empty")
    for field in ("platforms", "destinations"):
        values = system.get(field)
        if not isinstance(values, list) or not values or not all(is_text(value) for value in values):
            errors.append(f"system.{field}: must be a non-empty list of strings")


def validate_evidence(report: dict[str, Any], errors: list[str], policy: dict[str, Any]) -> set[str]:
    items = report.get("evidence")
    if not isinstance(items, list) or not items:
        errors.append("evidence: must be a non-empty list")
        return set()
    allowed = set(policy["allowed_tags"])
    seen: set[str] = set()
    for index, item in enumerate(items):
        path = f"evidence[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if not is_text(evidence_id):
            errors.append(f"{path}.id: must be non-empty")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate {evidence_id}")
        else:
            seen.add(str(evidence_id))
        if item.get("tag") not in allowed:
            errors.append(f"{path}.tag: invalid")
        for field in ("source", "summary"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
    return seen


def validate_taxonomy(report: dict[str, Any], errors: list[str], known_evidence: set[str]) -> set[str]:
    items = report.get("taxonomy")
    if not isinstance(items, list) or not items:
        errors.append("taxonomy: must be a non-empty list")
        return set()
    domains: set[str] = set()
    for index, item in enumerate(items):
        path = f"taxonomy[{index}]"
        require(errors, item, path, ["domain", "purpose", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        domain = item.get("domain")
        if is_text(domain):
            domains.add(str(domain))
        if not is_text(item.get("purpose")):
            errors.append(f"{path}.purpose: must be non-empty")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return domains


def validate_properties(report: dict[str, Any], errors: list[str], policy: dict[str, Any]) -> tuple[set[str], bool]:
    items = report.get("properties")
    if not isinstance(items, list) or not items:
        errors.append("properties: must be a non-empty list")
        return set(), False
    names: set[str] = set()
    has_sensitive = False
    allowed_types = set(policy["allowed_types"])
    allowed_pii = set(policy["allowed_pii"])
    blocked = set(policy["blocked_property_names"])
    for index, item in enumerate(items):
        path = f"properties[{index}]"
        require(errors, item, path, policy["required_property_fields"])
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not is_text(name):
            errors.append(f"{path}.name: must be non-empty")
        else:
            property_name = str(name)
            names.add(property_name)
            if property_name in blocked:
                errors.append(f"{path}.name: blocked raw personal data property")
        if item.get("type") not in allowed_types:
            errors.append(f"{path}.type: invalid")
        if not isinstance(item.get("required"), bool):
            errors.append(f"{path}.required: must be boolean")
        if not is_text(item.get("description")):
            errors.append(f"{path}.description: must be non-empty")
        pii = item.get("pii")
        if pii not in allowed_pii:
            errors.append(f"{path}.pii: invalid")
        elif pii == "sensitive":
            has_sensitive = True
            for field in policy["sensitive_requires"]:
                if not is_text(item.get(field)):
                    errors.append(f"{path}.{field}: required for sensitive properties")
    return names, has_sensitive


def validate_identity(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_properties: set[str], known_evidence: set[str]) -> None:
    identity = report.get("identity")
    require(errors, identity, "identity", policy["required_fields"])
    if not isinstance(identity, dict):
        return
    for field in ("anonymous_id_policy", "user_id_policy", "merge_policy", "deduplication_key"):
        if not is_text(identity.get(field)):
            errors.append(f"identity.{field}: must be non-empty")
    for property_name in policy["required_identity_properties"]:
        if property_name not in known_properties:
            errors.append(f"identity: missing required property {property_name}")
    if policy["authenticated_identity_property"] not in known_properties:
        errors.append(f"identity: missing authenticated property {policy['authenticated_identity_property']}")
    refs(errors, identity.get("evidence_ids"), known_evidence, "identity.evidence_ids")


def validate_events(
    report: dict[str, Any],
    errors: list[str],
    policy: dict[str, Any],
    domains: set[str],
    known_properties: set[str],
    known_evidence: set[str],
) -> set[str]:
    items = report.get("events")
    if not isinstance(items, list) or not items:
        errors.append("events: must be a non-empty list")
        return set()
    pattern = re.compile(policy["event_name_pattern"])
    allowed_actions = set(policy["allowed_actions"])
    blocked_names = set(policy["blocked_names"])
    event_names: set[str] = set()
    for index, item in enumerate(items):
        path = f"events[{index}]"
        require(errors, item, path, policy["required_event_fields"])
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not is_text(name):
            errors.append(f"{path}.name: must be non-empty")
        else:
            event_name = str(name)
            event_names.add(event_name)
            if not pattern.match(event_name):
                errors.append(f"{path}.name: must be lower snake_case object_action")
            if event_name in blocked_names:
                errors.append(f"{path}.name: blocked generic event name")
        domain = item.get("domain")
        if domain not in domains:
            errors.append(f"{path}.domain: unknown")
        action = item.get("action")
        if action not in allowed_actions:
            errors.append(f"{path}.action: invalid")
        elif is_text(name) and not str(name).endswith(str(action)):
            errors.append(f"{path}.name: must end with action {action}")
        for field in ("trigger", "owner"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        platforms = item.get("platforms")
        if not isinstance(platforms, list) or not platforms or not all(is_text(value) for value in platforms):
            errors.append(f"{path}.platforms: must be a non-empty list of strings")
        properties = item.get("properties")
        if not isinstance(properties, list) or not properties:
            errors.append(f"{path}.properties: must be a non-empty list")
        else:
            unknown = [value for value in properties if value not in known_properties]
            if unknown:
                errors.append(f"{path}.properties: unknown properties {unknown}")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return event_names


def validate_tracking_plan(report: dict[str, Any], errors: list[str], policy: dict[str, Any], events: set[str], known_evidence: set[str]) -> None:
    items = report.get("tracking_plan")
    if not isinstance(items, list) or not items:
        errors.append("tracking_plan: must be a non-empty list")
        return
    allowed_phases = set(policy["allowed_rollout_phases"])
    covered: set[str] = set()
    for index, item in enumerate(items):
        path = f"tracking_plan[{index}]"
        require(errors, item, path, policy["required_fields"])
        if not isinstance(item, dict):
            continue
        event_name = item.get("event_name")
        if event_name not in events:
            errors.append(f"{path}.event_name: unknown")
        else:
            covered.add(str(event_name))
        for field in ("destination", "implementation_owner", "qa_method"):
            if not is_text(item.get(field)):
                errors.append(f"{path}.{field}: must be non-empty")
        if item.get("rollout_phase") not in allowed_phases:
            errors.append(f"{path}.rollout_phase: invalid")
        refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    missing = events - covered
    if missing:
        errors.append(f"tracking_plan: missing events {sorted(missing)}")


def validate_governance(report: dict[str, Any], errors: list[str], policy: dict[str, Any], known_evidence: set[str], has_sensitive: bool) -> None:
    governance = report.get("governance")
    require(errors, governance, "governance", policy["required_governance_fields"])
    if not isinstance(governance, dict):
        return
    for field in ("naming_convention", "versioning_policy", "deprecation_policy"):
        if not is_text(governance.get(field)):
            errors.append(f"governance.{field}: must be non-empty")
    if not isinstance(governance.get("privacy_review"), bool):
        errors.append("governance.privacy_review: must be boolean")
    if has_sensitive and governance.get("privacy_review") is not True:
        errors.append("governance.privacy_review: required when sensitive properties exist")
    refs(errors, governance.get("evidence_ids"), known_evidence, "governance.evidence_ids")


def validate_validation(report: dict[str, Any], errors: list[str], contract: dict[str, Any]) -> None:
    validation = report.get("validation")
    require(errors, validation, "validation", ["status", "checks"])
    if not isinstance(validation, dict):
        return
    if validation.get("status") not in set(contract["allowed_validation_statuses"]):
        errors.append("validation.status: invalid")
    checks = validation.get("checks")
    if not isinstance(checks, list):
        errors.append("validation.checks: must be a list")
        return
    missing = set(contract["required_validation_checks"]) - set(checks)
    if missing:
        errors.append(f"validation.checks: missing required checks {sorted(missing)}")


def validate_report(report: dict[str, Any]) -> list[str]:
    contract = load_json(ASSET_DIR / "analytics-events-contract.json")
    naming_policy = load_json(ASSET_DIR / "naming-policy.json")
    property_policy = load_json(ASSET_DIR / "property-policy.json")
    identity_policy = load_json(ASSET_DIR / "identity-policy.json")
    tracking_policy = load_json(ASSET_DIR / "tracking-plan-policy.json")
    evidence_policy = load_json(ASSET_DIR / "evidence-policy.json")
    errors: list[str] = []
    for section in contract["required_sections"]:
        if section not in report:
            errors.append(f"report: missing required section {section}")
    if errors:
        return errors
    validate_system(report, errors, contract)
    known_evidence = validate_evidence(report, errors, evidence_policy)
    domains = validate_taxonomy(report, errors, known_evidence)
    known_properties, has_sensitive = validate_properties(report, errors, property_policy)
    validate_identity(report, errors, identity_policy, known_properties, known_evidence)
    events = validate_events(report, errors, naming_policy, domains, known_properties, known_evidence)
    validate_tracking_plan(report, errors, tracking_policy, events, known_evidence)
    validate_governance(report, errors, tracking_policy, known_evidence, has_sensitive)
    validate_validation(report, errors, contract)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an analytics events JSON tracking plan")
    parser.add_argument("report")
    args = parser.parse_args()
    report_path = Path(args.report)
    try:
        report = load_json(report_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {report_path}: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(report, dict):
        print(f"ERROR {report_path}: root must be an object", file=sys.stderr)
        return 1
    errors = validate_report(report)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(f"report={report_path.name} status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
