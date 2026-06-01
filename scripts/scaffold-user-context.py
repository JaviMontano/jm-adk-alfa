#!/usr/bin/env python3
"""Create or repair the in-kit JM-ADK user-context scaffold."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path


DEFAULT_ROOT = "user-context"
GENERATOR = "scripts/scaffold-user-context.py"


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


def schema(title: str, description: str, required: list[str], properties: dict[str, object]) -> str:
    return json.dumps(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": title,
            "description": description,
            "type": "object",
            "required": required,
            "properties": properties,
            "additionalProperties": True,
        },
        indent=2,
    ) + "\n"


def scaffold_files(context_root_name: str = DEFAULT_ROOT) -> dict[str, str]:
    today = date.today().isoformat()
    return {
        ".jm-adk-context.json": json.dumps(
            {
                "schema": 1,
                "kind": "jm-adk-user-context",
                "version": "1.0.0",
                "root": context_root_name,
                "privacy": "local-private",
                "trackedPolicy": "scaffold-only",
                "autoload": {
                    "enabled": False,
                    "entrypoints": [
                        "_INDICE.md",
                        "context/README.md",
                        "preferences/README.md",
                        "memory/README.md",
                        "resources/README.md",
                        "personal-skills/_INDICE.md",
                    ],
                    "maxFiles": 12,
                },
                "writePolicy": "explicit-context-update-only",
            },
            indent=2,
        ) + "\n",
        ".gitignore": """# User-owned context content is private by default.
*

# Tracked context-repo contract and scaffold.
!.gitignore
!.jm-adk-context.json
!README.md
!AGENTS.md
!_INDICE.md
!manifest.example.json

