<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Human Handoff Protocol Meta Prompt

Decide si `katas-human-handoff-protocol` debe activarse para este turno.

## Activation Check

- ¿El agente alcanzó un límite de política que no puede resolver (p.ej. reembolso sobre su tier)?
- ¿La acción solicitada es irreversible y requiere aprobación humana?
- ¿Hay un conflicto de datos que el agente no puede arbitrar?
- ¿Se pide diseñar el contrato del payload de escalada o el hook que cierra la sesión?

Si ninguna precondición de escalada aplica (el agente puede resolver dentro de su política), NO actives esta skill. El handoff es para end-states reales, no para incertidumbre genérica.
