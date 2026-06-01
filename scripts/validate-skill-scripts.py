#!/usr/bin/env python3
"""Validate deterministic script contracts inside JM-ADK skills.

The canonical skill scaffold is validated by validate-skills.py. This script
adds the narrower contract for skills that include local automation under
skills/<slug>/scripts/.

Default mode is static and non-destructive. Use --run-checks to execute each
scripts/check.sh from the repository root.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_EXTENSIONS = {".sh", ".py"}
DANGEROUS_SHELL_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fd",
    r"\bsudo\b",
]


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Path(result.stdout.strip())


def validate_json(path: Path) -> list[str]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: invalid JSON fixture: {exc}"]
    return []


def validate_shell_script(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not re.match(r"^#!(/usr/bin/env bash|/bin/bash)$", lines[0]):
        errors.append(f"{path}: shell script must start with a bash shebang")
    if "set -euo pipefail" not in "\n".join(lines[:20]):
        errors.append(f"{path}: shell script must enable set -euo pipefail near the top")
    for pattern in DANGEROUS_SHELL_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"{path}: contains dangerous shell pattern: {pattern}")
    return errors


def validate_python_script(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        compile(text, str(path), "exec")
    except SyntaxError as exc:
        errors.append(f"{path}: Python syntax error: {exc}")
    if "__main__" not in text:
        errors.append(f"{path}: Python script should expose a __main__ entry point")
    return errors


def skill_mentions_scripts(skill_md: Path, script_names: list[str]) -> bool:
    if not skill_md.exists():
        return False
    body = skill_md.read_text(encoding="utf-8")
    if "scripts/" in body:
        return True
    return any(name in body for name in script_names)


def run_check(root: Path, check_path: Path, timeout: int) -> tuple[int, str]:
    result = subprocess.run(
        ["bash", str(check_path)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def validate_skill_scripts(
    root: Path,
    skill_dir: Path,
    strict: bool,
    run_checks: bool,
    timeout: int,
) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    check_logs: list[str] = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return errors, warnings, check_logs

    scripts = sorted(
        p
        for p in scripts_dir.rglob("*")
        if p.is_file() and not p.name.startswith(".") and p.suffix in SCRIPT_EXTENSIONS
    )
    script_names = [str(p.relative_to(skill_dir)) for p in scripts]
    if not scripts:
        errors.append(f"{skill_dir}: scripts/ exists but contains no .sh or .py scripts")

    readme = scripts_dir / "README.md"
    if strict and not readme.exists():
        errors.append(f"{skill_dir}: scripts/README.md is required")

    fixtures_dir = scripts_dir / "fixtures"
    fixtures = sorted(fixtures_dir.rglob("*.json")) if fixtures_dir.exists() else []
    if strict and not fixtures:
        errors.append(f"{skill_dir}: scripts/fixtures/*.json is required for deterministic checks")
    for fixture in fixtures:
        errors.extend(validate_json(fixture))

    check_path = scripts_dir / "check.sh"
    if strict and not check_path.exists():
        errors.append(f"{skill_dir}: scripts/check.sh is required")

    if strict and not skill_mentions_scripts(skill_dir / "SKILL.md", script_names):
        errors.append(f"{skill_dir}: SKILL.md must reference scripts/ or the script entry point")

    for script in scripts:
        if script.suffix == ".sh":
            errors.extend(validate_shell_script(script))
        elif script.suffix == ".py":
            errors.extend(validate_python_script(script))

    if run_checks and check_path.exists():
        code, output = run_check(root, check_path, timeout)
        if code != 0:
            errors.append(f"{skill_dir}: scripts/check.sh failed with exit {code}\n{output}")
        else:
            check_logs.append(f"PASS {skill_dir.name}: {output}")
    elif not run_checks and check_path.exists():
        warnings.append(f"{skill_dir}: scripts/check.sh not executed; pass --run-checks for runtime validation")

    return errors, warnings, check_logs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JM-ADK skill script contracts")
    parser.add_argument("--skills-dir", default="skills")
    parser.add_argument("--skill", help="Validate one skill slug")
    parser.add_argument("--strict", action="store_true", help="Require README, fixtures, check.sh, and SKILL.md references")
    parser.add_argument("--run-checks", action="store_true", help="Execute each scripts/check.sh")
    parser.add_argument("--timeout", type=int, default=30, help="Per-skill check timeout in seconds")
    args = parser.parse_args()

    root = repo_root()
    skills_dir = root / args.skills_dir
    errors: list[str] = []
    warnings: list[str] = []
    check_logs: list[str] = []
    skills_with_scripts = 0

    candidates = [skills_dir / args.skill] if args.skill else sorted(p for p in skills_dir.iterdir() if p.is_dir())
    for skill_dir in candidates:
        if not skill_dir.exists():
            errors.append(f"missing skill directory: {skill_dir}")
            continue
        if not (skill_dir / "scripts").exists():
            continue
        skills_with_scripts += 1
        skill_errors, skill_warnings, skill_logs = validate_skill_scripts(
            root=root,
            skill_dir=skill_dir,
            strict=args.strict,
            run_checks=args.run_checks,
            timeout=args.timeout,
        )
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
        check_logs.extend(skill_logs)

    for log in check_logs:
        print(log)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"skills_with_scripts={skills_with_scripts} warnings={len(warnings)} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
