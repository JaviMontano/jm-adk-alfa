<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop Quick Variation

Úsala cuando el bucle es pequeño y el problema es claro (p. ej. reemplazar una sola heurística de texto por enrutamiento `stop_reason`).

Devuelve solo el bucle corregido (`tool_use`→dispatch, `end_turn`→return, otro→raise, budget) más estado de validación y riesgos residuales. Sin notas de descubrimiento extensas.
