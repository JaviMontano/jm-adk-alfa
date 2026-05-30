<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Posttooluse Normalization Primary Prompt

## Objective

Implementar el patrón de la Kata 03: un hook `PostToolUse` que normaliza outputs heterogéneos (XML legacy, códigos de estado arcanos) a JSON canónico vía `updatedMCPToolOutput` antes de que entren al historial del modelo.

## Required Inputs

- Las tools que emiten payloads legacy o heterogéneos.
- El formato crudo de salida (tags XML, códigos como `0xA1`) y el JSON canónico objetivo.
- El mapa de traducción de estados (`STATUS_MAP`) o las reglas para construirlo.
- Definición de hecho: el modelo nunca debe ver el payload crudo.

## Process

1. Identifica todas las tools cuyos outputs hay que normalizar y define un único matcher de `PostToolUse` que las cubra.
2. Centraliza `STATUS_MAP` y los esquemas de traducción en código recargable.
3. Implementa `normalize_legacy(input, tool_use_id, ctx)`: lee `input["tool_response"]`, construye el dict limpio y devuelve `{"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedMCPToolOutput": {...json...}, "additionalContext": ...}}`.
4. Usa `additionalContext` para metadatos auditables (origen legacy) que el modelo no necesita ver.
5. Verifica que el XML crudo nunca entra al historial.

## Output

Devuelve: el código del hook, el `STATUS_MAP`, una nota de evidencia que cite el shape de `updatedMCPToolOutput`, el estado de validación y los riesgos residuales (códigos sin mapear, tools fuera del matcher).
