<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Human Handoff Protocol Deep Variation

Úsala cuando hay que diseñar el contrato del handoff o el hook que lo materializa como end-state.

Incluye: enumeración de las precondiciones de escalada (límite, irreversibilidad, conflicto); el input schema de `escalate_to_human` con los cinco campos; el hook `PostToolUse` que termina la sesión tras la escalada; y la verificación de que el payload es autocontenido (el humano no necesita leer la conversación). Documenta las conexiones con `katas-hook-driven-policy-enforcement` y `katas-numeric-cross-validation`.
