<!--
generated-by: scripts/scaffold-skill.py
generated-for: agentic-loop-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Agentic Loop Engineering Quick Variation

Úsalo cuando el SDK y el mapa de handlers ya están claros y solo hace falta el esqueleto del loop.

Devuelve directamente: el `while True` con enrutado por `stop_reason` (`tool_use` → dispatch + reinyección `tool_result`; `end_turn` → halt; otro → `raise`), el techo `max_iterations` con `BudgetExceeded`, el estado de validación contra el checklist y los riesgos residuales. Sin notas de descubrimiento.
