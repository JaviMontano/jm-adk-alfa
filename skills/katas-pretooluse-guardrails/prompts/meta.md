<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-pretooluse-guardrails
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Pretooluse Guardrails Meta Prompt

Evalúa si `katas-pretooluse-guardrails` debe activarse para esta tarea.

## Activation Check

- ¿Hay una política o límite duro (montos, dominios, paths) que no puede romperse?
- ¿Se necesita bloquear una tool ANTES de que produzca side-effects?
- ¿El control debe ser determinista y no depender del prompt?
- ¿La petición es del dominio del guardarraíl `PreToolUse` y no de otra kata (bucle, normalización, MCP)?

## No activar cuando

- La petición no involucra tools ni políticas (no es del dominio).
- Solo se pide tono o redacción del prompt sin guardarraíl.
- El input está vacío o no define ninguna regla de negocio.
