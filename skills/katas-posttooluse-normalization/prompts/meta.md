<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Posttooluse Normalization Meta Prompt

Decide si `katas-posttooluse-normalization` debe activarse y qué agentes participan.

## Activation Check

- ¿Hay una o más tools que devuelven payloads heterogéneos o legacy (XML, códigos opacos) que conviene canonizar a JSON?
- ¿El usuario menciona `PostToolUse`, `updatedMCPToolOutput`, normalización de output o payloads legacy?
- ¿Se busca una garantía central por runtime, no una limpieza voluntaria por-tool?
- NO activar si el problema es extracción defensiva de un `tool_result` ya estructurado (esa es otra kata) ni si el input está vacío.

## Agentes

- lead: implementa el hook y `STATUS_MAP`.
- support: caza tools fuera del matcher y códigos sin mapear.
- guardian: valida el argumento de runtime y rechaza el anti-patrón por-tool.
- specialist: detalle del shape del hook en el SDK.
