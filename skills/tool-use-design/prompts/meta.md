<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Tool Use Design Meta Prompt

Decide si `tool-use-design` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿La petición trata de diseñar/refactorizar descripciones de tools, routing, o la estrategia de built-in tools?
- ¿Hay síntomas de overloading (el agente elige mal o pide aclaración) o de read-all masivo?
- ¿Input suficiente: lista de tools y descripciones vigentes?
- ¿No hay una skill más específica para el caso (p. ej. `custom-tooling-extension` para commands/skills, `plan-mode-workflow` para exploración read-only)?

## Routing de agentes

- **lead** redacta las descripciones-contrato y el flujo `Grep → Read → Edit`.
- **support** caza fronteras unidireccionales y descripciones genéricas.
- **specialist** aporta el detalle de SDK/Claude Code (contrato de Edit, input_schema).
- **guardian** corre el checklist y bloquea el anti-patrón antes de cerrar.

## No-activación

- La petición es ejecutar una tarea con tools, no diseñarlos.
- Pide explícitamente saltarse validación o frontera (conflicto con el canon).
