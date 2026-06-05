<!--
generated-by: scripts/scaffold-skill.py
generated-for: cierre-conversacion
generated-on: 2026-06-05
overwrite-policy: missing-only unless --force
-->

# Cierre Conversacion

Cosecha aprendizajes y cierra la conversacion al superar 15 turnos o por comando explicito.

## Triggers

- cierre-conversacion
- session-audit
- cosechar-aprendizajes

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `cierre-conversacion` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
