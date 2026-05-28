<!--
generated-by: scripts/scaffold-skill.py
generated-for: iic-task-decomposer
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Iic Task Decomposer

Decomposes plans into tasks with format [T###] [P?] [US#] Description. Marks parallelizable tasks, tracks dependencies, estimates effort. [EXPLICIT]

## Triggers

- iic-task-decomposer

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `iic-task-decomposer` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
