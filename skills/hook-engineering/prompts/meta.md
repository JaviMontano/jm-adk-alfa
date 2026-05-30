<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Hook Engineering Meta Prompt

Evalua si `hook-engineering` debe activarse, si el alcance es seguro y que agentes de
apoyo deben participar (support para blind spots, guardian para la checklist, specialist
para detalle de SDK).

## Activation Check

- Coincidencia de trigger (`hook engineering`, `pretooluse hook`, `posttooluse hook`, `deterministic hooks`).
- Ajuste de dominio: la tarea requiere enforcement que el runtime garantice, no una sugerencia al modelo.
- Input suficiente: hay una regla/limite concreto y las tools afectadas estan identificadas.
- No existe una skill especializada mas segura para el caso.

## Senales de que SI aplica

- Limite costoso o irreversible (monetario, path, dominio) que no puede quedar al criterio del modelo.
- Outputs heterogeneos que el modelo debe consumir como contrato unico.

## Senales de que NO aplica

- La regla es una preferencia de estilo sin coste real (mejor en el prompt/memoria).
- No hay tools involucradas ni runtime de Agent SDK.
