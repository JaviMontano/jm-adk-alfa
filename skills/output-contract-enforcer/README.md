<!--
generated-by: scripts/scaffold-skill.py
generated-for: output-contract-enforcer
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Output Contract Enforcer

Validates that every skill output matches its declared contract (format, completeness, evidence tags). Rejects non-conformant outputs. [EXPLICIT]

## Triggers

- output-contract-enforcer

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `output-contract-enforcer` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
