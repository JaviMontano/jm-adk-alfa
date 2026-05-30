<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-fewshot-edge-calibration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Fewshot Edge Calibration

> Kata 14 · "Few-Shot para Calibrar Bordes" · slug `katas-fewshot-edge-calibration`.

## Resumen ejecutivo

En tareas subjetivas (tono, formato no estándar, juicio estético) o de clasificación con criterio, un párrafo de instrucciones zero-shot deja al modelo en su default genérico. Entre 2 y 4 ejemplos `input/output` del mismo schema desplazan su distribución hacia el formato deseado, más rápido y barato que la prosa. Los buenos ejemplos cubren los **bordes** del dominio (los casos difíciles), no el centro. Few-shot complementa al schema (Kata 5): el schema impone forma, los ejemplos calibran juicio. Si ambos chocan, gana el schema.

## Triggers

- few-shot calibration
- edge examples
- fewshot prompting
- subjective calibration

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Detecta si la tarea es subjetiva o de formato no rígido; si no lo es, no actives.
2. Elige 2 a 4 ejemplos que cubran bordes distintos del dominio, no el caso fácil del centro.
3. Escribe cada ejemplo en el mismo schema que la salida esperada.
4. Coloca el bloque de ejemplos al inicio del prompt (parte estática: maximiza prefix cache, Kata 10).
5. Si hay schema estricto (Kata 5), úsalo como forma dura y alinea los ejemplos con él.
6. No superes ~5 ejemplos: dispersa atención (Kata 11) y rompe caches (Kata 10) sin ganar calidad.

## Output Format

Markdown con resumen, evidencia, resultado, validación y riesgos.
