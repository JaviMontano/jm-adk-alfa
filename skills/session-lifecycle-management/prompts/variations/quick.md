<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management Quick Variation

Úsala cuando el contexto es pequeño y el estado del mundo claro.

1. ¿Cambió algún tool result crítico contra su fuente (mtime/hash/HEAD)? Si sí → `fresh`.
2. ¿El objetivo es ramificable sin estado compartido? Si sí → `fork` aislado.
3. Si no → `resume`.

Devuelve solo: transición elegida, razón en una línea, y `TypedSummary` si fue `fresh`.
