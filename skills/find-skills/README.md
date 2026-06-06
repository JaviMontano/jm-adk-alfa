# Find Skills

Finds and recommends agent skills from local catalogs and optional remote sources. It is local-first, evidence-tagged, and installation-safe: the skill may present commands, but it must not install anything without explicit user confirmation.

## Triggers

- `find-skills`
- `find a skill`
- `is there a skill for`
- `search skills`
- `install skill`
- `skill marketplace`
- `skills.sh`
- `extend capabilities`

## Allowed Tools

- Read
- Glob
- Grep
- Bash
- WebFetch
- Task

## Deterministic Resources

- `assets/source-policy.json` defines local, remote, and user-provided sources.
- `assets/scoring-rubric.json` defines stable candidate scoring and tiers.
- `assets/install-policy.json` blocks automatic installation.
- `assets/report-contract.json` defines the offline-validatable report.
- `scripts/check.sh` validates local fixtures without network access.

## Quick Use

Use this skill to parse a capability request, search local catalogs first, optionally summarize remote candidates, score every candidate, and recommend a bounded next action.

## Output Format

Markdown or JSON with exact date, query, scope, intent, candidate table, selected recommendation, install policy, validation, and risks. Every claim requires an evidence tag.
