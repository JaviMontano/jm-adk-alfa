<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching

Prefix caching: estatico-first y dinamico-last; interpretar cache_creation vs cache_read input tokens para estimar ahorro.

## Triggers

- prefix caching
- kv cache
- cache control
- static prefix

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

La API de Claude reusa el cache KV cuando el prefijo del prompt es idéntico turno a turno. Si pones lo estático (system prompt, `CLAUDE.md`, tool definitions, contexto del repo) primero y lo dinámico (input del usuario, timestamps, `user_id`) al final, el primer ~90% del prompt entra en cache y se factura ~10% del costo. La trampa: un valor dinámico al inicio invalida el cache en cada llamada, encareciendo 10x el mismo contenido sin error visible. La métrica de verdad es `cache_creation_input_tokens` vs `cache_read_input_tokens` en `usage`.

## Quick Use

Activa cuando el request toque organización del prompt para reuso de cache, `cache_control` ephemeral, prefijo estático vs sufijo dinámico, o lectura de los tokens de cache en `usage`. Aplica el patrón: estático arriba con `cache_control: {type: "ephemeral"}`, dinámico al final aislado en `<reminder>`.

## Output Format

Markdown con resumen, evidencia (`usage` tokens citados), resultado, validación y riesgos.
