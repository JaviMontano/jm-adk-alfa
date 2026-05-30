<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Few Shot Engineering Quick Variation

Usar cuando el schema ya existe y hay 2–3 bordes claros que calibrar.

1. Toma 2–3 casos de borde y escríbelos con el schema de salida exacto.
2. Pégalo al inicio del prompt, antes de la entrada variable.
3. Verifica que ningún ejemplo contradice al otro.

Devuelve solo el bloque de ejemplos, el estado de validación contra bordes y los riesgos residuales.
