<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation Meta Prompt

Revisa si `katas-context-dilution-mitigation` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿Hay reglas críticas que deben sostenerse a lo largo de una conversación larga? -> activar.
- ¿Se observa que un agente respeta una política temprano y la viola después sin error visible? -> activar.
- ¿Se está diseñando una estrategia de compactación de contexto? -> activar.
- ¿La tarea es un one-shot corto sin riesgo de dilución ni reglas críticas? -> NO activar.
- ¿El input es vacío o ajeno al dominio de prompts/agentes? -> NO activar.

## Señales de no-activación

- Petición sin relación con prompts, atención del modelo o gestión de contexto.
- Requerimientos que piden explícitamente saltarse validación o evidencia.
