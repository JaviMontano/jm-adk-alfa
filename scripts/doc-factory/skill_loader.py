#!/usr/bin/env python3
"""
Skill Loader — Load schema, template, knowledge, and agents for any skill.
==========================================================================
Given a skill name, loads all resources needed for execution.
Works as both a CLI tool and importable module.

Usage:
    python skill_loader.py invoice-generator
    python skill_loader.py acta-formal --format docx
    python skill_loader.py --list  # list all skills with schemas
"""

import argparse
import json
import sys
from pathlib import Path

# Skills root relative to this file
SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent / "skills"


def find_skill(skill_name):
    """Find a skill directory by name."""
    skill_dir = SKILLS_ROOT / skill_name
    if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
        return skill_dir
    return None


def load_schema(skill_dir):
    """Load schema.json if it exists."""
    schema_path = skill_dir / "templates" / "schema.json"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def find_template(skill_dir, fmt="html"):
    """Find the best template for a given format."""
    templates_dir = skill_dir / "templates"
    if not templates_dir.exists():
        return None

    # Priority order for template discovery
    candidates = [
        templates_dir / f"template.{fmt}",
        templates_dir / f"template.{fmt}.html",
        templates_dir / f"output.{fmt}",
    ]

    # Special cases
    if fmt == "html":
        # Also check for skill-specific named templates
        for f in templates_dir.glob("*.html"):
            if f.name not in ("output.html", "README.html"):
                candidates.insert(0, f)

    if fmt == "pdf":
        # PDF uses HTML template
        candidates.extend([
            templates_dir / "template.html",
        ])
        for f in templates_dir.glob("*.html"):
            if f.name not in ("output.html", "README.html"):
                candidates.append(f)

    for c in candidates:
        if c.exists():
            return c

    return None


def load_knowledge(skill_dir):
    """Load all knowledge files for a skill."""
    knowledge_dir = skill_dir / "knowledge"
    if not knowledge_dir.exists():
        return []

    knowledge = []
    for f in sorted(knowledge_dir.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        knowledge.append({
            "name": f.stem,
            "path": str(f),
            "size": f.stat().st_size,
        })

    return knowledge


def load_agents(skill_dir):
    """Load agent definitions for a skill."""
    agents_dir = skill_dir / "agents"
    if not agents_dir.exists():
        return []

    agents = []
    for f in sorted(agents_dir.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        # Read frontmatter
        content = f.read_text(encoding="utf-8")
        name = ""
        role = ""
        for line in content.split("\n"):
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("role:"):
                role = line.split(":", 1)[1].strip()

        agents.append({
            "file": f.name,
            "name": name,
            "role": role,
            "path": str(f),
        })

    return agents


def load_skill(skill_name, fmt=None):
    """
    Load all resources for a skill.

    Returns:
        dict: {name, path, schema, template, templates_available, knowledge, agents, ready}
    """
    skill_dir = find_skill(skill_name)
    if not skill_dir:
        return {"error": f"Skill not found: {skill_name}", "ready": False}

    schema = load_schema(skill_dir)

    # Determine available formats from schema
    available_formats = []
    if schema:
        available_formats = schema.get("outputs", [])

    # Find template for requested format
    template = None
    if fmt:
        template = find_template(skill_dir, fmt)
    elif available_formats:
        # Find first available template
        for f in available_formats:
            t = find_template(skill_dir, f)
            if t:
                template = t
                fmt = f
                break

    knowledge = load_knowledge(skill_dir)
    agents = load_agents(skill_dir)

    # Readiness check
    ready = True
    missing = []
    if not schema:
        ready = False
        missing.append("schema.json")

    result = {
        "name": skill_name,
        "path": str(skill_dir),
        "schema": schema,
        "schema_path": str(skill_dir / "templates" / "schema.json") if schema else None,
        "template_path": str(template) if template else None,
        "templates_available": available_formats,
        "format": fmt,
        "knowledge": knowledge,
        "knowledge_count": len(knowledge),
        "agents": agents,
        "agents_count": len(agents),
        "ready": ready,
        "missing": missing,
    }

    return result


def list_skills_with_schemas():
    """List all skills that have schema.json."""
    skills = []
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir():
            continue
        schema_path = skill_dir / "templates" / "schema.json"
        if schema_path.exists():
            with open(schema_path) as f:
                schema = json.load(f)
            skills.append({
                "name": skill_dir.name,
                "title": schema.get("title", ""),
                "outputs": schema.get("outputs", []),
                "required_fields": len(schema.get("required", [])),
            })
    return skills


def main():
    parser = argparse.ArgumentParser(description="Skill Loader — Load skill resources")
    parser.add_argument("skill", nargs="?", help="Skill name to load")
    parser.add_argument("--format", help="Output format (html, docx, xlsx, etc.)")
    parser.add_argument("--list", action="store_true", help="List skills with schemas")

    args = parser.parse_args()

    if args.list:
        skills = list_skills_with_schemas()
        print(json.dumps(skills, indent=2, ensure_ascii=False))
        return

    if not args.skill:
        print("ERROR: Specify skill name or --list", file=sys.stderr)
        sys.exit(1)

    result = load_skill(args.skill, args.format)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
