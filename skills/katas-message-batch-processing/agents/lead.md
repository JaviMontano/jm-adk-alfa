<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

---
name: katas-message-batch-processing-lead
role: lead
description: "Owns primary execution and deliverable assembly."
tools: [Read, Grep, Glob, Bash]
---

# Kata 17 · Lead

Ejecuta el patrón correcto de la Message Batches API y ensambla el entregable.

## Responsabilidades

- Construir el batch con una request por item y un `custom_id` único por request.
- Implementar el ciclo `create → poll processing_status → results`, con polling hasta `ended`.
- Persistir cada resultado por `custom_id`, mapeando response a input sin ambigüedad.
- Confirmar que la carga es offline y tolerante a latencia antes de elegir batch.
- Preservar overrides locales y archivos manuales existentes.
