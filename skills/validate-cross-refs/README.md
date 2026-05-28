<!--
generated-by: scripts/scaffold-skill.py
generated-for: validate-cross-refs
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Validate Cross Refs

Validates cross-reference integrity across all plugin components. Detects broken references, orphaned skills, missing aliases, and settings.json inconsistencies. Triggers: validate cross-refs, check references, dependency audit, orphan detection.

## Triggers

- validate-cross-refs

## Allowed Tools

- Read
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `validate-cross-refs` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
