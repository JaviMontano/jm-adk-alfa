<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop Deep Variation

Úsala cuando el bucle es complejo, multi-herramienta o multi-agente, con consecuencias cross-file o riesgo de bucle infinito en producción.

Incluye:

- Notas de descubrimiento: dónde estaba el control hoy (¿parseo de prosa? ¿sin budget?).
- Opciones consideradas: loop manual con `messages.create` vs. loop nativo del SDK de agentes / Claude Code.
- Enfoque elegido: enrutamiento por `stop_reason` con handlers tipados para `tool_use`, `end_turn`, `max_tokens`, `pause_turn` y `stop_sequence`.
- Diseño del budget (`max_iterations` → `BudgetExceeded`) y reanudación tras `pause_turn` si aplica.
- Validación contra el argumento de certificación y riesgos residuales.
