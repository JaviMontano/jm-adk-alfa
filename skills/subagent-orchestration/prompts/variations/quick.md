<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration Quick Variation

Usa cuando el fan-out es pequeño y bien especificado (2-3 spokes homogéneos, mismo tipo de subtarea).

Devuelve solo: la definición de los spokes (`AgentDefinition` con tools/modelo), el esqueleto de agregación con error tipado por spoke, el estado de validación del checklist y los riesgos residuales. Aun en modo rápido, el manejo de error debe distinguir `access_failure` de `valid_empty` y anotar coverage gaps.
