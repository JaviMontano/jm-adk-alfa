#!/usr/bin/env python3
"""Diagnose the in-kit JM-ADK user-context repo without modifying files."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


MARKER = ".jm-adk-context.json"
EXPECTED_KIND = "jm-adk-user-context"
DEFAULT_ROOT = "user-context"
DEFAULT_MAX_FILES = 12
SECRET_PATTERNS = [
    re.compile(r"\b(password|passwd|secret|token|api[_-]?key|private[_-]?key)\b", re.IGNORECASE),
    re.compile(r"\b(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[0-9A-Za-z]{36}|sk-[0-9A-Za-z]{48})\b"),
    re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
]
REQUIRED_SCAFFOLD = [
    MARKER,
    ".gitignore",
    "README.md",
    "AGENTS.md",
    "_INDICE.md",
    "context/README.md",
    "preferences/README.md",
    "memory/README.md",
    "sources/README.md",
    "resources/README.md",
    "personal-skills/README.md",
    "personal-skills/_INDICE.md",
    "personal-skills/.jm-adk-personal-skills.json",
    "personal-skills/skills/.gitkeep",
    "schemas/README.md",
    "schemas/user-context-manifest.schema.json",
    "schemas/context-card.schema.json",
    "schemas/resource-card.schema.json",
    "schemas/personal-skills-manifest.schema.json",
]
TRACKED_ALLOWLIST = set(REQUIRED_SCAFFOLD) | {
    "manifest.example.json",
    "context/.gitkeep",
    "preferences/.gitkeep",
    "memory/.gitkeep",
    "sources/.gitkeep",
    "resources/.gitkeep",
}


def repo_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return start.resolve()


def read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "JSON root must be an object"
    return data, None


def load_local_user_context(root: Path) -> tuple[dict[str, Any], str | None]:
    path = root / ".jm-adk.local.json"
    if not path.exists():
        return {}, None
    data, error = read_json(path)
    if error:
        return {}, f".jm-adk.local.json invalid: {error}"
    value = data.get("userContext", {}) if data else {}
    if value is None:
        return {}, None
    if not isinstance(value, dict):
        return {}, ".jm-adk.local.json userContext must be an object"
    return value, None


def bool_arg(value: str | None, default: bool) -> bool:
    if value is None or value == "auto":
        return default
    return value.lower() in {"1", "true", "yes", "on", "enabled"}


def resolve_context_root(root: Path, raw: str) -> Path:
    path = Path(os.path.expanduser(raw))
    if path.is_absolute():
        return path.resolve()
    return (root / path).resolve()


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def tracked_files(root: Path, context_rel: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--", context_rel],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return []
    prefix = context_rel.rstrip("/") + "/"
    files: list[str] = []
    for line in result.stdout.splitlines():
        if line.startswith(prefix):
            files.append(line[len(prefix) :])
    return files


def secret_like(path: Path) -> list[str]:
    findings: list[str] = []
    if not path.exists() or path.is_dir():
        return findings
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(str(path))
            break
    return findings


def configured_values(root: Path, args: argparse.Namespace) -> tuple[dict[str, Any], list[str]]:
    problems: list[str] = []
    local, local_error = load_local_user_context(root)
    if local_error:
        problems.append(local_error)
    enabled_default = bool(local.get("enabled", True))
    enabled = bool_arg(args.enabled, enabled_default)
    context_root = args.context_root or str(local.get("root", DEFAULT_ROOT))
    return {
        "enabled": enabled,
        "root": context_root,
        "autoload": bool(local.get("autoload", False)),
        "privacyMode": str(local.get("privacyMode", "local-private")),
        "maxFiles": int(local.get("maxFiles", DEFAULT_MAX_FILES)),
    }, problems


def diagnose(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    config, problems = configured_values(root, args)
    context_path = resolve_context_root(root, str(config["root"]))
    workspace_path = (root / "workspace").resolve()
    checks: dict[str, Any] = {
        "required_scaffold": "unknown",
        "known_buckets": "unknown",
        "marker": "unknown",
        "manifest": "not_present",
        "personal_skills_marker": "unknown",
        "inside_repo": is_inside(context_path, root.resolve()),
        "outside_workspace": not is_inside(context_path, workspace_path),
        "private_tracked_files": [],
        "secret_like_files": [],
    }

    if not config["enabled"]:
        return {
            "schema": 1,
            "status": "disabled",
            "enabled": False,
            "repo_root": str(root),
            "context_root": str(context_path),
            "config": config,
            "checks": checks,
            "problems": problems,
            "next_action": "Enable userContext in .jm-adk.local.json or pass --enabled true.",
        }

    if not context_path.exists():
        return {
            "schema": 1,
            "status": "missing",
            "enabled": True,
            "repo_root": str(root),
            "context_root": str(context_path),
            "config": config,
            "checks": checks,
            "problems": problems,
            "next_action": "Run python3 scripts/scaffold-user-context.py --apply.",
        }

    if not checks["inside_repo"]:
        problems.append("context root must live inside the Alfa repo")
    if not checks["outside_workspace"]:
        problems.append("context root must not live inside workspace/")

    missing = [rel for rel in REQUIRED_SCAFFOLD if not (context_path / rel).exists()]
    checks["required_scaffold"] = "pass" if not missing else {"missing": missing}
    if missing:
        problems.append("user-context scaffold is incomplete")

    bucket_missing = [rel for rel in ["context", "preferences", "memory", "sources", "resources", "personal-skills", "schemas"] if not (context_path / rel).is_dir()]
    checks["known_buckets"] = "pass" if not bucket_missing else {"missing": bucket_missing}
    if bucket_missing:
        problems.append("known user-context buckets are missing")

    marker_path = context_path / MARKER
    marker, marker_error = read_json(marker_path)
    if marker_error:
        checks["marker"] = f"invalid: {marker_error}"
        problems.append(f"{MARKER} invalid: {marker_error}")
    elif marker.get("kind") != EXPECTED_KIND:
        checks["marker"] = f"invalid kind: {marker.get('kind')}"
        problems.append(f"{MARKER} kind must be {EXPECTED_KIND}")
    else:
        checks["marker"] = "pass"

    personal_marker_path = context_path / "personal-skills/.jm-adk-personal-skills.json"
    personal_marker, personal_error = read_json(personal_marker_path)
    if personal_error:
        checks["personal_skills_marker"] = f"invalid: {personal_error}"
        problems.append(f"personal skills marker invalid: {personal_error}")
    elif personal_marker.get("kind") != "jm-adk-personal-skills":
        checks["personal_skills_marker"] = f"invalid kind: {personal_marker.get('kind')}"
        problems.append("personal skills marker kind must be jm-adk-personal-skills")
    else:
        checks["personal_skills_marker"] = "pass"

    manifest_path = context_path / "manifest.json"
    if manifest_path.exists():
        manifest, manifest_error = read_json(manifest_path)
        if manifest_error:
            checks["manifest"] = f"invalid: {manifest_error}"
            problems.append(f"manifest.json invalid: {manifest_error}")
        elif manifest.get("kind") != "jm-adk-user-context-manifest":
            checks["manifest"] = f"invalid kind: {manifest.get('kind')}"
            problems.append("manifest.json kind must be jm-adk-user-context-manifest")
        else:
            checks["manifest"] = "pass"

    if is_inside(context_path, root.resolve()):
        rel_root = str(context_path.relative_to(root.resolve()))
        private_tracked = [rel for rel in tracked_files(root, rel_root) if rel not in TRACKED_ALLOWLIST]
        checks["private_tracked_files"] = private_tracked
        if private_tracked:
            problems.append("private user-context files are tracked by git")

    scan_candidates = [manifest_path, context_path / "_INDICE.md"]
    if marker and isinstance(marker.get("autoload"), dict):
        for rel in marker["autoload"].get("entrypoints", []):
            scan_candidates.append(context_path / str(rel))
    unique_candidates = []
    seen: set[Path] = set()
    for candidate in scan_candidates[: int(config["maxFiles"] )]:
        resolved = candidate.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique_candidates.append(resolved)
    secret_findings: list[str] = []
    for candidate in unique_candidates:
        secret_findings.extend(secret_like(candidate))
    checks["secret_like_files"] = secret_findings
    if secret_findings:
        problems.append("secret-like content found in user-context autoload files")

    status = "ready" if not problems else "degraded"
    return {
        "schema": 1,
        "status": status,
        "enabled": True,
        "repo_root": str(root),
        "context_root": str(context_path),
        "config": config,
        "checks": checks,
        "problems": problems,
        "next_action": "Proceed with explicit, minimal context loading." if status == "ready" else "Fix reported user-context issues.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose the JM-ADK in-kit user-context repo")
    parser.add_argument("--root", default=".", help="Alfa repo root")
    parser.add_argument("--context-root", help="Context root path, relative to Alfa by default")
    parser.add_argument("--enabled", choices=["auto", "true", "false"], default="auto")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--dry-run", action="store_true", help="Compatibility flag; diagnosis is read-only")
    args = parser.parse_args()

    root = repo_root(Path(args.root))
    result = diagnose(root, args)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"USER_CONTEXT_STATUS: {result['status']}")
        print(f"ENABLED: {str(result['enabled']).lower()}")
        print(f"CONTEXT_ROOT: {result['context_root']}")
        for problem in result.get("problems", []):
            print(f"PROBLEM: {problem}")
        print(f"NEXT: {result['next_action']}")
    return 1 if result["status"] == "degraded" else 0


if __name__ == "__main__":
    raise SystemExit(main())
