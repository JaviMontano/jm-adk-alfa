<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management Primary Prompt

## Objective

Decidir e implementar la transición de ciclo de vida (`resume` / `fork` / `fresh`) para la sesión del agente, con detección de tool results stale y summary tipado.

## Required Inputs

- `SessionContext` previo: tool results con su fuente, decisiones, preguntas abiertas, hechos.
- Invariantes del mundo: HEAD de git, hash del lockfile, esquema de BD, timestamp.
- Objetivo del próximo turno y si es ramificable.

## Process

1. Captura el `SessionContext` y lista las fuentes de cada tool result.
2. Corre la detección de staleness: para cada result compara mtime/hash/HEAD contra su fuente actual.
3. Aplica la matriz de decisión:
   - Contexto válido y objetivo continuo → `resume`.
   - Objetivo ramificable sin estado mutable compartido → `fork` con scratchpad aislado por rama.
   - Algún tool result crítico stale o el mundo cambió → `fresh` con `TypedSummary`.
4. Si `fresh`, construye el `TypedSummary`: `goal`, `decisions[]`, `open_questions[]`, `verified_facts[]` (conservando evidencia), `stale_dropped[]`.
5. Registra la transición elegida con su razón.

## Output

Devuelve el resultado en la forma de `templates/output.md`: decisión, evidencia de staleness, summary tipado (si aplica), validación contra el checklist y riesgos residuales.
