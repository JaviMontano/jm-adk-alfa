<!--
generated-by: scripts/scaffold-skill.py
generated-for: meta-skill-indexer
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Meta Skill Indexer

Regenerates skills_index.json by scanning all SKILL.md files. Extracts frontmatter metadata for BM25 search. [EXPLICIT]

## Triggers

- meta-skill-indexer

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `meta-skill-indexer` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
