<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction Body of Knowledge

## Canon

La extracción estructurada defensiva fuerza `tool_choice` con un JSON Schema. El schema es el contrato: declara `required` reales, modela opcionales como union nullable, y define enums con válvula de escape (`'other'`, `'unclear'`) más un campo `details`. El modelo nunca responde en prosa.

## Conceptos clave

- **`required` real**: un campo solo es `required` si está siempre presente en la fuente. Si puede faltar, es nullable.
- **Union nullable**: opcionales se modelan como `{"type":["string","null"]}`; fechas como `{"type":["string","null"],"format":"date"}`.
- **Enum con válvula de escape**: todo enum incluye `'other'`/`'unclear'` y un campo `details` para capturar lo que no encaja.
- **`tool_choice` forzado**: `{"type":"tool","name":"extract_invoice"}` obliga al modelo a poblar el schema en vez de responder best-effort en prosa.
- **Default `''` = alucinación**: si el valor se desconoce, debe ser `null` o `'unclear'`, nunca cadena vacía.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| `required` mínimos | Solo campos siempre presentes en la fuente |
| Nullable explícito | Todo opcional es union con `null`; sin defaults `''` |
| Enums con escape | Cada enum tiene `'other'`/`'unclear'` + campo `details` |
| tool_choice forzado | La extracción invoca la herramienta, nunca prosa |
| Sin parseo ciego | No se usa `json.loads(resp.text)` sobre prosa |

## Anti-patrón canónico

Prompt en prosa "devuelve JSON con invoice_id, currency, status..." seguido de `json.loads(resp.text)`. Produce alucinación silenciosa: campos inventados, vacíos rellenados con `''` y valores fuera del dominio del enum, todo con apariencia de JSON válido.

## Límite de la kata

NO forzar `tool_choice` cuando el modelo debe decidir entre varias tools, o cuando una respuesta híbrida (texto + extracción) es legítima.
