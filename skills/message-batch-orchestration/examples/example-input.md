<!--
generated-by: scripts/scaffold-skill.py
generated-for: message-batch-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Tenemos 8.000 tickets de soporte en un export CSV (cada uno con un `ticket_id` único). Queremos clasificarlos por categoría e intención usando Claude. No hay usuario esperando: es un backfill nocturno. En un primer intento ~3% suele fallar por timeouts transitorios.

Usa `message-batch-orchestration` para construir el orquestador: clasificación masiva offline, correlación por `ticket_id`, y reintento solo de los tickets que fallen (máximo 2 reintentos). Persiste los éxitos en `results.jsonl`.
