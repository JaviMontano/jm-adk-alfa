#!/usr/bin/env python3
"""Safely sync canonical MOAT skills into the JM-ADK skill structure.

Dry-run is the default. Existing files are preserved unless --force is set.
"""

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path

CANONICAL_SRC: Path
AGENTIC_SKILLS: Path
APPLY = False
FORCE = False

# ─── Counters ─────────────────────────────────────────────────────────────────
stats = {
    "total": 0,
    "updated": 0,
    "added": 0,
    "files_written": 0,
}


def slug_to_title(slug: str) -> str:
    """Convert kebab-case slug to Title Case name."""
    return " ".join(word.capitalize() for word in slug.replace("-", " ").split())


def write_file(path: Path, content: str) -> None:
    """Write file, creating parent dirs as needed. Increment counter."""
    if path.exists() and not FORCE:
        return
    print(f"{'overwrite' if path.exists() else 'create'}: {path}")
    if not APPLY:
        return
    os.makedirs(path.parent, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    stats["files_written"] += 1


def copy_file(src: Path, dst: Path) -> None:
    """Copy a file only when missing, unless --force is set."""
    if dst.exists() and not FORCE:
        return
    print(f"{'overwrite' if dst.exists() else 'copy'}: {dst}")
    if not APPLY:
        return
    os.makedirs(dst.parent, exist_ok=True)
    shutil.copy2(src, dst)
    stats["files_written"] += 1


def create_agents(skill_dir: Path, slug: str) -> None:
    """Create agents/ directory with 4 agent files if it doesn't exist."""
    agents_dir = skill_dir / "agents"
    if agents_dir.exists():
        return
    title = slug_to_title(slug)
    if APPLY:
        os.makedirs(agents_dir, exist_ok=True)

    write_file(agents_dir / "lead.md", f"""---
name: {slug}-lead
role: Lead
description: "Primary execution agent for {title}."
tools: [Read, Write, Glob, Grep]
---
# {title} Lead
Produces the primary deliverable for this skill domain.
Follows RCTF pattern: Role → Context → Task → Format.
""")

    write_file(agents_dir / "specialist.md", f"""---
name: {slug}-specialist
role: Specialist
description: "Domain expert for {title}."
tools: [Read, Glob, Grep]
---
# {title} Specialist
Provides deep domain expertise. Reviews outputs for correctness and depth.
""")

    write_file(agents_dir / "guardian.md", f"""---
name: {slug}-guardian
role: Guardian
description: "Quality gatekeeper for {title}."
tools: [Read, Glob, Grep]
---
# {title} Guardian
Validates outputs against MOAT criteria. Ensures evidence tags, Validation Gate, and Usage sections are present.
""")

    write_file(agents_dir / "support.md", f"""---
name: {slug}-support
role: Support
description: "Execution support for {title}."
tools: [Read, Write, Edit, Glob, Grep]
---
# {title} Support
Handles secondary tasks: evidence gathering, reference formatting, eval generation.
""")


def create_knowledge(skill_dir: Path, slug: str) -> None:
    """Create knowledge/ directory with 2 files if it doesn't exist."""
    knowledge_dir = skill_dir / "knowledge"
    if knowledge_dir.exists():
        return
    title = slug_to_title(slug)
    if APPLY:
        os.makedirs(knowledge_dir, exist_ok=True)

    write_file(knowledge_dir / "body-of-knowledge.md", f"""# {title} — Body of Knowledge

## Canon
Key standards, references, and best practices for {title}.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Accuracy | >= 90% | Correct outputs / total |
| Evidence coverage | >= 80% | Claims tagged [EXPLICIT]/[INFERRED]/[OPEN] |
| Constitution compliance | 100% | Principles respected |
| Validation Gate pass | 100% | All checklist items satisfied |

## References
- See `references/` folder in canonical skill for detailed references
- Industry standards and best practices for this domain
""")

    write_file(knowledge_dir / "knowledge-graph.md", f"""# {title} — Knowledge Graph

## Core Concepts
- {slug}: primary capability
- validation-gate: quality control checkpoint
- evidence-tagging: [EXPLICIT]/[INFERRED]/[OPEN] claims

## Dependencies
- Upstream: input-analysis, context-optimization
- Downstream: output-engineering, rendering-engine

## Skill Relationships
Part of the JM Labs canonical skill registry.
""")


def create_prompts(skill_dir: Path, slug: str) -> None:
    """Create prompts/ directory with meta, primary, and variations if it doesn't exist."""
    prompts_dir = skill_dir / "prompts"
    if prompts_dir.exists():
        return
    title = slug_to_title(slug)
    if APPLY:
        os.makedirs(prompts_dir, exist_ok=True)
    variations_dir = prompts_dir / "variations"
    if APPLY:
        os.makedirs(variations_dir, exist_ok=True)

    write_file(prompts_dir / "meta.md", f"""---
name: {slug}-meta
type: meta
version: 2.0.0
description: "Meta-prompt for {title} skill routing."
---

# {title} — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/{slug}`

## Skill Routing
1. Load SKILL.md → read `## When to Activate` section
2. If match → activate lead agent: `{slug}-lead`
3. If orchestrated → defer to orchestrating skill
""")

    write_file(prompts_dir / "primary.md", f"""---
name: {slug}-primary
type: execution
version: 2.0.0
description: "Execute the {title} workflow."
triad:
  lead: "{slug}-lead"
  support: "{slug}-support"
  guardian: "{slug}-guardian"
---

# {title} — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{{{task}}}}` | What to accomplish | Yes | User input |
| `{{{{context}}}}` | Background and constraints | Yes | User or codebase |
| `{{{{constraints}}}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Read SKILL.md `## When to Activate` — confirm this skill applies
2. Read SKILL.md `## Validation Gate` — internalize quality criteria
3. Execute the skill workflow per SKILL.md sections
4. Validate output against Validation Gate before delivering
""")

    write_file(variations_dir / "deep.md", f"""---
name: {slug}-deep
type: variation
variant: deep
---
# {title} — Deep Analysis

Full depth execution. Load all `references/` files from canonical. Run L3 progressive loading.
Apply all Validation Gate criteria strictly.
""")

    write_file(variations_dir / "quick.md", f"""---
name: {slug}-quick
type: variation
variant: quick
---
# {title} — Quick Mode

Streamlined execution. Focus on TL;DR and primary output only.
Apply Validation Gate but skip extended evidence tagging.
""")


def create_templates(skill_dir: Path, slug: str) -> None:
    """Create templates/ directory with docx and html templates if it doesn't exist."""
    templates_dir = skill_dir / "templates"
    if templates_dir.exists():
        return
    title = slug_to_title(slug)
    if APPLY:
        os.makedirs(templates_dir, exist_ok=True)

    write_file(templates_dir / "output.docx.md", f"""# {title} — DOCX Template

## Document Structure
- Title: {title} — [Client/Project Name]
- Author: JM Labs
- Date: {{{{DATE}}}}

## Sections (mirror SKILL.md structure)
See canonical SKILL.md for section blueprints.
Use brand-config.json tokens: Navy #122562 · Gold #FFD700 · Blue #137DC5
""")

    write_file(templates_dir / "output.html", f"""<!-- JM Labs Brand Template: {title} -->
<!-- Uses: brand/jmlabs/brand-config.json + brand/jmlabs/corporate-template.css -->
<!-- Replace: {{{{TITLE}}}}, {{{{SUBTITLE}}}}, {{{{CONTENT}}}}, {{{{DATE}}}} -->
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{{{TITLE}}}} | {title} | JM Labs</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--navy:#122562;--gold:#FFD700;--blue:#137DC5;--bg:#0B1120;--bg-alt:#0F1929;--heading:#F1F5F9;--text-s:#94A3B8}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--heading);margin:0;padding:2rem}}
.c{{max-width:1000px;margin:0 auto}}
h1{{font-family:'Poppins',sans-serif;font-weight:900;font-size:clamp(2rem,5vw,3rem)}}
h1 .gold{{color:var(--gold)}}
h2{{font-family:'Poppins',sans-serif;color:var(--gold);border-bottom:1px solid rgba(255,255,255,.05);padding-bottom:.5rem}}
.card{{background:var(--bg-alt);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:1.5rem;margin:1rem 0}}
table{{width:100%;border-collapse:collapse}}
th{{font-family:'Poppins',sans-serif;color:var(--gold);text-align:left;padding:.75rem;border-bottom:2px solid var(--gold)}}
td{{padding:.75rem;border-bottom:1px solid rgba(255,255,255,.05)}}
footer{{text-align:center;margin-top:3rem;border-top:2px solid var(--gold);padding:1.5rem;font-size:.75rem;color:var(--text-s)}}
</style>
</head>
<body>
<div class="c">
  <h1>JM <span class="gold">Labs</span></h1>
  <h2>{{{{TITLE}}}}</h2>
  <p style="color:var(--text-s)">{{{{SUBTITLE}}}}</p>
  <div class="card">{{{{CONTENT}}}}</div>
  <footer>JM Labs · {title} · {{{{DATE}}}}</footer>
</div>
</body>
</html>
""")


def copy_evals(canonical_skill_dir: Path, skill_dir: Path) -> None:
    """Copy evals/evals.json from canonical to agentic skill dir."""
    src_evals = canonical_skill_dir / "evals" / "evals.json"
    if not src_evals.exists():
        return
    dst_evals_dir = skill_dir / "evals"
    copy_file(src_evals, dst_evals_dir / "evals.json")


def copy_references(canonical_skill_dir: Path, skill_dir: Path) -> None:
    """Copy all files from canonical references/ to agentic references/."""
    src_refs = canonical_skill_dir / "references"
    if not src_refs.exists():
        return
    dst_refs = skill_dir / "references"
    for ref_file in src_refs.iterdir():
        if ref_file.is_file():
            copy_file(ref_file, dst_refs / ref_file.name)


def sync_skill(canonical_dir: Path, slug: str) -> None:
    """Sync a single canonical skill into the agentic skills directory."""
    skill_dir = AGENTIC_SKILLS / slug
    existed = skill_dir.exists()

    if APPLY:
        os.makedirs(skill_dir, exist_ok=True)

    # B. Copy SKILL.md missing-only unless --force is set.
    src_skill_md = canonical_dir / "SKILL.md"
    if src_skill_md.exists():
        copy_file(src_skill_md, skill_dir / "SKILL.md")

    # C. agents/ — only if not present
    create_agents(skill_dir, slug)

    # D. knowledge/ — only if not present
    create_knowledge(skill_dir, slug)

    # E. prompts/ — only if not present
    create_prompts(skill_dir, slug)

    # F. templates/ — only if not present
    create_templates(skill_dir, slug)

    # G. evals/ — always copy/update from canonical
    copy_evals(canonical_dir, skill_dir)

    # H. references/ — always copy/update from canonical
    copy_references(canonical_dir, skill_dir)

    stats["total"] += 1
    if existed:
        stats["updated"] += 1
    else:
        stats["added"] += 1


def repo_root() -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, text=True, stdout=subprocess.PIPE)
    return Path(result.stdout.strip())


