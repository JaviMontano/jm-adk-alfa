#!/usr/bin/env python3
"""Validate AI Architecture Audit JSON packets offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


EXPECTED_SCHEMA = "jm-labs.ai-architecture-audit.report.v1"
REQUIRED_TOP = {
    "schema",
    "system",
    "scope",
    "evidence",
    "dimensions",
    "findings",
    "quality_attributes",
    "anti_patterns",
    "security_controls",
    "technical_debt",
    "roadmap",
    "validation",
}
REQUIRED_DIMENSIONS = {"D1", "D2", "D3", "D4", "D5", "D6"}
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
EVIDENCE_TAGS = {"[CÓDIGO]", "[CONFIG]", "[MÉTRICA]", "[DOC]", "[ENTREVISTA]", "[HERRAMIENTA]", "[INFERENCIA]"}
CONCRETE_TAGS = {"[CÓDIGO]", "[CONFIG]", "[MÉTRICA]", "[DOC]", "[ENTREVISTA]", "[HERRAMIENTA]"}
EFFORTS = {"S", "M", "L", "XL"}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "evidence_required",
    "severity_taxonomy",
    "six_dimensions",
    "remediation_contract",
}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def list_of_objects(value: Any, name: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out = []
    for index, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{name}[{index}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors

    require(data.get("schema") == EXPECTED_SCHEMA, errors, "schema mismatch")

    system = data.get("system")
    require(isinstance(system, dict), errors, "system must be object")
    if isinstance(system, dict):
        for field in ("name", "type", "stage"):
            require(bool(system.get(field)), errors, f"system missing {field}")

    scope = data.get("scope")
    require(isinstance(scope, dict), errors, "scope must be object")
    if isinstance(scope, dict):
        require(scope.get("mode") in {"piloto-auto", "desatendido", "supervisado", "paso-a-paso"}, errors, "invalid scope.mode")
        require(scope.get("depth") in {"express", "standard", "deep"}, errors, "invalid scope.depth")
        require(scope.get("format") in {"ejecutivo", "técnico", "híbrido"}, errors, "invalid scope.format")

    evidence_items = list_of_objects(data.get("evidence"), "evidence", errors)
    evidence_ids: set[str] = set()
    for index, item in enumerate(evidence_items):
        evidence_id = item.get("id")
        require(isinstance(evidence_id, str) and evidence_id, errors, f"evidence[{index}] missing id")
        if isinstance(evidence_id, str):
            require(evidence_id not in evidence_ids, errors, f"duplicate evidence id: {evidence_id}")
            evidence_ids.add(evidence_id)
        tag = item.get("tag")
        require(tag in EVIDENCE_TAGS, errors, f"evidence {evidence_id} invalid tag {tag}")
        for field in ("type", "source", "summary"):
            require(bool(item.get(field)), errors, f"evidence {evidence_id} missing {field}")

    dimensions = list_of_objects(data.get("dimensions"), "dimensions", errors)
    covered = {item.get("id") for item in dimensions}
    require(REQUIRED_DIMENSIONS.issubset(covered), errors, "dimensions must cover D1-D6")
    for item in dimensions:
        require(item.get("id") in REQUIRED_DIMENSIONS, errors, f"invalid dimension {item.get('id')}")
        score = item.get("score")
        require(isinstance(score, int) and 0 <= score <= 5, errors, f"dimension {item.get('id')} score must be 0..5")
        if item.get("status") == "omitted":
            require(bool(item.get("rationale")), errors, f"omitted dimension {item.get('id')} needs rationale")

    findings = list_of_objects(data.get("findings"), "findings", errors)
    require(findings, errors, "findings must be non-empty")
    finding_ids: set[str] = set()
    for index, finding in enumerate(findings):
        fid = finding.get("id")
        require(isinstance(fid, str) and fid, errors, f"finding[{index}] missing id")
        if isinstance(fid, str):
            require(fid not in finding_ids, errors, f"duplicate finding id: {fid}")
            finding_ids.add(fid)
        require(finding.get("severity") in SEVERITIES, errors, f"finding {fid} invalid severity {finding.get('severity')}")
        require(finding.get("dimension") in REQUIRED_DIMENSIONS, errors, f"finding {fid} invalid dimension {finding.get('dimension')}")
        refs = finding.get("evidence_ids")
        require(isinstance(refs, list) and refs, errors, f"finding {fid} missing evidence_ids")
        concrete = False
        if isinstance(refs, list):
            for ref in refs:
                require(ref in evidence_ids, errors, f"finding {fid} references unknown evidence {ref}")
                source = next((item for item in evidence_items if item.get("id") == ref), {})
                concrete = concrete or source.get("tag") in CONCRETE_TAGS
        require(concrete, errors, f"finding {fid} needs at least one concrete evidence tag")
        remediation = finding.get("remediation")
        require(isinstance(remediation, dict), errors, f"finding {fid} remediation must be object")
        if isinstance(remediation, dict):
            require(bool(remediation.get("pattern")), errors, f"finding {fid} remediation missing pattern")
            require(remediation.get("effort") in EFFORTS, errors, f"finding {fid} invalid remediation effort")
            require(isinstance(remediation.get("dependencies"), list), errors, f"finding {fid} remediation dependencies must be list")
            require(bool(remediation.get("dod")), errors, f"finding {fid} remediation missing dod")

    quality_attrs = list_of_objects(data.get("quality_attributes"), "quality_attributes", errors)
    require(quality_attrs, errors, "quality_attributes must be non-empty")
    for attr in quality_attrs:
        require(bool(attr.get("name")), errors, "quality attribute missing name")
        require("threshold" in attr and attr.get("threshold") not in ("", None), errors, f"quality attribute {attr.get('name')} missing threshold")
        require("current" in attr, errors, f"quality attribute {attr.get('name')} missing current")
        require(attr.get("evidence_id") in evidence_ids, errors, f"quality attribute {attr.get('name')} references unknown evidence")

    anti_patterns = list_of_objects(data.get("anti_patterns"), "anti_patterns", errors)
    require(anti_patterns, errors, "anti_patterns must be non-empty")
    for item in anti_patterns:
        require(bool(item.get("name")), errors, "anti_pattern missing name")
        require(bool(item.get("detection_method")), errors, f"anti_pattern {item.get('name')} missing detection_method")
        require(item.get("evidence_id") in evidence_ids, errors, f"anti_pattern {item.get('name')} references unknown evidence")

    security_controls = list_of_objects(data.get("security_controls"), "security_controls", errors)
    require(security_controls, errors, "security_controls must be non-empty")
    for item in security_controls:
        require(bool(item.get("control")), errors, "security control missing control")
        require(item.get("status") in {"implemented", "partial", "missing", "unknown"}, errors, f"security control {item.get('control')} invalid status")
        require(item.get("evidence_id") in evidence_ids, errors, f"security control {item.get('control')} references unknown evidence")

    debts = list_of_objects(data.get("technical_debt"), "technical_debt", errors)
    require(debts, errors, "technical_debt must be non-empty")
    for item in debts:
        require(bool(item.get("type")), errors, "technical debt missing type")
        for field in ("impact", "interest", "principal"):
            require(bool(item.get(field)), errors, f"technical debt {item.get('type')} missing {field}")
        require(item.get("evidence_id") in evidence_ids, errors, f"technical debt {item.get('type')} references unknown evidence")

    roadmap = list_of_objects(data.get("roadmap"), "roadmap", errors)
    require(roadmap, errors, "roadmap must be non-empty")
    for item in roadmap:
        require(item.get("finding_id") in finding_ids, errors, f"roadmap references unknown finding {item.get('finding_id')}")
        require(isinstance(item.get("priority_score"), int) and 1 <= item.get("priority_score") <= 27, errors, "roadmap priority_score must be 1..27")
        require(bool(item.get("phase")), errors, "roadmap item missing phase")

    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if isinstance(validation, dict):
        require(validation.get("status") in {"pass", "warn", "block"}, errors, "invalid validation.status")
        checks = validation.get("checks")
        require(isinstance(checks, list), errors, "validation.checks must be list")
        if isinstance(checks, list):
            require(REQUIRED_CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")
        omissions = validation.get("omissions", [])
        require(isinstance(omissions, list), errors, "validation.omissions must be list")
        if isinstance(omissions, list) and omissions:
            require(validation.get("status") != "pass", errors, "omissions cannot produce pass status")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_ai_architecture_audit_report.py <report.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"report={path.name} status=fail errors=1")
        print(f"ERROR invalid json: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print(f"report={path.name} status=fail errors=1")
        print("ERROR report must be object", file=sys.stderr)
        return 1
    errors = validate(data)
    print(f"report={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
