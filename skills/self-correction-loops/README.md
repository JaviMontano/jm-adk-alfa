<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops

Capacidad de ingenieria para verificacion cruzada **declarado vs calculado**: recomputar cada numero agregado desde sus componentes crudos, comparar contra lo que la fuente afirma con un `epsilon` justificado, y emitir `mismatch=true` con ambos valores cuando difieren. La regla dura: **nunca corregir un numero en silencio**; un mismatch escala a humano, no se sobreescribe.

## Triggers

- self-correction loops
- cross-check verification
- mismatch flag
- numeric validation

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill cuando un pipeline recibe valores numericos agregados (totales, balances, conteos) y existen los componentes para recomputarlos de forma independiente, sobre todo en dominios donde un numero mal propagado es caro (finanzas, facturacion, inventario, reporting).

1. Identifica campos verificables y su formula de recomputo.
2. Fija un `epsilon` por tipo de dato (cero enteros, centavo/`1e-6` moneda).
3. Recomputa, compara, emite estado tipado (`match` / `mismatch`).
4. Ante mismatch: escala con `declared` y `computed` visibles; no reescribas.

## Output Format

Markdown con summary, evidence (declarado vs calculado por campo), result (registros con flag), validation (checklist) y risks.
