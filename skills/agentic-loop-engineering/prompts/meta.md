<!--
generated-by: scripts/scaffold-skill.py
generated-for: agentic-loop-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Agentic Loop Engineering Meta Prompt

Decide si `agentic-loop-engineering` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿El request toca el bucle que llama al modelo, ejecuta herramientas y reinyecta resultados?
- ¿Hay síntomas de control por prosa, bucles infinitos, halts a destiempo o falta de budget?
- ¿Existe información suficiente sobre el SDK y el mapa de handlers?
- ¿No hay una skill más específica que resuelva mejor (p. ej. solo reintentos o solo streaming)?

## Routing de agentes

- lead: implementa el loop y el enrutado por `stop_reason`.
- support: enumera señales no contempladas y fugas de budget.
- guardian: valida el checklist y rechaza el anti-patrón de control por prosa.
- specialist: aporta detalle del SDK Anthropic / Claude Code (forma de `tool_use`/`tool_result`, valores de `stop_reason`).

## Safety

No reemplazar overrides locales. Si falta el origen de `stop_reason`, marcarlo como pregunta abierta antes de construir.
