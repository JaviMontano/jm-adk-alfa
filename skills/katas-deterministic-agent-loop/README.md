<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop

Kata 01 · Bucle agéntico determinista. Controla la continuación/parada del bucle mirando SOLO el campo estructurado `stop_reason` (`tool_use` vs `end_turn`), nunca la prosa del modelo. Halt y budget deterministas.

## Resumen ejecutivo

Un bucle que detiene por heurística de texto convierte una frase casual ("task complete") en un halt silencioso o en un bucle infinito. La solución es enrutar por `stop_reason`: `tool_use` despacha la herramienta, `end_turn` finaliza, cualquier otro valor eleva un error explícito. La ejecución se acota con un budget configurable (`max_iterations` → `BudgetExceeded`). Escenarios: Customer Support, Multi-Agent Research.

## Triggers

- deterministic loop
- stop_reason
- agent loop control
- budget exceeded

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando revises o escribas un bucle agéntico y el control de flujo dependa (o pudiera depender) de parsear texto del modelo. Reemplaza la heurística de prosa por enrutamiento tipado sobre `stop_reason` más un budget de iteraciones.

## Output Format

Markdown con resumen, evidencia, resultado, validación y riesgos.
