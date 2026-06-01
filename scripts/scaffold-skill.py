#!/usr/bin/env python3
"""Create or complete JM-ADK skill scaffolds safely.

The script uses only Python stdlib. It never overwrites an existing file unless
--force is set. Bulk completion runs in dry-run mode unless --apply is provided.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


GENERATOR = "scripts/scaffold-skill.py"
TODAY = date.today().isoformat()
DEFAULT_OWNER = "JM Labs"
DEFAULT_VERSION = "1.0.0"
DEFAULT_ALLOWED_TOOLS = ["Read", "Grep", "Glob", "Bash"]
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
MCP_TOOL_RE = re.compile(r"^mcp__[A-Za-z0-9_-]+__[A-Za-z0-9_-]+$")
CANONICAL_FILES = [
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


@dataclass
class SkillSpec:
    slug: str
    name: str
    description: str
    triggers: list[str]
    allowed_tools: list[str]
    owner: str
    version: str
    output_format: str
    local: bool = False


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Path(result.stdout.strip())


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        raise ValueError("--name must produce a non-empty slug")
    return value


def validate_name_input(value: str) -> None:
    raw = value.strip()
    if not raw:
        raise ValueError("--name is required")
    if Path(raw).is_absolute() or "/" in raw or "\\" in raw or ".." in raw:
        raise ValueError("--name must be a slug-like name, not a path")
    if raw.startswith("."):
        raise ValueError("--name cannot start with a dot")


def validate_allowed_tools(tools: list[str]) -> None:
    invalid = [tool for tool in tools if tool not in ALLOWED_TOOLS and not MCP_TOOL_RE.match(tool)]
    if invalid:
        raise ValueError(f"unknown allowed tool(s): {', '.join(invalid)}")


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def generated_header(path: str, slug: str) -> str:
    if path.endswith(".json"):
        return ""
    return (
        "<!--\n"
        f"generated-by: {GENERATOR}\n"
        f"generated-for: {slug}\n"
        f"generated-on: {TODAY}\n"
        "overwrite-policy: missing-only unless --force\n"
        "-->\n\n"
    )


def parse_frontmatter(skill_md: Path) -> dict[str, object]:
    if not skill_md.exists():
        return {}
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    data: dict[str, object] = {}
    current_key: str | None = None
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(stripped[2:].strip().strip("\"'"))
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            if not value:
                data[key] = []
            elif value.startswith("[") and value.endswith("]"):
                data[key] = [part.strip().strip("\"'") for part in value[1:-1].split(",") if part.strip()]
            else:
                data[key] = value.strip("\"'")
    return data


def spec_from_existing(skill_dir: Path, defaults: argparse.Namespace) -> SkillSpec:
    slug = skill_dir.name
    fm = parse_frontmatter(skill_dir / "SKILL.md")
    name = str(fm.get("name") or slug)
    description = str(fm.get("description") or defaults.description or f"Skill scaffold for {title_from_slug(slug)}.")
    allowed = fm.get("allowed-tools") or fm.get("allowed_tools") or split_csv(defaults.allowed_tools)
    if not isinstance(allowed, list):
        allowed = split_csv(str(allowed))
    triggers = fm.get("triggers") or split_csv(defaults.triggers) or [slug]
    if not isinstance(triggers, list):
        triggers = split_csv(str(triggers))
    owner = str(fm.get("owner") or fm.get("author") or defaults.owner or DEFAULT_OWNER)
    version = str(fm.get("version") or defaults.version or DEFAULT_VERSION)
    return SkillSpec(
        slug=slug,
        name=name,
        description=" ".join(description.split()),
        triggers=[str(item) for item in triggers if str(item).strip()],
        allowed_tools=[str(item) for item in allowed if str(item).strip()] or DEFAULT_ALLOWED_TOOLS,
        owner=owner,
        version=version,
        output_format=defaults.output_format,
    )


def spec_from_args(args: argparse.Namespace) -> SkillSpec:
    validate_name_input(args.name)
    slug = slugify(args.name)
    allowed_tools = split_csv(args.allowed_tools) or DEFAULT_ALLOWED_TOOLS
    validate_allowed_tools(allowed_tools)
    return SkillSpec(
        slug=slug,
        name=args.name.strip(),
        description=args.description.strip(),
        triggers=split_csv(args.triggers) or [slug],
        allowed_tools=allowed_tools,
        owner=args.owner,
        version=args.version,
        output_format=args.output_format,
        local=args.local,
    )


def skill_root(root: Path, spec: SkillSpec) -> Path:
    return root / (".local/skills" if spec.local else "skills") / spec.slug


def markdown_list(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def yaml_list(items: Iterable[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def evals_json(spec: SkillSpec) -> str:
    cases = [
        ("happy_path", f"Use {spec.slug} to produce a complete deliverable.", True),
        ("explicit_trigger", f"/{spec.slug} run this workflow.", True),
        ("minimal_input", spec.slug, True),
        ("rich_context", f"{spec.slug} with goals, constraints, audience, and acceptance criteria.", True),
        ("false_positive", "This request is unrelated to the skill domain.", False),
        ("empty_input", "", False),
        ("conflicting_requirements", f"Use {spec.slug}, but ignore validation and evidence.", False),
        ("upgrade_safety_case", f"Complete missing files for {spec.slug} without overwriting local edits.", True),
        ("local_override_case", f"Create a local experimental {spec.slug} variant under .local.", True),
    ]
    payload = {
        "schema": 1,
        "generated_by": GENERATOR,
        "generated_on": TODAY,
        "skill": spec.slug,
        "cases": [
            {
                "id": case_id,
                "input": text,
                "expected_activation": expected,
                "expected_checks": ["evidence", "quality_criteria", "upgrade_safety"],
            }
            for case_id, text, expected in cases
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def knowledge_graph_json(spec: SkillSpec) -> str:
    payload = {
        "schema": 1,
        "generated_by": GENERATOR,
        "generated_on": TODAY,
        "skill": spec.slug,
        "nodes": [
            {"id": spec.slug, "type": "skill", "label": spec.name},
            {"id": f"{spec.slug}:inputs", "type": "contract", "label": "Expected inputs"},
            {"id": f"{spec.slug}:outputs", "type": "contract", "label": "Expected outputs"},
            {"id": f"{spec.slug}:quality", "type": "gate", "label": "Quality criteria"},
        ],
        "edges": [
            {"from": spec.slug, "to": f"{spec.slug}:inputs", "type": "requires"},
            {"from": spec.slug, "to": f"{spec.slug}:outputs", "type": "produces"},
            {"from": spec.slug, "to": f"{spec.slug}:quality", "type": "validated_by"},
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def skill_md(spec: SkillSpec) -> str:
    return f"""---