# Tracked directories and their public scaffold docs.
!context/
!context/README.md
!context/.gitkeep
!preferences/
!preferences/README.md
!preferences/.gitkeep
!memory/
!memory/README.md
!memory/.gitkeep
!sources/
!sources/README.md
!sources/.gitkeep
!resources/
!resources/README.md
!resources/.gitkeep
!personal-skills/
!personal-skills/README.md
!personal-skills/_INDICE.md
!personal-skills/.jm-adk-personal-skills.json
!personal-skills/skills/
!personal-skills/skills/.gitkeep
!schemas/
!schemas/README.md
!schemas/*.schema.json
""",
        "README.md": """# JM-ADK User Context

This directory is the in-kit context repo for durable user context.

It is identified by `.jm-adk-context.json`, not by whatever files the user adds
later. Keep the marker intact so Alfa recognizes this directory even when
private contents change.

Read `_INDICE.md` first. Never bulk-load `sources/` or `resources/`. Write here
only after an explicit remember/update-context instruction from the user.
""",
        "AGENTS.md": """# AGENTS.md · JM-ADK User Context

This directory is the user's durable context repo inside Alfa.

The role of this directory comes from `.jm-adk-context.json`, not from private
files the user may add later.

Read `_INDICE.md` first. Do not bulk-load `sources/` or `resources/`. Personal
skills belong under `personal-skills/skills/` and sync out by copy mirror only.
Task artifacts belong in `workspace/{active}/artifacts/`.
""",
        "_INDICE.md": """# _INDICE.md · User Context

This index is intentionally sparse. Add links to user-approved context files as
they are created locally.

Identity is defined by `.jm-adk-context.json`; private files listed here may
change without changing this directory's role as the Alfa context repo.

| Area | Purpose |
|---|---|
| `context/` | Durable background and reusable user context |
| `preferences/` | Stable preferences for output, tooling, autonomy, and privacy |
| `memory/` | Long-lived notes explicitly approved by the user |
| `sources/` | Private source files or source indexes |
| `resources/` | Curated persistent user resources |
| `personal-skills/` | Canonical private source for user-authored skills |
| `schemas/` | Context schemas and validation references |
""",
        "manifest.example.json": json.dumps(
            {
                "schema": 1,
                "kind": "jm-adk-user-context-manifest",
                "owner": "local-user",
                "updated": today,
                "autoload": ["_INDICE.md"],
                "privacy": {"mode": "local-private", "externalConnectors": "deny-by-default"},
                "notes": "Copy to manifest.json for local private use. manifest.json is ignored by git.",
            },
            indent=2,
        ) + "\n",
        "context/README.md": "# Context\n\nStore durable user background here only after explicit user approval.\n",
        "context/.gitkeep": "\n",
        "preferences/README.md": "# Preferences\n\nStore stable user preferences here only after explicit user approval.\n",
        "preferences/.gitkeep": "\n",
        "memory/README.md": "# Memory\n\nStore durable notes that should outlive task workspaces.\n",
        "memory/.gitkeep": "\n",
        "sources/README.md": "# Sources\n\nStore private source files or source indexes here. Do not bulk-load this directory.\n",
        "sources/.gitkeep": "\n",
        "resources/README.md": "# Resources\n\nStore curated, persistent user resources here only after explicit user approval.\n",
        "resources/.gitkeep": "\n",
        "personal-skills/README.md": "# Personal Skills\n\nCanonical private source for user-authored skills. Use `scripts/scaffold-skill.py --personal`.\n",
        "personal-skills/_INDICE.md": "# _INDICE.md · Personal Skills\n\nList private user-authored skills here when the user creates them locally.\n",
        "personal-skills/.jm-adk-personal-skills.json": json.dumps(
            {
                "schema": 1,
                "kind": "jm-adk-personal-skills",
                "version": "1.0.0",
                "root": f"{context_root_name}/personal-skills",
                "skillsRoot": f"{context_root_name}/personal-skills/skills",
                "syncMode": "copy",
                "trackedPolicy": "scaffold-only",
                "runtimes": ["alfa-local", "codex", "claude", "gemini", "antigravity", "visual-studio"],
                "writePolicy": "explicit-personal-skill-update-only",
            },
            indent=2,
        ) + "\n",
        "personal-skills/skills/.gitkeep": "\n",
        "schemas/README.md": "# Schemas\n\nPublic schemas for the local user-context repo.\n",
        "schemas/user-context-manifest.schema.json": schema(
            "JM-ADK User Context Manifest",
            "Optional private manifest for local context loading. Repo identity is defined by .jm-adk-context.json, not by this file.",
            ["schema", "kind", "autoload", "privacy"],
            {
                "schema": {"const": 1},
                "kind": {"const": "jm-adk-user-context-manifest"},
                "autoload": {"type": "array", "items": {"type": "string"}, "maxItems": 12},
                "privacy": {"type": "object"},
            },
        ),
        "schemas/context-card.schema.json": schema(
            "JM-ADK Context Card",
            "Optional durable context card. It may describe user-approved context but never defines the repo identity.",
            ["schema", "kind", "title", "summary", "privacy"],
            {
                "schema": {"const": 1},
                "kind": {"const": "jm-adk-context-card"},
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "privacy": {"enum": ["local-private", "pii-safe", "public-safe"]},
            },
        ),
        "schemas/resource-card.schema.json": schema(
            "JM-ADK Resource Card",
            "Optional index card for a private user resource.",
            ["schema", "kind", "title", "resourceType", "privacy"],
            {
                "schema": {"const": 1},
                "kind": {"const": "jm-adk-resource-card"},
                "title": {"type": "string"},
                "resourceType": {"enum": ["cv", "identification", "url", "document", "reference", "other"]},
                "privacy": {"enum": ["local-private", "pii-safe", "public-safe"]},
            },
        ),
        "schemas/personal-skills-manifest.schema.json": schema(
            "JM-ADK Personal Skills Manifest",
            "Marker and sync contract for private user-authored skills inside user-context.",
            ["schema", "kind", "root", "skillsRoot", "syncMode", "trackedPolicy"],
            {
                "schema": {"const": 1},
                "kind": {"const": "jm-adk-personal-skills"},
                "root": {"type": "string"},
                "skillsRoot": {"type": "string"},
                "syncMode": {"const": "copy"},
                "trackedPolicy": {"const": "scaffold-only"},
            },
        ),
    }


def local_profile_payload(path: str) -> dict[str, object]:
    return {"enabled": True, "root": path, "autoload": False, "privacyMode": "local-private", "maxFiles": 12}


def merge_local_config(root: Path, context_root: str, force: bool) -> tuple[str, str]:
    target = root / ".jm-adk.local.json"
    if target.exists():
        data = json.loads(target.read_text(encoding="utf-8"))
    else:
        data = {"schema": 1, "generatedBy": GENERATOR}
    if "userContext" in data and not force:
        return "skip", ".jm-adk.local.json already has userContext; use --force to replace it"
    data["userContext"] = local_profile_payload(context_root)
    data.setdefault("personalSkills", {"targets": {}})
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return "write", str(target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold the in-kit JM-ADK user-context repo")
    parser.add_argument("--root", default=".", help="Alfa repo root")
    parser.add_argument("--context-root", default=DEFAULT_ROOT, help="Context root relative to Alfa")
    parser.add_argument("--apply", action="store_true", help="Write files")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without changing files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    parser.add_argument("--configure-local", action="store_true", help="Add userContext to .jm-adk.local.json")
    args = parser.parse_args()

    root = repo_root(Path(args.root))
    if Path(args.context_root).is_absolute() or ".." in Path(args.context_root).parts:
        print("ERROR: --context-root must be a safe path inside Alfa")
        return 2
    context_root = root / args.context_root
    planned = scaffold_files(args.context_root)
    writes: list[tuple[str, Path]] = []
    skips: list[Path] = []

    for rel, _content in planned.items():
        target = context_root / rel
        if target.exists() and not args.force:
            skips.append(target)
        else:
            writes.append((rel, target))

    if not args.apply:
        print(f"DRY-RUN: context root {context_root}")
        for rel, target in writes:
            print(f"write: {target}")
        for target in skips:
            print(f"skip-existing: {target}")
        if args.configure_local:
            print(f"would configure: {root / '.jm-adk.local.json'}")
        return 0

    for rel, target in writes:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(planned[rel], encoding="utf-8")
        print(f"WROTE: {target}")
    for target in skips:
        print(f"SKIP: {target}")

    if args.configure_local:
        action, detail = merge_local_config(root, args.context_root, args.force)
        print(f"{action.upper()}: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
