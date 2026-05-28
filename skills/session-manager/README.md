<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-manager
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Session Manager

Manages session state, pipeline progress, and cold-start priming. Reads/writes .specify/context.json to track feature stages and artifact completion. [EXPLICIT]

## Triggers

- session-manager

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `session-manager` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
