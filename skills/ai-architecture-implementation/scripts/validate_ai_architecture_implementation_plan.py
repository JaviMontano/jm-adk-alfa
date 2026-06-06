#!/usr/bin/env python3
"""Validate AI Architecture Implementation plan packets offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SCHEMA = "jm-labs.ai-architecture-implementation.plan.v1"
REQUIRED_TOP = {"schema", "system", "mode", "scope", "evidence", "prerequisites", "phases", "technology_decisions", "controls", "risks", "validation"}
MODES = {"greenfield", "brownfield", "remediation", "migration"}
PHASES = {"F0", "F1", "F2", "F3", "F4", "F5"}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[MÉTRICA]", "[ENTREVISTA]", "[INFERENCIA]"}
CHECKS = {"assets", "deterministic_scripts", "quality_criteria", "phase_dod", "evidence_required", "technology_decisions", "rollback_monitoring"}
CONTROLS = {"ci_cd", "rollback", "monitoring", "runbooks"}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def objects(value: Any, name: str, errors: list[str]) -> list[dict[str, Any]]:
    require(isinstance(value, list), errors, f"{name} must be list")
    if not isinstance(value, list):
        return []
    out = []
    for i, item in enumerate(value):
        require(isinstance(item, dict), errors, f"{name}[{i}] must be object")
        if isinstance(item, dict):
            out.append(item)
    return out


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("mode") in MODES, errors, f"invalid mode {data.get('mode')}")
    require(bool(data.get("system", {}).get("name")), errors, "system.name required")
    require(isinstance(data.get("scope"), dict) and bool(data["scope"].get("coverage")), errors, "scope.coverage required")

    evidence = objects(data.get("evidence"), "evidence", errors)
    evidence_ids = set()
    for item in evidence:
        eid = item.get("id")
        require(isinstance(eid, str) and eid, errors, "evidence id required")
        if isinstance(eid, str):
            require(eid not in evidence_ids, errors, f"duplicate evidence id {eid}")
            evidence_ids.add(eid)
        require(item.get("tag") in TAGS, errors, f"evidence {eid} invalid tag")
        require(bool(item.get("source")), errors, f"evidence {eid} source required")

    phases = objects(data.get("phases"), "phases", errors)
    phase_ids = {item.get("id") for item in phases}
    require(PHASES.issubset(phase_ids), errors, "phases must cover F0-F5")
    for phase in phases:
        pid = phase.get("id")
        require(pid in PHASES, errors, f"invalid phase {pid}")
        require(isinstance(phase.get("deliverables"), list) and phase["deliverables"], errors, f"phase {pid} deliverables required")
        require(isinstance(phase.get("dependencies"), list), errors, f"phase {pid} dependencies must be list")
        require(isinstance(phase.get("dod"), list) and phase["dod"], errors, f"phase {pid} dod required")
        refs = phase.get("evidence_ids")
        require(isinstance(refs, list) and refs, errors, f"phase {pid} evidence_ids required")
        if isinstance(refs, list):
            for ref in refs:
                require(ref in evidence_ids, errors, f"phase {pid} references unknown evidence {ref}")

    decisions = objects(data.get("technology_decisions"), "technology_decisions", errors)
    require(decisions, errors, "technology_decisions required")
    for decision in decisions:
        component = decision.get("component")
        for field in ("component", "selected", "rationale"):
            require(bool(decision.get(field)), errors, f"technology decision missing {field}")
        require(isinstance(decision.get("alternatives"), list) and decision["alternatives"], errors, f"technology decision {component} alternatives required")
        refs = decision.get("evidence_ids")
        require(isinstance(refs, list) and refs, errors, f"technology decision {component} evidence_ids required")
        if isinstance(refs, list):
            for ref in refs:
                require(ref in evidence_ids, errors, f"technology decision {component} references unknown evidence {ref}")

    controls = data.get("controls")
    require(isinstance(controls, dict), errors, "controls must be object")
    if isinstance(controls, dict):
        for control in CONTROLS:
            item = controls.get(control)
            require(isinstance(item, dict), errors, f"control {control} must be object")
            if isinstance(item, dict):
                require(item.get("status") in {"planned", "implemented", "blocked"}, errors, f"control {control} invalid status")
                require(bool(item.get("dod")), errors, f"control {control} dod required")

    require(isinstance(data.get("prerequisites"), list), errors, "prerequisites must be list")
    require(isinstance(data.get("risks"), list), errors, "risks must be list")
    validation = data.get("validation")
    require(isinstance(validation, dict), errors, "validation must be object")
    if isinstance(validation, dict):
        require(validation.get("status") in {"pass", "warn", "block"}, errors, "invalid validation.status")
        checks = validation.get("checks")
        require(isinstance(checks, list), errors, "validation.checks must be list")
        if isinstance(checks, list):
            require(CHECKS.issubset(set(checks)), errors, "validation.checks missing required checks")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_ai_architecture_implementation_plan.py <plan.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data if isinstance(data, dict) else {})
    print(f"plan={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
