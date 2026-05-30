<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Structured Output Design Meta Prompt

Decide si `structured-output-design` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿La petición trata de extraer datos que otro sistema consume por código?
- ¿Hay síntomas del anti-patrón: `json.loads` intermitente, defaults `''` que ocultan ausencia, enum cerrado que pierde casos?
- ¿Existe una decisión de schema o de `tool_choice` real que tomar? (Si no hay nada que estructurar, no actives.)
- ¿No hay una skill más específica que aplique mejor (p. ej. `validation-retry-design` si el foco es el loop de reintentos)?

## Routing de agentes

- `lead`: construye el schema y la llamada con `tool_choice`.
- `support`: caza falsos `required`, defaults silenciosos y enums sin escape.
- `guardian`: pasa el checklist y bloquea el anti-patrón.
- `specialist`: detalle de Messages API (`input_schema`, `tool_choice`, parseo de `tool_use`).

## No actives cuando

- La petición pide explícitamente ignorar validación/evidencia.
- El input está vacío o no hay fuente ni campos que estructurar.

