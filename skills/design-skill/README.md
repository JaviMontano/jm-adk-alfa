# Design Skill

Designs a reviewable plugin skill specification with valid frontmatter, structured procedure, quality criteria, anti-patterns, edge cases, tool rationale, and MOAT score. It does not write the final deployable skill file without confirmation.

## Triggers

- `design-skill`
- `design skill`
- `skill design`
- `create skill spec`
- `plan skill`
- `draft skill`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Deterministic Resources

- `assets/frontmatter-policy.json` defines frontmatter fields and validation rules.
- `assets/body-policy.json` defines body section minimums.
- `assets/tool-policy.json` defines least-privilege profiles.
- `assets/report-contract.json` defines the JSON design spec.
- `scripts/check.sh` validates offline fixtures.

## Quick Use

Use this skill to produce a skill design spec before generating a deployable `SKILL.md`. Validate procedure steps, tool choices, and MOAT score before presenting the design.

## Output Format

Markdown or JSON with exact date, frontmatter, guiding principle, procedure, quality criteria, anti-patterns, edge cases, tool rationale, MOAT score, validation, and risks. Every claim requires an evidence tag.
