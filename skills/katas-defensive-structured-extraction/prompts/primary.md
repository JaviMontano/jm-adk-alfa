<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction Primary Prompt

## Objetivo

Extraer campos estructurados de la fuente usando un JSON Schema con `tool_choice` forzado, sin devolver prosa.

## Instrucción de producción

Eres un extractor defensivo. Dada la fuente:

1. Define un tool `extract_invoice` con `input_schema`:
   - `required`: solo los campos que SIEMPRE aparecen en la fuente (`invoice_id`, `currency`, `status`).
   - opcionales como union nullable: `due_date` → `{"type":["string","null"],"format":"date"}`.
   - enums con válvula de escape: `currency` enum `["USD","EUR","COP","other"]` + `currency_other_details` nullable; `status` enum con `"unclear"`.
2. Llama `messages.create(tools=[EXTRACT_TOOL], tool_choice={"type":"tool","name":"extract_invoice"})`.
3. Si un valor se desconoce, usa `null` o `'unclear'`; nunca `''` ni valores fuera del dominio.

## Reglas duras

- Nunca pidas "devuelve JSON" en prosa ni hagas `json.loads(resp.text)`.
- Cada campo entregado debe estar sostenido por la fuente o marcado como nullable/`unclear`.

## Output

Tool-use block conforme al schema, más nota de validación (campos null/unclear y por qué).
