<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Path Conditional Rules

Kata 09 · Reglas condicionales por ruta. Las reglas heurísticas de lenguaje (estilo, lints, testing) se cargan solo cuando el agente edita archivos que matchean un glob (`src/**/*.py`, `*.tf`); las reglas universales (seguridad) permanecen siempre cargadas. Así un repo no paga 2000 líneas de contexto al editar un simple README.

## Triggers

- path conditional rules
- glob rules
- conditional memory
- per-path rules

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala al diseñar o auditar el esquema de reglas/memoria de un repo: clasifica cada regla como universal (carga directa en `CLAUDE.md` raíz, sin glob) o condicional por glob (`## When editing <glob>: @rules/...`), y estima el ahorro de tokens comparando una sesión que edita un README contra una que edita un `.py`.

## Output Format

Markdown con summary, evidence, result, validation y risks. El bloque de result incluye la clasificación universal vs condicional y el `CLAUDE.md` resultante.
