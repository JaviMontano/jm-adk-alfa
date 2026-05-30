<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design Quick Variation

Usar cuando el formato y las reglas de validacion ya estan claras y el riesgo es bajo.

Entrega solo:

1. Validador minimo que devuelve `{ok, error, recoverable}`.
2. Loop con `max_retries=2` que reinyecta el error previo (no el prompt original).
3. Una linea de escalada al agotar el tope.
4. Checklist marcado.

No reintentes a ciegas ni aceptes salida fallida en silencio.
