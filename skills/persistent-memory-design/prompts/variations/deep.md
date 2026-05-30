<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Persistent Memory Design Deep Variation

Úsala cuando el flujo es multi-sesión, el contexto es grande o el diseño de memoria toca varios archivos y herramientas.

Incluye: notas de discovery (dónde vive hoy el estado y qué se pierde en `/compact`), opciones consideradas (ruta del archivo, granularidad del esquema, estrategia de escritura append vs upsert), enfoque elegido con su justificación, prueba de supervivencia simulando compact/reset, integración con prompt caching y con `session-lifecycle-management`, y los riesgos. Cada hallazgo del scratchpad debe quedar trazado a source y fecha.
