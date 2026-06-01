#!/usr/bin/env python3
"""Diagnose JM-ADK personal skills without modifying files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


DEFAULT_ROOT = "user-context/personal-skills"
DEFAULT_SKILLS_ROOT = "user-context/personal-skills/skills"
MARKER = ".jm-adk-personal-skills.json"
EXPECTED_KIND = "jm-adk-personal-skills"
UNSAFE_TEXT = [re.compile(r"file://", re.IGNORECASE), re.compile(r"/Users/[^\s)]+"), re.compile(r"~/(?!\.codex/skills|\.agents/skills)")]


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


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def tracked_files(root: Path, rel: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--", rel],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def load_config(root: Path) -> dict[str, str]:
    config = {"root": DEFAULT_ROOT, "skillsRoot": DEFAULT_SKILLS_ROOT}
    path = root / ".jm-adk.json"
    if path.exists():
        data, error = read_json(path)
        if not error and isinstance(data, dict):
            personal = data.get("personalSkills", {})
            if isinstance(personal, dict):
                config["root"] = str(personal.get("root", config["root"]))
                config["skillsRoot"] = str(personal.get("skillsRoot", config["skillsRoot"]))
    return config


def skill_dirs(skills_root: Path) -> list[Path]:
    if not skills_root.exists():
        return []
    return sorted(p for p in skills_root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def unsafe_links(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    for md in skill_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for pattern in UNSAFE_TEXT:
            if pattern.search(text):
                problems.append(f"{md}: unsafe absolute or file URL reference")
                break
        for target in re.findall(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)", text):
            clean = target.split("#", 1)[0].strip()
            if not clean:
                continue
            if clean.startswith("file://") or Path(clean).is_absolute():
                problems.append(f"{md}: unsafe link target: {target}")
                continue
            candidate = (md.parent / clean).resolve()
            if not is_inside(candidate, skill_dir):
                problems.append(f"{md}: link escapes personal skill: {target}")
            elif not candidate.exists():
                problems.append(f"{md}: broken internal link: {target}")
    return problems


def validate_with_core(root: Path, skills_root_rel: str) -> list[str]:
    result = subprocess.run(
        ["python3", str(root / "scripts/validate-skills.py"), "--strict", "--skills-dir", skills_root_rel],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return [] if result.returncode == 0 else [result.stdout.strip()]


def diagnose(root: Path) -> dict[str, Any]:
    config = load_config(root)
    personal_root = (root / config["root"]).resolve()
    skills_root = (root / config["skillsRoot"]).resolve()
    problems: list[str] = []
    checks: dict[str, Any] = {
        "marker": "unknown",
        "skills_root": str(skills_root),
        "private_tracked_files": [],
        "core_slug_collisions": [],
        "unsafe_links": [],
        "validator": "not_run",
    }

    if not personal_root.exists():
        return {"schema": 1, "status": "missing", "config": config, "checks": checks, "problems": problems}

    marker_path = personal_root / MARKER
    marker, marker_error = read_json(marker_path)
    if marker_error:
        checks["marker"] = f"invalid: {marker_error}"
        problems.append(f"{MARKER} invalid: {marker_error}")
    elif marker.get("kind") != EXPECTED_KIND:
        checks["marker"] = f"invalid kind: {marker.get('kind')}"
        problems.append(f"{MARKER} kind must be {EXPECTED_KIND}")
    else:
        checks["marker"] = "pass"

    if not skills_root.exists():
        problems.append("personal skills root is missing")
    elif not is_inside(skills_root, personal_root):
        problems.append("personal skills root must stay inside user-context/personal-skills")

    private_tracked = [p for p in tracked_files(root, config["skillsRoot"]) if p != f"{config['skillsRoot']}/.gitkeep"]
    checks["private_tracked_files"] = private_tracked
    if private_tracked:
        problems.append("private personal skill content is tracked by git")

    core_slugs = {p.name for p in (root / "skills").iterdir() if p.is_dir()} if (root / "skills").exists() else set()
    personal_slugs = [p.name for p in skill_dirs(skills_root)]
    collisions = sorted(core_slugs.intersection(personal_slugs))
    checks["core_slug_collisions"] = collisions
    if collisions:
        problems.append("personal skill slug collides with Alfa core skill")

    link_problems: list[str] = []
    for skill_dir in skill_dirs(skills_root):
        link_problems.extend(unsafe_links(skill_dir))
    checks["unsafe_links"] = link_problems
    problems.extend(link_problems)

    validator_errors = validate_with_core(root, config["skillsRoot"])
    checks["validator"] = "pass" if not validator_errors else validator_errors
    problems.extend(validator_errors)

    status = "ready" if not problems else "degraded"
    if status == "ready" and not personal_slugs:
        status = "empty"
    return {"schema": 1, "status": status, "config": config, "checks": checks, "problems": problems}


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose JM-ADK personal skills")
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Compatibility flag; diagnosis is read-only")
    args = parser.parse_args()
    root = repo_root(Path(args.root))
    result = diagnose(root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"PERSONAL_SKILLS_STATUS: {result['status']}")
        for problem in result.get("problems", []):
            print(f"PROBLEM: {problem}")
    return 1 if result["status"] == "degraded" else 0


if __name__ == "__main__":
    raise SystemExit(main())