def main() -> None:
    global CANONICAL_SRC, AGENTIC_SKILLS, APPLY, FORCE
    parser = argparse.ArgumentParser(description="Safely sync canonical skills")
    parser.add_argument("--canonical-src", required=True, help="Directory containing numbered canonical skill folders")
    parser.add_argument("--skills-dir", default="skills", help="Target skills directory relative to repo root")
    parser.add_argument("--apply", action="store_true", help="Apply writes; default is dry-run")
    parser.add_argument("--force", action="store_true", help="Allow overwriting existing files")
    args = parser.parse_args()
    root = repo_root()
    CANONICAL_SRC = Path(args.canonical_src).expanduser().resolve()
    AGENTIC_SKILLS = (root / args.skills_dir).resolve()
    APPLY = args.apply
    FORCE = args.force

    if not CANONICAL_SRC.exists():
        raise SystemExit(f"canonical source not found: {CANONICAL_SRC}")

    # Build slug mapping from canonical source
    pattern = re.compile(r"^\d{4}-(.+)$")
    canonical_skills = []

    for entry in sorted(CANONICAL_SRC.iterdir()):
        if not entry.is_dir():
            continue
        m = pattern.match(entry.name)
        if not m:
            continue
        slug = m.group(1)
        canonical_skills.append((entry, slug))

    print(f"Found {len(canonical_skills)} canonical skills to sync...")
    print(f"Target: {AGENTIC_SKILLS}")
    print(f"Mode: {'apply' if APPLY else 'dry-run'} | Force: {FORCE}")
    print()

    for i, (canonical_dir, slug) in enumerate(canonical_skills, 1):
        if i % 50 == 0 or i == len(canonical_skills):
            print(f"  [{i:3d}/{len(canonical_skills)}] Processing {slug}...")
        sync_skill(canonical_dir, slug)

    print()
    print("=" * 60)
    print("SYNC COMPLETE")
    print("=" * 60)
    print(f"  Skills processed total : {stats['total']}")
    print(f"  Skills updated         : {stats['updated']}  (existed in agentic)")
    print(f"  Skills added           : {stats['added']}   (new to agentic)")
    print(f"  Files created/written  : {stats['files_written']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
