<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching Primary Prompt

## Objective

Reorganizar un prompt de producción para maximizar el reuso del cache KV: estático en el prefijo, dinámico en el sufijo.

## Required Inputs

- El prompt actual (system prompt, contexto del repo, input del usuario).
- Qué partes son estables turno a turno y qué partes cambian (timestamps, `user_id`, estado del turno).
- Lectura de `usage` si existe (`cache_creation_input_tokens`, `cache_read_input_tokens`).

## Process

1. Clasificar cada bloque como estático o dinámico.
2. Mover lo estático al prefijo (system prompt, `CLAUDE.md`, tool definitions, contexto pesado del repo) y marcarlo con `cache_control: {type: "ephemeral"}`.
3. Mover lo dinámico al final, aislado en un tag `<reminder>now: {now}</reminder>`.
4. Verificar que ningún valor volátil precede a un bloque estable (un carácter invalida desde ahí).
5. Estimar el ahorro comparando `cache_read_input_tokens` vs `cache_creation_input_tokens` (~10x).

## Output

Markdown con: resumen, el prompt reordenado (GOOD), evidencia (`usage` tokens citados), validación de que no hay dinámico en el prefijo, y riesgos.
