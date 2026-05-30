<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration Deep Variation

Usa cuando el fan-out es grande o heterogéneo, hay dependencias entre spokes, modelos mixtos, o el costo del fallo parcial es alto.

Incluye:

- Notas de descomposición: por qué fan-out vence a un pase único; mapa de dependencias entre spokes.
- Diseño por spoke: prompt, `tools` mínimas, `model` (Haiku extracción / Sonnet razonamiento) y justificación de costo.
- Contrato de error completo (`failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`) y política de local recovery (reintento acotado, query alternativa).
- Estrategia de agregación tolerante a fallo parcial: blast radius acotado, distinción `access_failure` vs `valid_empty`, coverage gaps por rama.
- Validación contra el checklist completo y riesgos residuales (rate limits, dependencias ocultas, contexto que se filtra entre spokes).
