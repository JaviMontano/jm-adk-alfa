<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Few Shot Engineering

Capacidad de ingeniería para calibrar bordes subjetivos de una tarea con 2–4 ejemplos del mismo schema de salida, colocados al inicio del prompt para preservar el prefix cache. El few-shot complementa al schema mostrando cómo se resuelven las zonas grises; no lo reemplaza ni lo contradice.

## Resumen ejecutivo

- **Problema:** el modelo acierta en el caso típico pero falla en los bordes, y el criterio es difícil de verbalizar en prosa.
- **Solución:** exponer pocos ejemplos de borde con el formato exacto de producción, al inicio (zona estática), para fijar juicio y forma sin reentrenar.
- **Resultado:** menor varianza en decisiones grises, prefix cache estable, atención concentrada.

## Triggers

- few-shot engineering
- edge calibration examples
- fewshot design
- subjective calibration

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Recoge casos reales de borde donde el modelo dudó.
2. Escribe 2–4 ejemplos con el schema de salida exacto.
3. Colócalos al inicio del prompt, antes de la entrada variable.
4. Valida contra un set de bordes y revisa el checklist de `SKILL.md`.

## Output Format

Markdown con: resumen, evidencia, el bloque de ejemplos diseñado, validación contra bordes y riesgos residuales.
