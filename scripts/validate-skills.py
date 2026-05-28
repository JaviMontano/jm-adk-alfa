#!/usr/bin/env python3
"""Validate JM-ADK skill structure and metadata."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
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
REQUIRED_FRONTMATTER = ["name", "version", "description"]
ALLOWED_TOOLS = {
    "Bash",
    "Edit",
    "Glob",
    "Grep",
    "MultiEdit",
    "NotebookEdit",
    "Read",
    "Task",
    "TodoWrite",
    "WebFetch",
    "WebSearch",
    "Write",
}
HIGH_RISK_TRIGGERS = {"create", "build", "deploy", "test", "analyze", "review", "fix", "audit", "design"}


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Path(result.stdout.strip())


def parse_frontmatter(path: Path) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}, ["missing or malformed frontmatter"]
    data: dict[str, object] = {}
    current: str | None = None
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current:
            data.setdefault(current, [])
            if isinstance(data[current], list):
                data[current].append(stripped[2:].strip().strip("\"'"))
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current = key
            if not value:
                data[key] = []
            elif value.startswith("[") and value.endswith("]"):
                data[key] = [part.strip().strip("\"'") for part in value[1:-1].split(",") if part.strip()]
            else:
                data[key] = value.strip("\"'")
    return data, errors


def extract_triggers(fm: dict[str, object], body: str, slug: str) -> list[str]:
    values: list[str] = []
    raw = fm.get("triggers")
    if isinstance(raw, list):
        values.extend(str(item).strip().lower() for item in raw if str(item).strip())
    elif isinstance(raw, str) and raw.strip():
        values.extend(part.strip().lower() for part in raw.split(",") if part.strip())
    for match in re.finditer(r"trigger[s]?:\s*([^\n]+)", body, re.IGNORECASE):
        values.extend(part.strip(" \"'.,").lower() for part in match.group(1).split(",") if part.strip(" \"'.,"))
    if not values:
        values.append(slug)
    return sorted(set(values))


def validate_json(path: Path) -> list[str]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"invalid JSON in {path}: {exc}"]
    return []


def validate_links(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)", text):
        clean = target.split("#", 1)[0].strip()
        if not clean:
            continue
        candidate = (path.parent / clean).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(f"{path}: link escapes repo: {target}")
            continue
        if not candidate.exists():
            errors.append(f"{path}: broken internal link: {target}")
    return errors


def validate_skill(skill_dir: Path, root: Path, strict: bool) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    triggers: list[str] = []
    for rel in REQUIRED_FILES:
        path = skill_dir / rel
        if not path.exists():
            (errors if strict else warnings).append(f"{skill_dir}: missing {rel}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return errors, warnings, triggers

    fm, fm_errors = parse_frontmatter(skill_md)
    errors.extend(f"{skill_md}: {err}" for err in fm_errors)
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            errors.append(f"{skill_md}: missing required frontmatter field: {field}")
    name = str(fm.get("name", ""))
    if name and name != skill_dir.name:
        warnings.append(f"{skill_md}: name '{name}' differs from directory '{skill_dir.name}'")
    tools = fm.get("allowed-tools") or fm.get("allowed_tools") or []
    if isinstance(tools, str):
        tools = [part.strip() for part in tools.split(",") if part.strip()]
    if strict and not tools:
        warnings.append(f"{skill_md}: missing allowed-tools")
    for tool in tools if isinstance(tools, list) else []:
        if str(tool) not in ALLOWED_TOOLS:
            warnings.append(f"{skill_md}: unknown allowed tool '{tool}'")
    body = skill_md.read_text(encoding="utf-8")
    triggers = extract_triggers(fm, body, skill_dir.name)

    for json_rel in ["evals/evals.json", "knowledge/knowledge-graph.json"]:
        path = skill_dir / json_rel
        if path.exists():
            errors.extend(validate_json(path))
    for md in skill_dir.rglob("*.md"):
        errors.extend(validate_links(md, root))
    return errors, warnings, triggers


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JM-ADK skills")
    parser.add_argument("--strict", action="store_true", help="Require every canonical scaffold file")
    parser.add_argument("--skills-dir", default="skills")
    args = parser.parse_args()
    root = repo_root()
    skills_dir = root / args.skills_dir
    errors: list[str] = []
    warnings: list[str] = []
    trigger_map: dict[str, list[str]] = {}

    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_errors, skill_warnings, triggers = validate_skill(skill_dir, root, args.strict)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
        for trigger in triggers:
            trigger_map.setdefault(trigger, []).append(skill_dir.name)

    for trigger, skills in sorted(trigger_map.items()):
        if len(skills) > 1 and trigger in HIGH_RISK_TRIGGERS:
            errors.append(f"high-risk duplicate trigger '{trigger}' used by: {', '.join(skills[:12])}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"skills={len([p for p in skills_dir.iterdir() if p.is_dir()])} warnings={len(warnings)} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
