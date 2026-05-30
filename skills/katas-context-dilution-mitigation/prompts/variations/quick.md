<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation Quick Variation

Úsala cuando el prompt es pequeño y solo necesitas el patrón aplicado.

- Mueve las reglas críticas al inicio como `<rules>...</rules>` y repítelas al final como `REMINDER:<rules>...</rules>`.
- Deja los datos ricos en el centro.
- Añade el gate: `if usage_fraction(history) > 0.55: compact(...)`.

Devuelve solo el prompt corregido, el estado de validación y los riesgos residuales.
