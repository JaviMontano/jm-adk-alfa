# Katas Posttooluse Normalization

Kata para normalizar outputs heterogéneos con un hook `PostToolUse`. El runtime reemplaza XML, códigos opacos u otros payloads legacy mediante `updatedMCPToolOutput` antes de que el output entre al historial del modelo.

## Triggers

- posttooluse normalization
- output normalization
- updatedmcptooloutput
- legacy payload

## Use When

- Una tool devuelve XML, códigos legacy o payloads heterogéneos.
- El modelo no debe ver el payload crudo.
- La normalización debe ser garantía del runtime, no convención por tool.
- Se requiere `additionalContext` para metadatos auditables separados del JSON limpio.

## Output Contract

El entregable debe incluir:

- `STATUS_MAP` o reglas de traducción recargables.
- Hook `PostToolUse` registrado con matcher de cobertura.
- `updatedMCPToolOutput` con JSON canónico.
- `additionalContext` sin payload crudo.
- Fallback explícito `unknown` para códigos no mapeados.

## Offline Validation

```bash
bash skills/katas-posttooluse-normalization/scripts/check.sh
python3 -B skills/katas-posttooluse-normalization/scripts/validate_posttooluse_normalization.py skills/katas-posttooluse-normalization/scripts/fixtures/valid-legacy-erp.json
```