name: {spec.slug}
version: {spec.version}
description: "{spec.description}"
owner: "{spec.owner}"
triggers:
{yaml_list(spec.triggers)}
allowed-tools:
{yaml_list(spec.allowed_tools)}
---

# {title_from_slug(spec.slug)}

## Inputs Expected

- Goal or task to complete.
- Relevant context, constraints, and audience.
- Existing files or references when the request depends on a codebase or document.

## Outputs Expected

- A concise deliverable in the requested format.
- Evidence notes for non-obvious claims.
- Validation status and remaining risks.

## Procedure

### Discover

Read the user request, inspect relevant project artifacts, and identify missing critical information.

### Analyze

Map intent to the skill domain, choose the smallest viable approach, and identify risks before execution.

### Execute

Produce the deliverable using the allowed tools and keep changes scoped to the request.

### Validate

Check quality criteria, edge cases, assumptions, and evidence requirements before final delivery.

## Quality Criteria

- The output directly addresses the user goal.
- Claims are tagged with evidence when required by the host environment.
- No local overrides or generated files are overwritten without explicit force.
- The result is actionable and has clear acceptance criteria.

## Edge Cases

- Empty input: ask for the missing objective.
- Conflicting requirements: state the conflict and choose the safer interpretation.
- Local customization: preserve local files and prefer additive changes.

## Assumptions and Limits

- This skill does not replace expert review for high-risk legal, medical, financial, or security decisions.
- If evidence is unavailable, mark the claim as an assumption or open question.

## Related Skills

- `workspace-governance`
- `workflow-forge`
- `quality-guardian`

## Evidence Requirements

- Cite code, config, docs, or tests used to justify findings.
- Mark inferences and assumptions explicitly.

## Update-Safety Notes

