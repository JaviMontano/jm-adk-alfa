<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design Quick Variation

Usar cuando la precondicion de escalada es unica y clara (p. ej. solo `limit_exceeded`) y la tool ya existe.

Devuelve solo: el codigo del handoff con el payload tipado autocontenido, la confirmacion de que la generacion se corta (end-state), el checklist de validacion y los riesgos residuales.
