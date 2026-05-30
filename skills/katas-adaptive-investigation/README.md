<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-adaptive-investigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Adaptive Investigation

Investigacion adaptativa: mapeo barato, budget de exploracion acotado y re-plan disciplinado solo al invalidar la hipotesis.

## Triggers

- adaptive investigation
- dynamic decomposition
- exploration budget
- re-plan discipline

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Kata 19 · Investigacion Adaptativa (Descomposicion Dinamica). En dominio desconocido no se planifica al detalle de antemano: se mapea topologia barata primero, se prioriza, se hace deep-dive selectivo y se re-planifica SOLO cuando un hallazgo invalida la hipotesis, todo dentro de un presupuesto de exploracion acotado. Evita la falla de seguir un plan rigido por ramas muertas.

## Quick Use

Activala al investigar un dominio o repositorio desconocido. Flujo: mapeo barato (`glob` de nombres + `regex` de imports) -> plan priorizado -> deep-dive solo sobre lo priorizado -> re-plan SOLO si un hallazgo invalida la hipotesis. Siempre bajo un presupuesto duro (archivos / queries / minutos) y persistiendo plan y findings en un scratchpad.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
