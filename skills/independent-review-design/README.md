<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Independent Review Design

Capacidad de ingeniería para diseñar la etapa de revisión de un pipeline: reviewer
independiente en sesión limpia, pases per-file y cross-file separados, y reporte sin
quorum N-de-M que suprima señal rara pero legítima.

## Resumen ejecutivo

Cuando el generador y el revisor comparten contexto, el sesgo de confirmación oculta
defectos. Esta skill enseña a construir la etapa de revisión de forma que el revisor no
vea la generación, distinga análisis local (per-file) de análisis global (cross-file), y
no descarte hallazgos por baja frecuencia de detección.

## Triggers

- independent review design
- clean session reviewer
- per-file cross-file
- no quorum

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Úsala al diseñar o auditar la fase de revisión de un pipeline de generación. Verifica tres
cosas: sesión limpia del reviewer, per-file y cross-file separados, y ausencia de quorum
que suprima issues legítimos.

## Output Format

Markdown con summary, evidence, result, validation y risks.