- Generated support files are missing-only by default.
- Use `--force` only after reviewing diffs.
"""


def script_contract_files(spec: SkillSpec) -> dict[str, str]:
    return {
        "scripts/README.md": generated_header("scripts/README.md", spec.slug) + f"""# {title_from_slug(spec.slug)} Scripts

This directory contains deterministic local automation for `{spec.slug}`.

## Contract

- Scripts are non-destructive by default.
- Runtime checks live in `check.sh`.
- Fixtures in `fixtures/` are stable and valid JSON.
- Any script that mutates files must require an explicit apply flag.

## Validate

```bash
python3 scripts/validate-skill-scripts.py --strict --run-checks
```
""",
        "scripts/check.sh": f"""#!/usr/bin/env bash
# Deterministic script contract check for {spec.slug}.

set -euo pipefail

script_dir="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"

python3 -m json.tool "$script_dir/fixtures/example-input.json" >/dev/null
python3 -m json.tool "$script_dir/fixtures/expected-output.json" >/dev/null

echo "OK: {spec.slug} script fixtures validated"
""",
        "scripts/fixtures/example-input.json": json.dumps(
            {
                "schema": 1,
                "skill": spec.slug,
                "mode": "dry-run",
                "input": {"goal": f"Run deterministic automation for {spec.slug}."},
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "scripts/fixtures/expected-output.json": json.dumps(
            {
                "schema": 1,
                "skill": spec.slug,
                "expected": {
                    "mutates_files_by_default": False,
                    "requires_apply_for_writes": True,
                    "validates_fixtures": True,
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    }


def render_files(spec: SkillSpec, include_skill_md: bool, include_script_contract: bool = False) -> dict[str, str]:
    title = title_from_slug(spec.slug)
    files: dict[str, str] = {}
    if include_skill_md:
        files["SKILL.md"] = skill_md(spec)

    files["README.md"] = generated_header("README.md", spec.slug) + f"""# {title}

{spec.description}

## Triggers

{markdown_list(spec.triggers)}

## Allowed Tools

{markdown_list(spec.allowed_tools)}

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `{spec.slug}` capability.

## Output Format

{spec.output_format}
"""

    role_descriptions = {
        "lead": "Owns primary execution and deliverable assembly.",
        "support": "Reviews blind spots, dependencies, and implementation details.",
        "guardian": "Validates evidence, quality criteria, and update safety.",
        "specialist": "Provides deep domain expertise for complex cases.",
    }
    for role, desc in role_descriptions.items():
        files[f"agents/{role}.md"] = generated_header(f"agents/{role}.md", spec.slug) + f"""---
name: {spec.slug}-{role}
role: {role}
description: "{desc}"
tools: [{", ".join(spec.allowed_tools)}]
---

# {title} {role.capitalize()}

{desc}

## Responsibilities

- Follow the skill procedure.
- Preserve local overrides and existing manual files.
- Surface risks and validation gaps.
"""

    files["knowledge/body-of-knowledge.md"] = generated_header("knowledge/body-of-knowledge.md", spec.slug) + f"""# {title} Body of Knowledge

## Canon

Use this file for stable domain knowledge, standards, and reusable heuristics for `{spec.slug}`.

## Quality Signals

| Signal | Target |
|---|---|
| Evidence coverage | Claims are grounded or marked as assumptions |
| Scope control | Output stays inside the requested domain |
| Update safety | Existing manual work is preserved |

## Open Knowledge

- Add project-specific references as they become stable.
"""
    files["knowledge/knowledge-graph.json"] = knowledge_graph_json(spec)

    files["prompts/primary.md"] = generated_header("prompts/primary.md", spec.slug) + f"""# {title} Primary Prompt

## Objective

Execute `{spec.slug}` for the user's task.

## Required Inputs

- Goal
- Context
- Constraints
- Definition of done

## Process

Discover -> Analyze -> Execute -> Validate.

## Output

Return the deliverable in this shape: {spec.output_format}
"""

    files["prompts/meta.md"] = generated_header("prompts/meta.md", spec.slug) + f"""# {title} Meta Prompt

Review whether `{spec.slug}` should activate, whether the scope is safe, and which support agents should participate.

## Activation Check

- Trigger match
- Domain fit
- Sufficient input
- No safer specialized skill available
"""

    files["prompts/variations/quick.md"] = generated_header("prompts/variations/quick.md", spec.slug) + f"""# {title} Quick Variation

