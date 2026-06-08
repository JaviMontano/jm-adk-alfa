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

## Assets y scripts

- `assets/manifest.json` registra los contratos usados por la skill.
- `assets/self-correction-loops-contract.json` define el reporte JSON auditable.
- `assets/epsilon-policy.json` evita tolerancias arbitrarias.
- `assets/mismatch-policy.json` y `assets/escalation-policy.json` bloquean la correccion silenciosa.
- `scripts/check.sh` ejecuta `scripts/validate_self_correction_loops.py` sobre fixtures deterministicas.

## Output Format

Markdown o JSON con summary, evidence (declarado vs calculado por campo), result (registros con flag), validation (checklist) y risks. Si se requiere evidencia automatizable, emitir el JSON descrito en `assets/self-correction-loops-contract.json`.
