<!--
generated-by: scripts/scaffold-skill.py
generated-for: agentic-loop-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Agentic Loop Engineering

Capacidad de ingeniería para construir el bucle de control de un agente que enruta por `stop_reason` tipado, con budget duro y handlers explícitos por señal, en vez de inferir el control desde la prosa del modelo. El loop deja de ser frágil (basado en `"done" in text`) y pasa a ser una máquina de estados determinista, acotada y auditable.

## Resumen ejecutivo

- Problema: agentes que entran en bucles infinitos, se detienen a destiempo o hacen halts silenciosos porque el control se decide leyendo texto libre.
- Solución: enrutar por señal estructurada (`tool_use` → dispatch + reinyección de `tool_result`; `end_turn` → halt; otro → `raise`) con techo de iteraciones/tokens.
- Resultado: control predecible, fallos fuertes y gasto acotado en producción.

## Triggers

- agentic loop engineering
- agent control loop
- stop_reason routing
- loop budget

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Usa esta skill cuando implementes o repares el bucle que llama al modelo, ejecuta herramientas y reinyecta resultados, o cuando necesites acotar el gasto de un agente autónomo. Sigue `## Cómo construir` de `SKILL.md` y valida con su checklist.

## Output Format

Markdown con summary, evidencia (snippet GOOD vs ANTI), resultado (loop construido), validación contra checklist y riesgos residuales.
