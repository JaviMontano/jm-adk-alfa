#!/usr/bin/env python3
"""Validate deterministic local-state preservation reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_ROOT = {
    "schema",
    "skill",
    "mode",
    "scope",
    "mutation_policy",
    "surfaces",
    "artifacts",
    "non_touch_decisions",
    "validation",
    "next_action",
}
MODES = {"inventory-only", "patch-bundle", "archive-bundle", "handoff"}
NEXT_ACTIONS = {"proceed", "pause", "blocked"}
SURFACES = {
    "tracked_changes",
    "untracked_files",
    "ignored_files",
    "stashes",
    "worktrees",
    "clones",
    "private_path_exclusions",
}
ARTIFACT_KINDS = {"patch", "archive", "manifest", "report", "checksum"}
HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
PRIVATE_MARKERS = ("user-context/jarvis-os", ".env", ".secret", "credentials")


def require_object(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{name} must be an object")
        return {}
    return value


def require_array(value: Any, name: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{name} must be an array")
        return []
    return value


def validate_scope(scope: dict[str, Any], errors: list[str]) -> None:
    for key in ("repository", "branch", "head"):
        if not str(scope.get(key, "")).strip():
            errors.append(f"scope.{key} is required")


def validate_mutation_policy(policy: dict[str, Any], errors: list[str]) -> None:
    if policy.get("default_mutates_files") is not False:
        errors.append("mutation_policy.default_mutates_files must be false")
    if policy.get("requires_explicit_apply") is not True:
        errors.append("mutation_policy.requires_explicit_apply must be true")


def validate_surfaces(surfaces: dict[str, Any], errors: list[str]) -> None:
    missing = sorted(SURFACES - set(surfaces))
    if missing:
        errors.append(f"surfaces missing required keys: {', '.join(missing)}")
    for key in SURFACES:
        entries = require_array(surfaces.get(key, []), f"surfaces.{key}", errors)
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"surfaces.{key}[{index}] must be an object")
                continue
            if key == "private_path_exclusions":
                for field in ("path", "handling", "reason"):
                    if not str(entry.get(field, "")).strip():
                        errors.append(f"surfaces.{key}[{index}].{field} is required")
                if entry.get("handling") not in {"redacted", "excluded", "blocked"}:
                    errors.append(f"surfaces.{key}[{index}].handling is invalid")
            else:
                for field in ("path", "status", "evidence"):
                    if not str(entry.get(field, "")).strip():
                        errors.append(f"surfaces.{key}[{index}].{field} is required")
                if key == "stashes":
                    if entry.get("touched") is not False:
                        errors.append(f"surfaces.{key}[{index}].touched must be false")
                    if entry.get("decision") not in {None, "inventory-only"}:
                        errors.append(f"surfaces.{key}[{index}].decision must be inventory-only when present")


def validate_artifacts(mode: str, artifacts: list[Any], errors: list[str]) -> None:
    if mode in {"patch-bundle", "archive-bundle", "handoff"} and not artifacts:
        errors.append(f"mode {mode} requires at least one artifact")
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"artifacts[{index}] must be an object")
            continue
        if artifact.get("kind") not in ARTIFACT_KINDS:
            errors.append(f"artifacts[{index}].kind is invalid")
        for field in ("path", "destination_path", "sha256"):
            if not str(artifact.get(field, "")).strip():
                errors.append(f"artifacts[{index}].{field} is required")
        if not HEX64.match(str(artifact.get("sha256", ""))):
            errors.append(f"artifacts[{index}].sha256 must be 64 hex characters")
        if not isinstance(artifact.get("source_paths"), list) or not artifact.get("source_paths"):
            errors.append(f"artifacts[{index}].source_paths must be a non-empty array")
        if not isinstance(artifact.get("size_bytes"), int) or artifact.get("size_bytes", 0) <= 0:
            errors.append(f"artifacts[{index}].size_bytes must be a positive integer")
        if artifact.get("overwrites_existing") is not False:
            errors.append(f"artifacts[{index}].overwrites_existing must be false")
        searchable = " ".join(
            str(part)
            for part in [
                artifact.get("path", ""),
                artifact.get("destination_path", ""),
                " ".join(str(p) for p in artifact.get("source_paths", []) if isinstance(p, str)),
            ]
        )
        if any(marker in searchable for marker in PRIVATE_MARKERS):
            errors.append(f"artifacts[{index}] includes a private path marker")


def validate_non_touch(decisions: list[Any], errors: list[str]) -> None:
    if not decisions:
        errors.append("non_touch_decisions must contain at least one decision")
    required_surfaces = {"stashes", "private_paths"}
    seen_surfaces: set[str] = set()
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            errors.append(f"non_touch_decisions[{index}] must be an object")
            continue
        for field in ("surface", "decision", "reason", "evidence"):
            if not str(decision.get(field, "")).strip():
                errors.append(f"non_touch_decisions[{index}].{field} is required")
        surface = str(decision.get("surface", ""))
        seen_surfaces.add(surface)
        if surface == "stashes" and decision.get("decision") != "inventory-only":
            errors.append("non_touch_decisions for stashes must be inventory-only")
        if surface == "private_paths" and decision.get("decision") != "do-not-move-or-publish":
            errors.append("non_touch_decisions for private_paths must be do-not-move-or-publish")
    missing = sorted(required_surfaces - seen_surfaces)
    if missing:
        errors.append(f"non_touch_decisions missing surfaces: {', '.join(missing)}")


def validate_validation(validation: dict[str, Any], next_action: str, errors: list[str]) -> None:
    status = validation.get("status")
    if status not in {"pass", "warn", "fail", "blocked"}:
        errors.append("validation.status is invalid")
    commands = require_array(validation.get("commands"), "validation.commands", errors)
    if not commands:
        errors.append("validation.commands must contain at least one command")
    failed = status in {"fail", "blocked"}
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            errors.append(f"validation.commands[{index}] must be an object")
            continue
        for field in ("command", "status", "evidence"):
            if not str(command.get(field, "")).strip():
                errors.append(f"validation.commands[{index}].{field} is required")
        if command.get("status") not in {"pass", "warn", "fail", "blocked", "not-run"}:
            errors.append(f"validation.commands[{index}].status is invalid")
        failed = failed or command.get("status") in {"fail", "blocked"}
    if failed and next_action == "proceed":
        errors.append("next_action cannot be proceed when validation failed")


def validate_report(report: Any) -> list[str]:
    errors: list[str] = []
    root = require_object(report, "root", errors)
    if not root:
        return errors
    missing = sorted(REQUIRED_ROOT - set(root))
    if missing:
        errors.append(f"root missing required keys: {', '.join(missing)}")
    if root.get("schema") != 1:
        errors.append("schema must be 1")
    if root.get("skill") != "local-state-preservation":
        errors.append("skill must be local-state-preservation")
    mode = str(root.get("mode", ""))
    if mode not in MODES:
        errors.append("mode is invalid")
    next_action = str(root.get("next_action", ""))
    if next_action not in NEXT_ACTIONS:
        errors.append("next_action is invalid")

    validate_scope(require_object(root.get("scope"), "scope", errors), errors)
    validate_mutation_policy(require_object(root.get("mutation_policy"), "mutation_policy", errors), errors)
    validate_surfaces(require_object(root.get("surfaces"), "surfaces", errors), errors)
    validate_artifacts(mode, require_array(root.get("artifacts"), "artifacts", errors), errors)
    validate_non_touch(require_array(root.get("non_touch_decisions"), "non_touch_decisions", errors), errors)
    validate_validation(require_object(root.get("validation"), "validation", errors), next_action, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local-state-preservation report")
    parser.add_argument("reports", nargs="+", help="Report JSON files to validate")
    args = parser.parse_args()

    all_errors: list[str] = []
    for report_path in args.reports:
        path = Path(report_path)
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            all_errors.append(f"{path}: invalid JSON: {exc}")
            continue
        for error in validate_report(report):
            all_errors.append(f"{path}: {error}")

    for error in all_errors:
        print(f"ERROR: {error}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
