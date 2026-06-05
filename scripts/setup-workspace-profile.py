#!/usr/bin/env python3
"""Create a local JM-ADK profile only when explicitly applied."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


GENERATOR = "scripts/setup-workspace-profile.py"
SECRET_PATTERNS = [
    re.compile(r"\b(password|passwd|secret|token|api[_-]?key|private[_-]?key)\b", re.IGNORECASE),
    re.compile(r"\b[A-Za-z0-9_=-]{32,}\b"),
]

# Canonical runtime identifiers the kit is homologated for (see runtime mirrors
# and docs/runtime-tool-access-matrix.md). Used to validate profile runtimes.
KNOWN_RUNTIMES = {
    "claude-code",
    "claude-desktop",
    "claude-cowork",
    "codex",
    "gemini-cli",
    "antigravity",
    "cursor",
    "windsurf",
    "vscode-copilot",
}


def normalize_runtime(value: str) -> str:
    """Lowercase + hyphenate so 'Claude Code' / 'Codex' map to canonical ids."""
    return re.sub(r"\s+", "-", value.strip().lower())


def parse_runtime_targets(raw: str | None, preferred: str) -> list[str]:
    """Resolve --runtime-targets (comma-separated) to a deduped canonical list.

    Falls back to [preferred] when not provided. Order-preserving.
    """
    if raw:
        items = [normalize_runtime(x) for x in raw.split(",") if x.strip()]
    else:
        items = [normalize_runtime(preferred)]
    seen: list[str] = []
    for it in items:
        if it not in seen:
            seen.append(it)
    return seen


def repo_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return start.resolve()


def reject_secret_like(values: dict[str, str]) -> list[str]:
    findings: list[str] = []
    for key, value in values.items():
        for pattern in SECRET_PATTERNS:
            if value and pattern.search(value):
                findings.append(key)
                break
    return findings


def profile_payload(args: argparse.Namespace) -> dict[str, object]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    preferred = normalize_runtime(args.runtime)
    targets = parse_runtime_targets(args.runtime_targets, args.runtime)
    return {
        "schema": 2,
        "generatedBy": GENERATOR,
        "generatedAt": now,
        "profile": {
            "primaryGoal": args.goal,
            "projectType": args.project_type,
            "stack": args.stack,
            "preferredRuntime": preferred,
            "runtimeTargets": targets,
            "autonomy": args.autonomy,
            "commandPolicy": args.command_policy,
            "privacy": args.privacy,
            "workspaceArea": args.workspace_area,
            "outputFormat": args.output_format,
        },
        "paths": {
            "specs": "workspace/{active}/specs",
            "tasks": "workspace/{active}/tasks",
            "artifacts": "workspace/{active}/artifacts",
        },
        "userContext": {
            "enabled": True,
            "root": "user-context",
            "autoload": False,
            "privacyMode": "local-private",
            "maxFiles": 12,
        },
        "qualityChecklist": [
            "confirm repo before edits",
            "read before write",
            "dry-run before bulk writes",
            "no secrets in config",
            "load user-context only by explicit relevant files",
            "run validators before handoff",
        ],
        "acceptanceCriteria": [
            "first task has objective, constraints, and definition of done",
            "local profile remains untracked",
            "workspace state remains under workspace/",
            "durable user context remains under user-context/",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up a local JM-ADK workspace profile")
    parser.add_argument("--root", default=".", help="Repo or directory root")
    parser.add_argument("--goal", default="Use Alfa as a safe local-first agentic development kit.")
    parser.add_argument("--project-type", default="agentic-development")
    parser.add_argument("--stack", default="not specified")
    parser.add_argument("--runtime", default="claude-code", help="Preferred runtime id (see KNOWN_RUNTIMES)")
    parser.add_argument("--runtime-targets", default=None,
                        help="Comma-separated runtime ids the kit will be used from (e.g. claude-code,codex,antigravity)")
    parser.add_argument("--autonomy", default="propose diffs before edits")
    parser.add_argument("--command-policy", default="dry-run first; no destructive commands")
    parser.add_argument("--privacy", default="do not request, store, or print secrets")
    parser.add_argument("--workspace-area", default="workspace/")
    parser.add_argument("--output-format", default="brief, operational, evidence-tagged")
    parser.add_argument("--apply", action="store_true", help="Actually write .jm-adk.local.json")
    parser.add_argument("--dry-run", action="store_true", help="Show planned output without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing local profile")
    args = parser.parse_args()

    values = {
        "goal": args.goal,
        "project_type": args.project_type,
        "stack": args.stack,
        "runtime": args.runtime,
        "autonomy": args.autonomy,
        "command_policy": args.command_policy,
        "privacy": args.privacy,
        "workspace_area": args.workspace_area,
        "output_format": args.output_format,
    }
    secret_fields = reject_secret_like(values)
    if secret_fields:
        print(f"ERROR: secret-like content detected in fields: {', '.join(secret_fields)}")
        print("Use placeholders or policy descriptions, not credentials.")
        return 2

    targets = parse_runtime_targets(args.runtime_targets, args.runtime)
    unknown = [r for r in [normalize_runtime(args.runtime), *targets] if r not in KNOWN_RUNTIMES]
    if unknown:
        print(f"ERROR: unknown runtime(s): {', '.join(sorted(set(unknown)))}")
        print(f"Known runtimes: {', '.join(sorted(KNOWN_RUNTIMES))}")
        return 2

    root = repo_root(Path(args.root))
    target = root / ".jm-adk.local.json"
    payload = profile_payload(args)
    if not args.apply:
        print(f"DRY-RUN: would write {target}")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if target.exists() and not args.force:
        print(f"ERROR: {target} exists; use --force after reviewing the diff.")
        return 1
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"WROTE: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
