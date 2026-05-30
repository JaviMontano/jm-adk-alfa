<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 26 · Chequeo de activación — Validación y Retry con Error Feedback

Decide si `katas-validation-retry-feedback` debe activarse, si el scope es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿Hay una extracción tipada (Pydantic / JSON Schema) que falló validación?
- ¿El contexto es CI/CD o Structured Extraction con contrato downstream?
- ¿Se observa un loop de reintentos sin feedback o aceptación silenciosa de salida inválida?
- ¿Hay suficiente input (documento, schema, error) para correr el loop?

## No activar cuando

- La tarea no involucra extracción tipada ni validación de schema (false positive).
- El input está vacío o no describe ningún objetivo.
- El request pide explícitamente ignorar validación y evidencia (conflicto con el canon de la kata).
