<!--
generated-by: scripts/scaffold-skill.py
generated-for: agentic-loop-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Agentic Loop Engineering Primary Prompt

## Objetivo

Construir (o reparar) el bucle de control de un agente para que enrute por `stop_reason` tipado, con budget duro y handlers explícitos por señal, eliminando todo control basado en prosa.

## Required Inputs

- Lenguaje/SDK y forma de la respuesta del modelo (de dónde leer `stop_reason`).
- Mapa de herramientas y sus handlers.
- Límite de gasto deseado (iteraciones y/o tokens).
- Definición de done: qué cuenta como halt limpio.

## Process

1. Enmarca el loop como `while True` cuyo conmutador es `stop_reason`.
2. `tool_use` → despacha cada bloque a su handler y reinyecta `tool_result` (mensaje `user`, con `tool_use_id`).
3. `end_turn` → detén y devuelve el resultado final.
4. Cualquier otra señal → `raise UnhandledStop(stop_reason)`.
5. Añade contador contra `max_iterations` configurable que dispare `BudgetExceeded`.
6. Instrumenta cada transición y valida contra el checklist de `SKILL.md`.

## Output

Devuelve el loop construido en código (EN), un bloque GOOD frente al ANTI de control por prosa, la validación contra el checklist y los riesgos residuales. Formato: Markdown con summary, evidencia, resultado, validación y riesgos.
