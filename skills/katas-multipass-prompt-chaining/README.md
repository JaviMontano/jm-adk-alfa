<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multipass Prompt Chaining

Kata 12 · Prompt Chaining Multi-Pass. Descompone una tarea que no cabe en un solo prompt en pases secuenciales: un pase local tipado por unidad (paralelizable) y un pase de integración que solo ve los resúmenes tipados, nunca las unidades crudas.

## Resumen ejecutivo

Pedir "audita 50 archivos" en un mega-prompt satura la atención del modelo y produce un resumen genérico que alucina. La solución es encadenar: pase 1 procesa cada unidad por separado con salida tipada según schema; pase 2 integra solo esos resúmenes. Cada pase declara su schema y el siguiente lo consume como una pipeline. El estado de error por unidad debe ser tipado para que el pase 2 sepa cuántas unidades válidas tiene.

## Triggers

- prompt chaining
- multipass chaining
- local then integrate
- chaining schema

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando una tarea no quepa cognitivamente en un solo prompt (auditar muchos archivos, resumir un documento largo) y necesites salida tipada y auditable por unidad antes de integrar. NO la actives si la tarea cabe holgadamente y el overhead de coordinación supera el beneficio.

## Output Format

Markdown con summary, evidence, result, validation y risks. El resultado distingue el pase 1 (resúmenes tipados por unidad) del pase 2 (informe integrado).
