<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Prompt Chaining Design Output

## Summary

{summary}

## Unidad atómica

{unidad_atomica}

## Schema del pase local

{schema_pase_local}

## Schema de transición

{schema_transicion}

## Pase de integración

{pase_integracion}

## Evidence

{evidence}

## Result

{result}

## Validation

- [ ] El pase de integración nunca ve crudos, solo resúmenes.
- [ ] Cada pase tiene schema de salida explícito.
- [ ] El estado de error está tipado por unidad.
- [ ] El pase local es aislado, idempotente y paralelizable.
- [ ] Existe schema de transición.
- [ ] El chaining se justifica frente a single-pass.

{validation}

## Risks and Limits

{risks}
