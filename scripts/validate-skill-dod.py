#!/usr/bin/env python3
"""Validate one skill against the JM-ADK Definition of Done.

The gate is intentionally per-skill. The catalog can advance one skill at a
time without implying every skill is already certified.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_CORE_FILES = [
    "SKILL.md",
    "README.md",
    "agents/lead.md",
    "agents/support.md",
    "agents/guardian.md",
    "agents/specialist.md",
    "knowledge/body-of-knowledge.md",
    "knowledge/knowledge-graph.json",
    "prompts/primary.md",
    "prompts/meta.md",
    "prompts/variations/quick.md",
    "prompts/variations/deep.md",
    "templates/output.md",
    "evals/evals.json",
    "examples/example-input.md",
    "examples/example-output.md",
]
GENERIC_MARKERS = [
    "Use this file for stable domain knowledge",
    "Add project-specific references as they become stable",
    "Use `{{skill}}` to produce a concise deliverable",
    "Example output for `{{skill}}`",
    "produce a complete deliverable",
    "realistic project request",
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


def read_json(path: Path) -> tuple[object | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def check_required_files(skill_dir: Path) -> list[str]:
    return [f"{skill_dir}: missing {rel}" for rel in REQUIRED_CORE_FILES if not (skill_dir / rel).exists()]


def check_assets(skill_dir: Path, slug: str) -> list[str]:
    errors: list[str] = []
    assets_dir = skill_dir / "assets"
    manifest_path = assets_dir / "manifest.json"
    readme_path = assets_dir / "README.md"
    if not assets_dir.exists():
        return [f"{skill_dir}: missing assets/ directory"]
    if not readme_path.exists():
        errors.append(f"{skill_dir}: missing assets/README.md")
    if not manifest_path.exists():
        errors.append(f"{skill_dir}: missing assets/manifest.json")
        return errors

    manifest, json_error = read_json(manifest_path)
    if json_error:
        return [f"{manifest_path}: invalid JSON: {json_error}"]
    if not isinstance(manifest, dict):
        return [f"{manifest_path}: root must be a JSON object"]
    if manifest.get("skill") != slug:
        errors.append(f"{manifest_path}: skill must be {slug}")
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append(f"{manifest_path}: assets must be a non-empty list")
        return errors

    for item in assets:
        if not isinstance(item, dict):
            errors.append(f"{manifest_path}: every asset entry must be an object")
            continue
        rel = str(item.get("path", ""))
        if not rel.startswith("assets/"):
            errors.append(f"{manifest_path}: asset path must start with assets/: {rel}")
            continue
        asset_path = skill_dir / rel
        if not asset_path.exists():
            errors.append(f"{manifest_path}: asset file does not exist: {rel}")
        if not str(item.get("type", "")).strip():
            errors.append(f"{manifest_path}: asset missing type: {rel}")
        if not str(item.get("purpose", "")).strip():
            errors.append(f"{manifest_path}: asset missing purpose: {rel}")
        used_by = item.get("used_by")
        if not isinstance(used_by, list) or not used_by:
            errors.append(f"{manifest_path}: asset missing used_by list: {rel}")
        else:
            for target in used_by:
                if not (skill_dir / str(target)).exists():
                    errors.append(f"{manifest_path}: used_by target missing for {rel}: {target}")

    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if "assets/" not in skill_md:
        errors.append(f"{skill_dir / 'SKILL.md'}: must reference assets/")
    return errors


def check_non_generic_content(skill_dir: Path, slug: str) -> list[str]:
    errors: list[str] = []
    markers = [marker.replace("{{skill}}", slug) for marker in GENERIC_MARKERS]
    for rel in ["knowledge/body-of-knowledge.md", "examples/example-input.md", "examples/example-output.md"]:
        path = skill_dir / rel
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker in text:
                errors.append(f"{path}: generic scaffold marker remains: {marker}")
    return errors


def check_evals(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    path = skill_dir / "evals" / "evals.json"
    data, json_error = read_json(path)
    if json_error:
        return [f"{path}: invalid JSON: {json_error}"]
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return [f"{path}: evals must contain a cases list"]
    cases = [case for case in data["cases"] if isinstance(case, dict)]
    if len(cases) < 8:
        errors.append(f"{path}: expected at least 8 eval cases")
    expected_checks = {
        check
        for case in cases
        if isinstance(case.get("expected_checks"), list)
        for check in case["expected_checks"]
    }
    for required in {"assets", "deterministic_scripts", "quality_criteria"}:
        if required not in expected_checks:
            errors.append(f"{path}: expected_checks must include {required}")
    generic_inputs = [
        str(case.get("input", ""))
        for case in cases
        if re.search(r"produce a complete deliverable|rich_context|minimal_input", str(case.get("input", "")))
    ]
    if generic_inputs:
        errors.append(f"{path}: generic eval inputs remain")
    return errors


def run_command(root: Path, command: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one JM-ADK skill against DoD")
    parser.add_argument("--skill", required=True, help="Skill slug to validate")
    parser.add_argument("--skip-script-checks", action="store_true", help="Skip scripts/check.sh runtime checks")
    args = parser.parse_args()

    root = repo_root()
    skill_dir = root / "skills" / args.skill
    errors: list[str] = []
    if not skill_dir.exists():
        errors.append(f"missing skill directory: {skill_dir}")
    else:
        errors.extend(check_required_files(skill_dir))
        errors.extend(check_assets(skill_dir, args.skill))
        errors.extend(check_non_generic_content(skill_dir, args.skill))
        errors.extend(check_evals(skill_dir))

    if not errors and not args.skip_script_checks and (skill_dir / "scripts").exists():
        code, output = run_command(
            root,
            ["python3", "-B", "scripts/validate-skill-scripts.py", "--strict", "--run-checks", "--skill", args.skill],
        )
        if code != 0:
            errors.append(f"script contract failed for {args.skill}:\n{output}")
        else:
            print(output)

    for error in errors:
        print(f"ERROR: {error}")
    print(f"skill={args.skill} dod={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
