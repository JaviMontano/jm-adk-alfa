<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 15 · Prompt primario — Evaluación Crítica y Auto-Corrección

## Objetivo

Ejecutar el cross-check numérico declarado vs calculado sobre el documento del usuario, emitiendo un mismatch flag cuando corresponda y sin corregir en silencio.

## Inputs requeridos

- El documento o fuente con los números a verificar (factura, recibo, estado de cuenta, etc.).
- La definición de qué campos son verificables (totales, sumas, conteos, fechas derivadas).
- El epsilon de tolerancia o el dominio (entero vs moneda) para decidirlo.

## Proceso

1. Identifica los campos numéricos verificables.
2. Extrae `stated` (lo declarado) y recalcula `computed` de forma determinista a partir de las líneas/fuentes.
3. Define el epsilon: cero para enteros, epsilon de redondeo de centavos para moneda; justifícalo.
4. Compara `abs(stated - computed) > epsilon`.
5. Si discrepan: devuelve `mismatch=true` con `stated`, `computed`, `delta`, `needs_human_review=true`. Nunca elijas un valor.
6. Si el documento no declara total: devuelve `computed_total` con `stated_total=null` y `mismatch=false`.
7. Enruta el mismatch a escalada humana y preserva el origen del dato.

## Output

JSON tipado:

```json
{
  "stated_total": 0,
  "computed_total": 0,
  "mismatch": false,
  "delta": 0,
  "needs_human_review": false
}
```
