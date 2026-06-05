#!/usr/bin/env python3
"""Validate generated outputs against explicit contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "assets" / "evidence-tag-policy.json"
PACKET_SCHEMA = ROOT / "templates" / "schema.json"


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def kebab_case_name(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+)?", name))


def suggest_kebab(name: str) -> str:
    stem = Path(name).stem
    suffix = Path(name).suffix.lower()
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    cleaned = re.sub(r"-+", "-", cleaned) or "artifact"
    return f"{cleaned}{suffix}"


def markdown_sections(text: str) -> set[str]:
    sections: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            sections.add(match.group(1).strip())
    return sections


def make_check(check_id: str, status: str, expected: str, observed: str, repair: str) -> dict:
    return {
        "id": check_id,
        "status": status,
        "expected": expected,
        "observed": observed,
        "repair": repair,
    }


def validation_packet(contract: dict, artifact: str) -> dict:
    return {
        "schema": 1,
        "skill": "output-contract-enforcer",
        "status": "pass",
        "contract_id": str(contract.get("contract_id", "inline-contract")),
        "artifact": artifact,
        "checks": [],
        "violations": [],
        "repair_suggestions": [],
        "evidence": [],
    }


def add_violation(packet: dict, check: dict, violation: str) -> None:
    packet["status"] = "fail"
    packet["violations"].append(violation)
    if check.get("repair") and check["repair"] != "none":
        packet["repair_suggestions"].append(check["repair"])


def validate_packet_shape(packet: dict) -> list[str]:
    schema = load_json(PACKET_SCHEMA)
    missing = [field for field in schema["required_fields"] if field not in packet]
    errors = [f"packet missing required field: {field}" for field in missing]
    if packet.get("status") not in schema["statuses"]:
        errors.append("packet status is invalid")
    for check in packet.get("checks", []):
        if not isinstance(check, dict):
            errors.append("packet check entries must be objects")
            continue
        for field in schema["check_fields"]:
            if field not in check:
                errors.append(f"packet check missing field: {field}")
    return errors


def validate(contract: dict, output_path: Path, artifact_name: str | None) -> dict:
    text = output_path.read_text(encoding="utf-8")
    artifact = artifact_name or str(output_path)
    packet = validation_packet(contract, artifact)
    policy = load_json(POLICY)

    packet["checks"].append(make_check("contract_loaded", "pass", "parseable JSON contract", "contract parsed", "none"))

    expected_format = str(contract.get("format", "unknown"))
    if expected_format == "json":
        try:
            output_json = json.loads(text)
            format_status = "pass"
            observed_format = "json"
        except json.JSONDecodeError as exc:
            output_json = None
            format_status = "fail"
            observed_format = f"invalid json: {exc}"
        check = make_check("format", format_status, "json", observed_format, "Return valid JSON.")
        packet["checks"].append(check)
        if format_status == "fail":
            add_violation(packet, check, "format: output is not valid JSON")
        required = list(contract.get("required_fields", []))
        missing = [field for field in required if not isinstance(output_json, dict) or field not in output_json]
        status = "fail" if missing else "pass"
        check = make_check(
            "required_fields",
            status,
            ", ".join(required) or "none",
            ", ".join(sorted(output_json.keys())) if isinstance(output_json, dict) else "no JSON object",
            f"Add missing JSON field(s): {', '.join(missing)}." if missing else "none",
        )
        packet["checks"].append(check)
        if missing:
            add_violation(packet, check, f"required_fields: missing {', '.join(missing)}")
    elif expected_format == "markdown":
        check = make_check("format", "pass", "markdown", "markdown text", "none")
        packet["checks"].append(check)
        required_sections = list(contract.get("required_sections", []))
        found = markdown_sections(text)
        missing = [section for section in required_sections if section not in found]
        status = "fail" if missing else "pass"
        check = make_check(
            "markdown_sections",
            status,
            ", ".join(required_sections) or "none",
            ", ".join(sorted(found)) or "none",
            f"Add missing Markdown section(s): {', '.join(missing)}." if missing else "none",
        )
        packet["checks"].append(check)
        if missing:
            add_violation(packet, check, f"markdown_sections: missing {', '.join(missing)}")
    else:
        check = make_check("format", "blocked", expected_format, "unsupported by script", "Provide markdown or json format.")
        packet["checks"].append(check)
        packet["status"] = "blocked"
        packet["violations"].append("format: unsupported by deterministic script")
        packet["repair_suggestions"].append("Use a markdown or json contract for script validation.")

    if contract.get("evidence_tags_required"):
        allowed = list(contract.get("allowed_evidence_tags") or policy["allowed_tags"])
        aliases = list(policy.get("aliases_not_allowed", []))
        present_allowed = [tag for tag in allowed if tag in text]
        present_aliases = [tag for tag in aliases if tag in text]
        status = "pass" if present_allowed and not present_aliases else "fail"
        observed = ", ".join(present_allowed + present_aliases) or "none"
        repair = f"Add at least one allowed evidence tag: {', '.join(allowed)}."
        if present_aliases:
            repair = f"Replace unsupported evidence tag vocabulary: {', '.join(present_aliases)}."
        check = make_check("evidence_tags", status, ", ".join(allowed), observed, repair if status == "fail" else "none")
        packet["checks"].append(check)
        if status == "fail":
            add_violation(packet, check, "evidence_tags: No tags = contract violation")

    naming = contract.get("naming")
    if isinstance(naming, dict) and naming.get("style") == "kebab-case":
        name = Path(artifact).name
        ok = kebab_case_name(name)
        suggestion = suggest_kebab(name)
        check = make_check(
            "naming",
            "pass" if ok else "fail",
            "kebab-case file name",
            name,
            "none" if ok else f"Suggest {suggestion}; do not auto-rename.",
        )
        packet["checks"].append(check)
        if not ok:
            add_violation(packet, check, f"naming: expected kebab-case, observed {name}")

    packet["evidence"].append("[CÓDIGO] validate_output_contract.py executed deterministic checks.")
    shape_errors = validate_packet_shape(packet)
    check = make_check(
        "machine_readable_packet",
        "pass" if not shape_errors else "fail",
        "templates/schema.json",
        "valid packet" if not shape_errors else "; ".join(shape_errors),
        "Fix validation packet shape." if shape_errors else "none",
    )
    packet["checks"].append(check)
    if shape_errors:
        add_violation(packet, check, "machine_readable_packet: packet schema failed")

    # Deduplicate repair suggestions while preserving order.
    seen: set[str] = set()
    repairs = []
    for repair in packet["repair_suggestions"]:
        if repair not in seen:
            seen.add(repair)
            repairs.append(repair)
    packet["repair_suggestions"] = repairs
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an output artifact against a JSON contract")
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--artifact-name", help="Artifact name/path to validate for naming checks")
    parser.add_argument("--expect", choices=["pass", "fail", "blocked"])
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        packet = validate(contract, args.output, args.artifact_name)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(packet, indent=2, ensure_ascii=False))
    if args.expect and packet["status"] != args.expect:
        print(f"ERROR: expected {args.expect}, observed {packet['status']}", file=sys.stderr)
        return 1
    return 0 if packet["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
