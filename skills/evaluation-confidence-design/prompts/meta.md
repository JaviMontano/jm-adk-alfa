<!--
generated-by: scripts/scaffold-skill.py
generated-for: evaluation-confidence-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Evaluation Confidence Design Meta Prompt

Decide si `evaluation-confidence-design` debe activarse, valida el alcance y enruta los agentes de apoyo.

## Activation Check

- ¿La tarea menciona confidence/threshold, evaluación de un clasificador, falsos positivos o muestreo? -> activar.
- ¿Hay un labeled set (o intención de construirlo)? Si no, primero pídelo.
- ¿La petición pide algo distinto (entrenar un modelo, anotar datos crudos)? -> NO activar; deriva.
- ¿Existe una skill más específica y segura para el caso? -> deriva.

## Routing

- `lead` construye calibración, estratificación y reporte.
- `support` caza blind spots (estratos ausentes, categorías ocultas).
- `guardian` valida el checklist y bloquea el anti-patrón.
- `specialist` aporta el cableado SDK/Claude Code y el gate de CI.
