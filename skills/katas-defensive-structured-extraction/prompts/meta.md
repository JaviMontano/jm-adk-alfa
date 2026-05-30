<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction Meta Prompt

Decide si `katas-defensive-structured-extraction` debe activarse para extraer datos estructurados de forma defensiva.

## Chequeo de activación

- ¿La tarea pide extraer campos estructurados de texto libre (facturas, tickets, formularios)?
- ¿El JSON resultante se consume aguas abajo, donde un campo corrupto rompe en silencio?
- ¿Hay riesgo de alucinación por pedir "devuélveme JSON" en prosa?

## No activar (límite de la kata)

- El modelo debe decidir entre varias tools → no fuerces `tool_choice`.
- Una respuesta híbrida (texto + extracción) es legítima.
- Input vacío o ajeno al dominio de extracción → no activar.
