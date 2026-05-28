<!--
generated-by: scripts/scaffold-skill.py
generated-for: discovery-orchestrator
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Discovery Orchestrator

Coordinates full analysis pipeline (phases 0-6). Sequences skills 009-023. Manages G1 gate. Does NOT analyze. [EXPLICIT]

## Triggers

- discovery-orchestrator

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `discovery-orchestrator` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
