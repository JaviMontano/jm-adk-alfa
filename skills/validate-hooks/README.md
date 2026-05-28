<!--
generated-by: scripts/scaffold-skill.py
generated-for: validate-hooks
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Validate Hooks

THE CRITICAL SKILL -- validates hooks.json structure, event names, and type-event compatibility. Detects prompt/agent hooks on events lacking ToolUseContext. Triggers: validate hooks, check hooks.json, hooks audit, hook safety check.

## Triggers

- validate-hooks

## Allowed Tools

- Read
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `validate-hooks` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
