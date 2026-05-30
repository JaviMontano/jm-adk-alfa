<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario: Multi-Agent Research. Tengo un coordinador que debe sintetizar un informe a partir de 30 documentos. Hoy concateno los 30 documentos y el historial del coordinador en un solo agente con `model="opus"` y le pido extraer hechos de cada uno. El costo se dispara, la atención se diluye y me preocupa que un documento envenenado contamine toda la sesión.

Quiero rediseñarlo con aislamiento hub-and-spoke: un subagente extractor que procese UN documento a la vez, con contexto vacío, modelo barato, y que el coordinador agregue solo los hechos extraídos.
