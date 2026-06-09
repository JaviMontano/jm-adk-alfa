#!/usr/bin/env python3
"""Validate deterministic Workspace Setup JSON plans."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.workspace-setup.plan.v1"
REQUIRED_TOP = {
    "schema",
    "skill",
    "mode",
    "target_file",
    "existing_profile",
    "profile",
    "commands",
    "privacy",
    "write_policy",
    "evidence",
    "validation",
}
PROFILE_FIELDS = {"goal", "runtime", "autonomy", "workspace_area", "output_format"}
COMMAND_SECTIONS = {"allowed", "prohibited", "escalation_required"}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "runtime_preferences",
    "command_policy",
    "privacy_policy",
    "write_policy",
    "evidence_required",
}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]"}
FORBIDDEN_ALLOWED = [
    re.compile(r"git\s+reset\s+--hard"),
    re.compile(r"rm\s+-rf"),
    re.compile(r"curl\s*\|\s*sh"),
    re.compile(r"export\s+.*KEY="),
    re.compile(r"gh\s+secret\s+set"),
]


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def text_list(value: Any, ctx: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for i, item in enumerate(value):
        require(is_text(item), errors, f"{ctx}[{i}] must be non-empty string")
        if is_text(item):
            out.append(item)
    return out


def object_at(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    require(isinstance(value, dict), errors, f"{key} must be object")
    return value if isinstance(value, dict) else {}


def validate_existing_profile(data: dict[str, Any], errors: list[str]) -> None:
    item = object_at(data, "existing_profile", errors)
    for key in ("detected", "overwrite", "force"):
        require(isinstance(item.get(key), bool), errors, f"existing_profile.{key} must be boolean")
    if item.get("detected") is True and item.get("overwrite") is True:
        require(item.get("force") is True, errors, "overwrite of existing profile requires force=true")


def validate_profile(data: dict[str, Any], errors: list[str]) -> None:
    profile = object_at(data, "profile", errors)
    missing = sorted(PROFILE_FIELDS - set(profile))
    require(not missing, errors, f"profile missing fields: {', '.join(missing)}")
    for field in sorted(PROFILE_FIELDS):
        require(is_text(profile.get(field)), errors, f"profile.{field} required")
    area = profile.get("workspace_area")
    if is_text(area):
        require(area.startswith("workspace/") or area.startswith(".local/"), errors, "profile.workspace_area must be local workspace path")
    fmt = profile.get("output_format")
    if is_text(fmt):
        require(fmt in {"markdown", "json", "markdown+json"}, errors, "profile.output_format invalid")


def validate_commands(data: dict[str, Any], errors: list[str]) -> None:
    commands = object_at(data, "commands", errors)
    missing = sorted(COMMAND_SECTIONS - set(commands))
    require(not missing, errors, f"commands missing sections: {', '.join(missing)}")
    allowed = text_list(commands.get("allowed"), "commands.allowed", errors)
    prohibited = text_list(commands.get("prohibited"), "commands.prohibited", errors)
    escalation = text_list(commands.get("escalation_required"), "commands.escalation_required", errors)
    require(bool(allowed), errors, "commands.allowed must not be empty")
    for command in allowed:
        for pattern in FORBIDDEN_ALLOWED:
            require(not pattern.search(command), errors, f"dangerous command cannot be allowed: {command}")
    require("git reset --hard" in prohibited, errors, "commands.prohibited must include git reset --hard")
    require("rm -rf" in prohibited, errors, "commands.prohibited must include rm -rf")
    require("network" in escalation, errors, "commands.escalation_required must include network")
    require("destructive" in escalation, errors, "commands.escalation_required must include destructive")


def validate_privacy(data: dict[str, Any], errors: list[str]) -> None:
    privacy = object_at(data, "privacy", errors)
    require(privacy.get("local_only") is True, errors, "privacy.local_only must be true")
    require(privacy.get("stores_secrets") is False, errors, "privacy.stores_secrets must be false")
    require(privacy.get("secret_scan_performed") is True, errors, "privacy.secret_scan_performed must be true")
    redactions = set(text_list(privacy.get("redactions"), "privacy.redactions", errors))
    require({"tokens", "passwords"}.issubset(redactions), errors, "privacy.redactions must include tokens and passwords")


def validate_write_policy(data: dict[str, Any], errors: list[str]) -> None:
    policy = object_at(data, "write_policy", errors)
    require(policy.get("dry_run_default") is True, errors, "write_policy.dry_run_default must be true")
    require(policy.get("apply_requires_explicit_flag") is True, errors, "write_policy.apply_requires_explicit_flag must be true")
    require(policy.get("overwrite_requires_force") is True, errors, "write_policy.overwrite_requires_force must be true")
    require(policy.get("gitignored") is True, errors, "write_policy.gitignored must be true")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> None:
    evidence = data.get("evidence")
    require(isinstance(evidence, list) and bool(evidence), errors, "evidence must be non-empty list")
    if not isinstance(evidence, list):
        return
    for i, item in enumerate(evidence):
        ctx = f"evidence[{i}]"
        require(isinstance(item, dict), errors, f"{ctx} must be object")
        if not isinstance(item, dict):
            continue
        require(is_text(item.get("claim")), errors, f"{ctx}.claim required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        require(is_text(item.get("source")), errors, f"{ctx}.source required")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = object_at(data, "validation", errors)
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    require(validation.get("offline") is True, errors, "validation.offline must be true")
    require(validation.get("network_required") is False, errors, "validation.network_required must be false")
    require(validation.get("deterministic") is True, errors, "validation.deterministic must be true")
    checks = set(text_list(validation.get("checks"), "validation.checks", errors))
    require(REQUIRED_CHECKS.issubset(checks), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "workspace-setup", errors, "skill must be workspace-setup")
    require(data.get("mode") in {"dry-run", "apply"}, errors, "mode must be dry-run or apply")
    require(data.get("target_file") == ".jm-adk.local.json", errors, "target_file must be .jm-adk.local.json")
    validate_existing_profile(data, errors)
    validate_profile(data, errors)
    validate_commands(data, errors)
    validate_privacy(data, errors)
    validate_write_policy(data, errors)
    validate_evidence(data, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_workspace_setup_plan.py <plan.json>", file=sys.stderr)
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
