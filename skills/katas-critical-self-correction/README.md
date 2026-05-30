<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 15 · Evaluación Crítica y Auto-Corrección

## Resumen ejecutivo

Cuando un agente extrae o calcula números (totales, sumas, conteos, fechas derivadas), debe cruzar lo que **calcula** contra lo que la fuente **declara**. Si la diferencia supera un epsilon de tolerancia, no decide arbitrariamente ni corrige en silencio: emite un flag `mismatch=true` con ambos valores y el delta, y enruta a revisión humana. Evita el incidente operacional clásico de facturación, contabilidad e impuestos: confiar en la alucinación más plausible.

## Triggers

- critical self-correction
- numeric cross-check
- mismatch flag
- computed vs stated

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Identifica los campos numéricos verificables del documento (totales, sumas, conteos, fechas derivadas).
2. Extrae el valor declarado (`stated`) y recalcula el valor (`computed`) a partir de las líneas/fuentes.
3. Define el epsilon: cero para enteros, epsilon pequeño para monedas (redondeo de centavos).
4. Si `abs(stated - computed) > epsilon`, devuelve `mismatch=true` con `stated`, `computed`, `delta` y `needs_human_review=true`.
5. Escala el conflicto vía `katas-human-handoff-protocol` y preserva el origen vía `katas-provenance-preservation`.

## Output Format

Markdown o JSON tipado con: campos verificados, `stated` vs `computed`, `delta`, `mismatch`, `needs_human_review` y nota de evidencia.

## Skills relacionadas

- `katas-human-handoff-protocol`
- `katas-provenance-preservation`
- `katas-validation-retry-feedback`
