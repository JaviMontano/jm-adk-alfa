<!--
generated-by: scripts/scaffold-skill.py
generated-for: revisor-veracidad
generated-on: 2026-06-05
overwrite-policy: missing-only unless --force
-->

# Revisor Veracidad

Marca afirmaciones no verificables con tags de veracidad y propone el siguiente paso de verificacion.

## Triggers

- revisor-veracidad
- verificar-fuente
- marcar-supuesto

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `revisor-veracidad` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
