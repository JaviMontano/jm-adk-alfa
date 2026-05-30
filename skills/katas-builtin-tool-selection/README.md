<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Builtin Tool Selection

Kata 23. Selección de built-in tools de Claude Code con estrategia incremental `Grep` → `Read` → `Edit`, conocimiento de failure modes y rechazo del `Read` masivo upfront.

## Resumen ejecutivo

Cada built-in tool tiene un uso primario y un failure mode. `Grep` busca contenido, `Glob` busca paths, `Read` carga un archivo, `Edit` modifica sobre un anchor único, `Write` sobrescribe y `Bash` ejecuta shell. La mecánica básica del examen es escoger el tool correcto rápido y aplicar la estrategia `Grep` (entry points) → `Read` (seguir imports) → `Edit`/`Write` puntual, sin cargar el repositorio entero.

## Triggers

- builtin tool selection
- grep read edit
- tool strategy
- edit anchor

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill cuando haya que explorar o modificar un codebase eligiendo entre los built-in tools, cuando un `Edit` falle por anchor ambiguo, o cuando un plan proponga leer todo el repo upfront. Aplica `Grep` → `Read` selectivo → `Edit` puntual y usa `Read` + `Write` como fallback si el anchor no es único.

## Output Format

Markdown con summary, evidence, result, validation y risks.
