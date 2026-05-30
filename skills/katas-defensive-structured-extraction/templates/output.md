<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction Output

## Summary

{resumen de qué se extrajo y de qué fuente}

## Schema usado

```json
{schema_input_con_required_nullable_y_enums_con_escape}
```

## Result (tool-use block)

```json
{json_extraido_conforme_al_schema}
```

## Validation

- Campos `required` confirmados presentes en la fuente: {lista}
- Campos `null` / `'unclear'` y razón: {lista}
- tool_choice forzado: {sí/no + justificación}
- Sin defaults `''` ni valores fuera de dominio: {sí/no}

## Risks and Limits

{riesgos residuales, campos ambiguos, supuestos}
