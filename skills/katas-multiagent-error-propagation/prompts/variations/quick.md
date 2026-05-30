<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation Quick Variation

Úsala cuando ya existe el código del subagente y solo hace falta corregir la propagación.

Devuelve el bloque corregido aplicando: `empty_valid:True` para 0 matches válidos, `success:False` con `failure_type`/`attempted_query`/`suggested_alternatives` para timeout, y `retryable:False` para permission. Señala en una línea el anti-patrón que se reemplazó (`except Exception: return {"results":[]}`).
