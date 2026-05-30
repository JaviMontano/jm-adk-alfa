<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Procesamiento Masivo con Message Batches API

## Resumen ejecutivo

Skill de la Kata 17. Enseña a procesar cargas masivas no interactivas (auditorías, backfills, evaluaciones) con la Message Batches API: aproximadamente 50% de ahorro frente al modo real-time, aislamiento de fallos por request mediante `custom_id` único y recuperación selectiva de fallos parciales por sub-batches. El anti-patrón canónico es el `for` que procesa 10000 items uno por uno en real-time.

## Triggers

- message batches
- batch processing
- custom_id
- offline batch

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill cuando el request implique procesar miles de requests offline, backfills o auditorías masivas tolerantes a latencia donde el costo importa. Aplica el ciclo `create → poll processing_status → results`, asigna un `custom_id` único por request y, ante fallos parciales, reintenta solo las requests `failed`.

## Output Format

Markdown con summary, evidence, result, validation y risks.
