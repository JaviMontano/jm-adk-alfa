# Primary Prompt

## Objective

Diseña una normalización determinística `PostToolUse` que reemplace outputs legacy por JSON canónico antes del historial del modelo.

## Required Inputs

- Tools que emiten payloads legacy.
- Ejemplos de payload crudo.
- JSON canónico objetivo.
- Mapa de estados o reglas de traducción.

## Process

1. Define matcher de cobertura para tools legacy.
2. Centraliza `STATUS_MAP` y esquema canónico.
3. Implementa hook `PostToolUse` con `updatedMCPToolOutput`.
4. Usa `additionalContext` sólo para metadatos.
5. Valida raw payload oculto, fallback y anti-patrón por-tool rechazado.

## Output

Entrega `Summary`, `Status Map`, `PostToolUse Hook`, `Transformation Matrix`, `Validation` y `Risks And Limits`.
