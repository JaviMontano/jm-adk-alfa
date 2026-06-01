#!/usr/bin/env python3
"""Copy personal skills to local runtime skill roots safely."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SKILLS_ROOT = "user-context/personal-skills/skills"
RUNTIME_ALIASES = {
    "visual-studio": "visualStudio",
    "visualstudio": "visualStudio",
    "alfa-local": "alfaLocal",
    "alfalocal": "alfaLocal",
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


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def config(root: Path) -> tuple[Path, dict[str, str]]:
    shared = read_json(root / ".jm-adk.json")
    local = read_json(root / ".jm-adk.local.json")
    personal = shared.get("personalSkills", {}) if isinstance(shared.get("personalSkills"), dict) else {}
    local_personal = local.get("personalSkills", {}) if isinstance(local.get("personalSkills"), dict) else {}
    skills_root = root / str(personal.get("skillsRoot", DEFAULT_SKILLS_ROOT))
    raw_targets = local_personal.get("targets", {}) if isinstance(local_personal.get("targets"), dict) else {}
    targets = {str(k): str(v) for k, v in raw_targets.items() if str(v).strip()}
    return skills_root, targets


def normalize_runtime(runtime: str) -> str:
    key = runtime.strip()
    return RUNTIME_ALIASES.get(key, key)


def discover_target(root: Path, runtime: str, explicit: str | None, targets: dict[str, str]) -> Path:
    if explicit:
        raw = explicit
    else:
        key = normalize_runtime(runtime)
        raw = targets.get(key) or targets.get(runtime)
        if not raw and runtime == "alfa-local":
            raw = ".local/skills"
        if not raw and runtime == "codex" and (Path.home() / ".codex/skills").exists():
            raw = str(Path.home() / ".codex/skills")
        if not raw and runtime == "claude" and (Path.home() / ".agents/skills").exists():
            raw = str(Path.home() / ".agents/skills")
    if not raw:
        raise ValueError(f"no target configured or discoverable for runtime: {runtime}")
    if raw.startswith("file://"):
        raise ValueError("target must be a filesystem path, not file:// URL")
    path = Path(os.path.expanduser(raw))
    return (root / path).resolve() if not path.is_absolute() else path.resolve()


def reject_unsafe_target(root: Path, source: Path, target: Path) -> None:
    blocked = [
        root / "skills",
        root / "agents",
        root / "commands",
        root / "prompts",
        root / "workspace",
        root / ".agent/skills",
        root / "user-context/resources",
        source,
    ]
    for item in blocked:
        if is_inside(target, item):
            raise ValueError(f"unsafe target inside protected path: {target}")
    if target.exists() and target.is_symlink():
        raise ValueError(f"target must be a real directory, not a symlink: {target}")
    for parent in target.parents:
        if parent == root.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise ValueError(f"target parent is a symlink: {parent}")


def source_skills(source: Path) -> list[Path]:
    if not source.exists():
        return []
    return sorted(p for p in source.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def files_for(skill: Path) -> list[Path]:
    return sorted(p for p in skill.rglob("*") if p.is_file() and not p.name.startswith(".DS_Store"))


def plan(source: Path, target: Path, force: bool) -> tuple[list[tuple[Path, Path, str]], list[str]]:
    actions: list[tuple[Path, Path, str]] = []
    conflicts: list[str] = []
    for skill in source_skills(source):
        for src in files_for(skill):
            if src.is_symlink():
                conflicts.append(f"source symlink is not allowed: {src}")
                continue
            rel = src.relative_to(source)
            dst = target / rel
            if not dst.exists():
                actions.append((src, dst, "copy"))
            elif dst.is_symlink():
                conflicts.append(f"destination symlink is not allowed: {dst}")
            elif sha256(src) == sha256(dst):
                actions.append((src, dst, "skip"))
            elif force:
                actions.append((src, dst, "overwrite"))
            else:
                conflicts.append(f"conflict: {dst}")
    return actions, conflicts


def write_manifest(target: Path, source: Path, actions: list[tuple[Path, Path, str]], runtime: str) -> None:
    payload = {
        "schema": 1,
        "kind": "jm-adk-personal-skills-sync-manifest",
        "runtime": runtime,
        "source": str(source),
        "target": str(target),
        "syncMode": "copy",
        "updated": datetime.now(timezone.utc).isoformat(),
        "files": [
            {"path": str(dst.relative_to(target)), "sha256": sha256(src), "action": action}
            for src, dst, action in actions
            if action in {"copy", "overwrite", "skip"}
        ],
    }
    (target / ".jm-adk-personal-skills-sync.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync personal skills by safe copy mirror")
    parser.add_argument("--root", default=".")
    parser.add_argument("--runtime", default="alfa-local", choices=["auto", "alfa-local", "codex", "claude", "gemini", "antigravity", "visual-studio"])
    parser.add_argument("--target", help="Explicit target skills directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite changed target files after review")
    args = parser.parse_args()

    if args.dry_run and args.apply:
        parser.error("--dry-run and --apply are mutually exclusive")
    if not args.dry_run and not args.apply:
        args.dry_run = True

    root = repo_root(Path(args.root))
    source, targets = config(root)
    runtime = "alfa-local" if args.runtime == "auto" else args.runtime
    try:
        target = discover_target(root, runtime, args.target, targets)
        reject_unsafe_target(root, source.resolve(), target)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

    actions, conflicts = plan(source, target, args.force)
    for conflict in conflicts:
        print(f"CONFLICT: {conflict}")
    for src, dst, action in actions:
        print(f"{action}: {src.relative_to(source)} -> {dst}")
    if conflicts:
        return 1
    if args.dry_run:
        print(f"DRY-RUN: source={source} target={target} files={len(actions)}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for src, dst, action in actions:
        if action == "skip":
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    write_manifest(target, source, actions, runtime)
    print(f"APPLIED: source={source} target={target} files={len(actions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
