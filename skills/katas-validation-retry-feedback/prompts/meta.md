# Kata 26 · Chequeo de activación — Validación y Retry con Error Feedback

Decide si `katas-validation-retry-feedback` debe activarse, si el scope es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿Hay una extracción tipada (Pydantic / JSON Schema) que falló validación?
- ¿El contexto es CI/CD o Structured Extraction con contrato downstream?
- ¿Se observa un loop de reintentos sin feedback o aceptación silenciosa de salida inválida?
- ¿Hay suficiente input (documento, schema, error) para correr el loop?
- ¿El pedido contiene un `ValidationError`, error JSON Schema, salida tipada fallida o decisión de retry/escalada?

## No activar cuando

- La tarea no involucra extracción tipada ni validación de schema (false positive).
- El input está vacío o no describe ningún objetivo.
- Falta la fuente original y no puede evaluarse si un dato ausente es no recuperable.
- El request pide explícitamente ignorar validación y evidencia (conflicto con el canon de la kata).

## Guardian Gate

Bloquea si el plan reintenta errores no recuperables, usa feedback genérico, supera 3 intentos totales, acepta una salida inválida o no conserva evidencia del error y del output previo.
