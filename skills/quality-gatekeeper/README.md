<!--
generated-by: scripts/scaffold-skill.py
generated-for: quality-gatekeeper
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Quality Gatekeeper

Validates deliverables at quality gates G0-G3. Blocks phase transitions until criteria are met. Produces pass/fail reports with evidence. [EXPLICIT]

## Triggers

- quality-gatekeeper

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `quality-gatekeeper` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
