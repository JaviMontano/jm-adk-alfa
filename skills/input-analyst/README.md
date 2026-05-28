<!--
generated-by: scripts/scaffold-skill.py
generated-for: input-analyst
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Input Analyst

Pre-processing layer that analyzes raw user input — detecting surface errors, performing root-cause analysis (5 Whys), impact tracing (7 So-Whats), and intent gap analysis — then reformulates into a precise, actionable prompt.

## Triggers

- input-analyst

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `input-analyst` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
