#!/usr/bin/env python3
"""Validate deterministic AI documentation packets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_fields(errors: list[str], obj: Any, path: str, fields: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field}")


def validate_safe_path(errors: list[str], value: Any, path: str, policy: dict[str, Any]) -> None:
    if not is_non_empty_string(value):
        errors.append(f"{path}: must be a non-empty string")
        return
    text = str(value)
    parts = Path(text).parts
    if Path(text).is_absolute():
        errors.append(f"{path}: must be relative")
    for segment in policy["forbidden_segments"]:
        if segment in parts or text.startswith(f"{segment}/"):
            errors.append(f"{path}: contains forbidden segment {segment}")
    exact_ok = text in set(policy["allowed_exact_paths"])
    prefix_ok = any(text.startswith(prefix) for prefix in policy["allowed_prefixes"])
    if not exact_ok and not prefix_ok:
        errors.append(f"{path}: must be README.md, CHANGELOG.md, or under docs/ or api/")


def validate_evidence(
    packet: dict[str, Any],
    errors: list[str],
    source_types: set[str],
) -> set[str]:
    evidence = packet.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence: must be a non-empty list")
        return set()
    allowed_tags = {"[EXPLICIT]", "[INFERRED]", "[OPEN]"}
    seen: set[str] = set()
    for index, item in enumerate(evidence):
        path = f"evidence[{index}]"
        require_fields(errors, item, path, ["id", "tag", "source_type", "path", "summary"])
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("id")
        if not is_non_empty_string(evidence_id):
            errors.append(f"{path}.id: must be a non-empty string")
        elif evidence_id in seen:
            errors.append(f"{path}.id: duplicate evidence id {evidence_id}")
        else:
            seen.add(evidence_id)
        if item.get("tag") not in allowed_tags:
            errors.append(f"{path}.tag: must be one of {sorted(allowed_tags)}")
        if item.get("source_type") not in source_types:
            errors.append(f"{path}.source_type: must be one of {sorted(source_types)}")
        for field in ("path", "summary"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be a non-empty string")
    return seen


def validate_refs(errors: list[str], refs: Any, known_evidence: set[str], path: str) -> None:
    if not isinstance(refs, list) or not refs:
        errors.append(f"{path}: must be a non-empty list")
        return
    for ref in refs:
        if ref not in known_evidence:
            errors.append(f"{path}: unknown evidence id {ref}")


def validate_project(packet: dict[str, Any], errors: list[str]) -> None:
    project = packet.get("project")
    require_fields(errors, project, "project", ["name", "documentation_mode", "primary_audience"])
    if not isinstance(project, dict):
        return
    if not is_non_empty_string(project.get("name")):
        errors.append("project.name: must be a non-empty string")
    if project.get("documentation_mode") not in {"create", "update", "audit"}:
        errors.append("project.documentation_mode: must be create, update, or audit")
    if not is_non_empty_string(project.get("primary_audience")):
        errors.append("project.primary_audience: must be a non-empty string")


def validate_source_inventory(
    packet: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    source_types: set[str],
    source_statuses: set[str],
) -> None:
    inventory = packet.get("source_inventory")
    if not isinstance(inventory, list) or not inventory:
        errors.append("source_inventory: must be a non-empty list")
        return
    for index, item in enumerate(inventory):
        path = f"source_inventory[{index}]"
        require_fields(errors, item, path, ["path", "source_type", "status", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if not is_non_empty_string(item.get("path")):
            errors.append(f"{path}.path: must be a non-empty string")
        if item.get("source_type") not in source_types:
            errors.append(f"{path}.source_type: must be one of {sorted(source_types)}")
        if item.get("status") not in source_statuses:
            errors.append(f"{path}.status: must be one of {sorted(source_statuses)}")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")


def validate_targets(
    packet: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    doc_types: set[str],
    audiences: set[str],
    freshness: set[str],
    path_policy: dict[str, Any],
) -> set[str]:
    targets = packet.get("documentation_targets")
    if not isinstance(targets, list) or not targets:
        errors.append("documentation_targets: must be a non-empty list")
        return set()
    target_types: set[str] = set()
    for index, item in enumerate(targets):
        path = f"documentation_targets[{index}]"
        require_fields(errors, item, path, ["doc_type", "output_path", "audience", "freshness_policy", "required_sections", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        doc_type = item.get("doc_type")
        if doc_type not in doc_types:
            errors.append(f"{path}.doc_type: must be one of {sorted(doc_types)}")
        else:
            target_types.add(str(doc_type))
        validate_safe_path(errors, item.get("output_path"), f"{path}.output_path", path_policy)
        if item.get("audience") not in audiences:
            errors.append(f"{path}.audience: must be one of {sorted(audiences)}")
        if item.get("freshness_policy") not in freshness:
            errors.append(f"{path}.freshness_policy: must be one of {sorted(freshness)}")
        if not isinstance(item.get("required_sections"), list) or not item["required_sections"]:
            errors.append(f"{path}.required_sections: must be a non-empty list")
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return target_types


def validate_sections(
    packet: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    doc_types: set[str],
    target_types: set[str],
) -> None:
    sections = packet.get("generated_sections")
    if not isinstance(sections, list) or not sections:
        errors.append("generated_sections: must be a non-empty list")
        return
    section_target_types: set[str] = set()
    for index, item in enumerate(sections):
        path = f"generated_sections[{index}]"
        require_fields(errors, item, path, ["target_doc_type", "heading", "content_summary", "source_evidence_ids", "validation_status"])
        if not isinstance(item, dict):
            continue
        doc_type = item.get("target_doc_type")
        if doc_type not in doc_types:
            errors.append(f"{path}.target_doc_type: must be one of {sorted(doc_types)}")
        elif doc_type not in target_types:
            errors.append(f"{path}.target_doc_type: has no matching documentation target")
        else:
            section_target_types.add(str(doc_type))
        for field in ("heading", "content_summary"):
            if not is_non_empty_string(item.get(field)):
                errors.append(f"{path}.{field}: must be a non-empty string")
        validate_refs(errors, item.get("source_evidence_ids"), known_evidence, f"{path}.source_evidence_ids")
        if item.get("validation_status") not in {"ready", "gap", "block"}:
            errors.append(f"{path}.validation_status: must be ready, gap, or block")
    missing_sections = target_types - section_target_types
    if missing_sections:
        errors.append(f"generated_sections: missing section coverage for {sorted(missing_sections)}")


def validate_gaps(
    packet: dict[str, Any],
    errors: list[str],
    known_evidence: set[str],
    doc_types: set[str],
    severities: set[str],
) -> bool:
    gaps = packet.get("gap_analysis")
    if not isinstance(gaps, list):
        errors.append("gap_analysis: must be a list")
        return False
    has_blocking_gap = False
    for index, item in enumerate(gaps):
        path = f"gap_analysis[{index}]"
        require_fields(errors, item, path, ["id", "severity", "target_doc_type", "description", "blocking", "evidence_ids"])
        if not isinstance(item, dict):
            continue
        if not is_non_empty_string(item.get("id")):
            errors.append(f"{path}.id: must be a non-empty string")
        if item.get("severity") not in severities:
            errors.append(f"{path}.severity: must be one of {sorted(severities)}")
        if item.get("target_doc_type") not in doc_types:
            errors.append(f"{path}.target_doc_type: must be one of {sorted(doc_types)}")
        if not is_non_empty_string(item.get("description")):
            errors.append(f"{path}.description: must be a non-empty string")
        if not isinstance(item.get("blocking"), bool):
            errors.append(f"{path}.blocking: must be boolean")
        elif item["blocking"]:
            has_blocking_gap = True
        validate_refs(errors, item.get("evidence_ids"), known_evidence, f"{path}.evidence_ids")
    return has_blocking_gap


def validate_validation(packet: dict[str, Any], errors: list[str], required_checks: set[str], has_blocking_gap: bool) -> None:
    validation = packet.get("validation")
    require_fields(errors, validation, "validation", ["status", "checks"])
    if not isinstance(validation, dict):
        return
    status = validation.get("status")
    if status not in {"pass", "warn", "block"}:
        errors.append("validation.status: must be pass, warn, or block")
    if has_blocking_gap and status == "pass":
        errors.append("validation.status: cannot be pass when blocking gaps exist")
    checks = validation.get("checks")
    if not isinstance(checks, list):
        errors.append("validation.checks: must be a list")
    else:
        missing = required_checks - set(checks)
        if missing:
            errors.append(f"validation.checks: missing required checks {sorted(missing)}")


def validate_packet(packet_path: Path) -> list[str]:
    errors: list[str] = []
    packet = load_json(packet_path)
    if not isinstance(packet, dict):
        return ["packet: must be a JSON object"]

    contract = load_json(ASSET_DIR / "documentation-contract.json")
    source_policy = load_json(ASSET_DIR / "source-policy.json")
    doc_policy = load_json(ASSET_DIR / "doc-type-policy.json")
    gap_policy = load_json(ASSET_DIR / "gap-policy.json")
    path_policy = load_json(ASSET_DIR / "path-policy.json")

    require_fields(errors, packet, "packet", contract["required_top_level_fields"])
    if packet.get("schema") != contract["report_schema"]:
        errors.append(f"schema: must be {contract['report_schema']}")

    source_types = set(source_policy["allowed_source_types"])
    known_evidence = validate_evidence(packet, errors, source_types)
    validate_project(packet, errors)
    validate_source_inventory(packet, errors, known_evidence, source_types, set(source_policy["allowed_statuses"]))
    target_types = validate_targets(
        packet=packet,
        errors=errors,
        known_evidence=known_evidence,
        doc_types=set(doc_policy["allowed_doc_types"]),
        audiences=set(doc_policy["allowed_audiences"]),
        freshness=set(doc_policy["allowed_freshness_policies"]),
        path_policy=path_policy,
    )
    validate_sections(packet, errors, known_evidence, set(doc_policy["allowed_doc_types"]), target_types)
    has_blocking_gap = validate_gaps(packet, errors, known_evidence, set(doc_policy["allowed_doc_types"]), set(gap_policy["allowed_severities"]))
    validate_validation(packet, errors, set(contract["required_validation_checks"]), has_blocking_gap)

    if not isinstance(packet.get("risks"), list):
        errors.append("risks: must be a list")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI documentation packet")
    parser.add_argument("packet", help="Path to a packet JSON fixture")
    args = parser.parse_args()

    packet_path = Path(args.packet)
    try:
        errors = validate_packet(packet_path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {packet_path}: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR {packet_path}: {error}", file=sys.stderr)
        return 1

    print(f"packet={packet_path.name} status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
