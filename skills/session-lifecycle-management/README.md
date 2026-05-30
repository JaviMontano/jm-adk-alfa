<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management

Capacidad de ingeniería para decidir, en un agente de larga duración, entre `resume` (contexto válido), `fork` (ramas paralelas sin interferencia) y `fresh` + summary tipado (el mundo cambió y los tool results quedaron stale). El corazón es la detección de staleness y la síntesis del scratchpad en hechos verificables.

## Resumen ejecutivo

- **Problema:** reusar contexto stale tras un refactor o pegar transcripts crudos degrada al agente con tokens y hechos falsos.
- **Solución:** un detector de staleness + una matriz de decisión resume/fork/fresh + un `TypedSummary`.
- **Salida:** decisión trazable con su razón, summary tipado, forks aislados.

## Triggers

- session lifecycle management
- resume vs fork
- fresh summary session
- stale context

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Captura el `SessionContext` previo con sus tool results y sus fuentes.
2. Corre el detector de staleness contra el estado actual del mundo.
3. Aplica la matriz: válido → `resume`; ramificable → `fork`; stale crítico → `fresh` + `TypedSummary`.
4. Valida con el checklist de `SKILL.md` y registra la razón de la transición.

## Output Format

Markdown con summary tipado, evidencia de staleness, decisión de transición, validación y riesgos.
