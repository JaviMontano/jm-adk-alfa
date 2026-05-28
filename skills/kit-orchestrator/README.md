<!--
generated-by: scripts/scaffold-skill.py
generated-for: kit-orchestrator
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Kit Orchestrator

Entry point and mode router. Detects whether the user needs analysis (MAO DNA) or development (SA DNA) and routes to the appropriate agent cluster. [EXPLICIT]

## Triggers

- kit-orchestrator

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `kit-orchestrator` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
