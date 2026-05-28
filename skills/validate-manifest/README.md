<!--
generated-by: scripts/scaffold-skill.py
generated-for: validate-manifest
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Validate Manifest

Validates plugin.json completeness, field correctness, and consistency with actual plugin contents. Triggers: validate manifest, check plugin.json, manifest audit.

## Triggers

- validate-manifest

## Allowed Tools

- Read
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `validate-manifest` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
