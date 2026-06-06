# Design Agent

Designs plugin subagents with valid frontmatter, role boundaries, skill assignments, execution flows, operating principles, and maxTurns rationale. It produces a reviewable design spec, not a final agent file.

## Triggers

- `design-agent`
- `design agent`
- `agent design`
- `create agent spec`
- `plan agent`
- `draft agent`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Deterministic Resources

- `assets/frontmatter-policy.json` defines required and forbidden fields.
- `assets/constraint-policy.json` blocks plugin subagent constraint violations.
- `assets/maxturns-policy.json` defines the maxTurns formula.
- `assets/report-contract.json` defines the JSON design spec.
- `scripts/check.sh` validates offline fixtures.

## Quick Use

Use this skill to design an agent spec before generating a deployable agent markdown file. Reject forbidden plugin subagent fields and require explicit flow, skill, and maxTurns evidence.

## Output Format

Markdown or JSON with exact date, frontmatter, role boundary, skill assignments, execution flows, operating principles, maxTurns rationale, validation, and risks. Every claim requires an evidence tag.
