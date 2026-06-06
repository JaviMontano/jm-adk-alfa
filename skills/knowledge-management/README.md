<!--
generated-by: scripts/scaffold-skill.py
generated-for: knowledge-management
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Knowledge Management

Build a deterministic knowledge register for project artifacts: what knowledge
exists, where it lives, who owns it, how it can be found, when it decays, and
what action keeps it usable.

## Triggers

- knowledge-management
- knowledge capture
- knowledge register
- searchability audit
- decay prevention

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when scattered project knowledge must be captured, indexed,
de-duplicated, assigned ownership, or reviewed for stale/uncited claims.

The skill does not infer freshness from the live clock. Reports must include a
fixed `reference_date`, and decay decisions must cite source dates.

## Output Format

Markdown or JSON with:

- Summary and scope
- Knowledge register
- Searchability map
- Decay review
- Gaps and contradictions
- Action log with owners and due dates
- Validation evidence
- Risks and assumptions

JSON reports can be validated offline with:

```bash
bash skills/knowledge-management/scripts/check.sh
```
