<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops Primary Prompt

## Objective

Construir un bucle de verificacion cruzada declarado vs calculado para los datos numericos del usuario, emitiendo `mismatch=true` cuando difieran y escalando a humano sin sobreescribir.

## Required Inputs

- Datos con campos numericos agregados (totales, balances, conteos) y sus componentes crudos.
- Reglas de recomputo por campo (suma de lineas, balance = debe - haber, conteo de items).
- Tipo de dato por campo (entero, moneda, float) para fijar el `epsilon`.
- Destino de escalada cuando hay mismatch.

## Process

1. Identifica los campos verificables y su formula de recomputo independiente.
2. Fija el `epsilon` por tipo: cero para enteros; tolerancia justificada (centavo, `1e-6`) para moneda/floats.
3. Recomputa cada agregado desde los componentes crudos (nunca desde el agregado declarado).
4. Compara declarado vs calculado y emite estado tipado: `match`, o `mismatch=true` con `declared`, `computed`, `delta`, `field`.
5. Ante mismatch: NO sobreescribas el campo; enruta a escalada con ambos valores visibles.
6. Anade un test estructural que inyecta un mismatch y verifica que produce el flag.

## Output

Markdown con summary, evidence (tabla declarado vs calculado por campo), result (registros con flag y accion), validation (checklist marcado) y risks. Nunca reportes un total corregido en silencio.
