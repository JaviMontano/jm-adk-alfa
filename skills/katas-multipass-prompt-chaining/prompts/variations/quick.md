<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multipass Prompt Chaining Quick Variation

Usar cuando las unidades y los schemas ya están claros y el riesgo es bajo.

- Ejecutar el pase 1 por unidad con el schema dado (incluyendo `status`/`error`).
- Ejecutar el pase 2 de integración solo sobre los resúmenes tipados.
- Devolver el resultado integrado, el conteo de unidades válidas, el estado de validación y los riesgos residuales.

Omitir notas de descubrimiento y opciones consideradas.