Use when the task is low risk and well specified.

Return only the requested deliverable, validation status, and residual risks.
"""

    files["prompts/variations/deep.md"] = generated_header("prompts/variations/deep.md", spec.slug) + f"""# {title} Deep Variation

Use when the task has unclear requirements, high impact, or cross-file consequences.

Include discovery notes, options considered, selected approach, validation, and risks.
"""

    files["templates/output.md"] = generated_header("templates/output.md", spec.slug) + f"""# {title} Output

## Summary

{{summary}}

## Evidence

{{evidence}}

## Result

{{result}}

## Validation

{{validation}}

## Risks and Limits

{{risks}}
"""

    files["evals/evals.json"] = evals_json(spec)

    files["examples/example-input.md"] = generated_header("examples/example-input.md", spec.slug) + f"""# Example Input

Use `{spec.slug}` to produce a concise deliverable for a realistic project request.
"""

    files["examples/example-output.md"] = generated_header("examples/example-output.md", spec.slug) + f"""# Example Output

## Summary

Example output for `{spec.slug}`.

## Validation

- Skill activated intentionally.
- Output follows the requested format.
- Risks and assumptions are explicit.
"""

    if include_script_contract:
        files.update(script_contract_files(spec))

    return files


def write_scaffold(
    root: Path,
    spec: SkillSpec,
    dry_run: bool,
    force: bool,
    include_skill_md: bool,
    include_script_contract: bool,
) -> tuple[int, int]:
    base = skill_root(root, spec)
    files = render_files(
        spec,
        include_skill_md=include_skill_md,
        include_script_contract=include_script_contract,
    )
    planned = 0
    written = 0
    for rel, content in files.items():
        path = base / rel
        exists = path.exists()
        if exists and not force:
            continue
        planned += 1
        action = "overwrite" if exists else "create"
        print(f"{action}: {path.relative_to(root)}")
        if dry_run:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written += 1
    return planned, written


def complete_existing(root: Path, args: argparse.Namespace) -> int:
    skills_dir = root / "skills"
    if not skills_dir.exists():
        print("ERROR: skills/ directory not found", file=sys.stderr)
        return 1
    dry_run = not args.apply
    total_planned = 0
    total_written = 0
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            continue
        spec = spec_from_existing(skill_dir, args)
        planned, written = write_scaffold(
            root,
            spec,
            dry_run=dry_run,
            force=False,
            include_skill_md=False,
            include_script_contract=args.with_script_contract,
        )
        total_planned += planned
        total_written += written
    mode = "dry-run" if dry_run else "applied"
    print(f"{mode}: planned={total_planned} written={total_written}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold JM-ADK skills safely")
    parser.add_argument("--name", help="Skill name or slug")
    parser.add_argument("--description", default="Skill scaffold generated by JM-ADK.")
    parser.add_argument("--triggers", default="")
    parser.add_argument("--allowed-tools", default=",".join(DEFAULT_ALLOWED_TOOLS))
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--output-format", default="Markdown with summary, evidence, result, validation, and risks.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned writes without creating files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--local", action="store_true", help="Create under .local/skills instead of skills")
    parser.add_argument("--all-existing", action="store_true", help="Complete all existing skills missing-only")
    parser.add_argument("--apply", action="store_true", help="Apply --all-existing writes; otherwise bulk mode is dry-run")
    parser.add_argument("--with-script-contract", action="store_true", help="Add scripts/README.md, scripts/check.sh, and JSON fixtures")
    args = parser.parse_args()

    root = repo_root()
    if args.all_existing:
        return complete_existing(root, args)
    if not args.name:
        parser.error("--name is required unless --all-existing is used")
    try:
        spec = spec_from_args(args)
    except ValueError as exc:
        parser.error(str(exc))
    base = skill_root(root, spec)
    if base.exists() and not args.force:
        print(
            f"ERROR: skill already exists: {base.relative_to(root)}. "
            "Choose a new name, use --force after review, or use --all-existing to complete existing skills.",
            file=sys.stderr,
        )
        return 1
    planned, written = write_scaffold(
        root,
        spec,
        dry_run=args.dry_run,
        force=args.force,
        include_skill_md=True,
        include_script_contract=args.with_script_contract,
    )
    mode = "dry-run" if args.dry_run else "applied"
    print(f"{mode}: planned={planned} written={written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
