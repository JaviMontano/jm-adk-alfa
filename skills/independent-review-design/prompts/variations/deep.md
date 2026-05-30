<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Independent Review Design Deep Variation

Úsala cuando el pipeline es complejo, multi-módulo o de alto impacto.

Incluye:

- **Discovery:** mapa de qué contexto del generador fluye al reviewer hoy y por qué canal
  (sesión compartida, prompt, trace, memoria).
- **Opciones consideradas:** reviewer como subagente con `Task` fresca vs. proceso/llamada
  separada; per-file y cross-file en una pasada vs. dos pasadas distintas; cómo deduplicar
  sin quorum.
- **Approach seleccionado:** diseño del reviewer independiente con per-file + cross-file
  separados y dedupe que conserva severidad.
- **Bloque de código GOOD** del reviewer y el **ANTI** que reemplaza (self-review + quorum).
- **Validation:** checklist completo recorrido.
- **Risks:** falsos positivos esperados al quitar el quorum y cómo el humano los triará.
