<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Path Conditional Rules Primary Prompt

## Objective

Diseñar (o auditar) el esquema de reglas de un repo aplicando la Kata 09: separar reglas universales (siempre cargadas) de reglas condicionales por glob de ruta, y producir el `CLAUDE.md` resultante con el ahorro de tokens estimado.

## Required Inputs

- Lista de reglas existentes o deseadas (estilo, lints, testing, terraform, seguridad).
- Tipos de archivo del repo y sus rutas (para definir los globs: `src/**/*.py`, `*.tf`).
- Restricciones de la sesión (qué editan típicamente los agentes).
- Definition of done: clasificación completa + `CLAUDE.md` + estimación de ahorro.

## Process

1. Inventaria las reglas y clasifícalas: universal (seguridad, siempre) vs condicional (heurística de lenguaje, por glob).
2. Para las universales, escribe import directo en el `CLAUDE.md` raíz, sin glob.
3. Para las condicionales, crea bloques `## When editing <glob>: @rules/...`.
4. Verifica precedencia por subpath cuando dos reglas apliquen al mismo archivo.
5. Estima el ahorro comparando `input_tokens` al editar un README contra un `.py`.

## Output

Devuelve el deliverable en este shape: Markdown con summary, evidence, result, validation y risks. El bloque de result contiene la tabla de clasificación y el `CLAUDE.md` final.
