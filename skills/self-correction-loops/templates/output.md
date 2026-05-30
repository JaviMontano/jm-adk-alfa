<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops Output

## Summary

{summary}

## Evidence — Declarado vs Calculado

| Campo | Declarado | Calculado | Delta | Epsilon | Estado |
|---|---|---|---|---|---|
| {field} | {declared} | {computed} | {delta} | {epsilon} | {match / mismatch} |

## Result

{result_records}

- Mismatches enrutados a escalada (campo NO sobreescrito): {escalations}

## Validation

- [ ] Campos verificables con recomputo independiente.
- [ ] Epsilon justificado por tipo de dato.
- [ ] Calculado derivado de componentes crudos.
- [ ] Mismatch tipado con declarado y calculado visibles.
- [ ] Mismatch escala a humano; sin sobreescritura.
- [ ] Test estructural de mismatch presente.

## Risks and Limits

{risks}
