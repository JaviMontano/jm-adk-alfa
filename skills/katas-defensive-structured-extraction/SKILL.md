---
name: katas-defensive-structured-extraction
version: 1.0.0
description: "Extraccion defensiva con JSON Schema, tool_choice forzado, enums con valvula de escape y nullable explicito; nunca prosa."
owner: "JM Labs"
triggers:
  - defensive extraction
  - json schema extraction
  - forced tool_choice
  - nullable union
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Defensive Structured Extraction

## Qué es

Kata 05 del kit JM-ADK. Enseña a extraer datos estructurados de forma defensiva: se fuerza `tool_choice` con un JSON Schema que declara los `required` reales, modela los campos opcionales como union nullable, y define enums con una válvula de escape (`'other'`, `'unclear'`) acompañada de un campo `details`. El modelo nunca devuelve prosa: siempre invoca la herramienta de extracción y el schema actúa como contrato.

Escenarios canónicos: Structured Extraction y Customer Support.

## Por qué importa (falla que evita)

Pedir "devuélveme JSON" en prosa garantiza alucinación silenciosa. Sin schema forzado el modelo inventa campos faltantes, llena vacíos con `''`, o fuerza valores fuera del dominio del enum. Como la salida parece JSON válido, el `json.loads(resp.text)` pasa y el dato corrupto entra al pipeline sin que nadie lo note. La extracción defensiva convierte esos fallos silenciosos en estados explícitos (`null`, `'unclear'`, `'other'` + `details`).

## Modelo mental

- `required` = el campo siempre está presente en la fuente. Si puede faltar, no es `required`: modélalo como union nullable.
- Default `''` es alucinación. Si el modelo no sabe el valor, debe ser `null` o `'unclear'`, nunca cadena vacía.
- Enums sin escape obligan a mentir cuando el valor real no encaja en ninguna opción. Añade siempre `'other'`/`'unclear'` más un campo `details`.
- `tool_choice` forzado evita la respuesta "best-effort en prosa": el modelo está obligado a poblar el schema.
- Fechas y opcionales se modelan como `{"type":["string","null"],"format":"date"}`.

## Patrón correcto

```python
EXTRACT_TOOL = {
    "name": "extract_invoice",
    "input_schema": {
        "type": "object",
        "required": ["invoice_id", "currency", "status"],
        "properties": {
            "invoice_id": {"type": "string"},
            "currency": {"type": "string", "enum": ["USD", "EUR", "COP", "other"]},
            "currency_other_details": {"type": ["string", "null"]},
            "status": {"type": "string", "enum": ["paid", "pending", "overdue", "unclear"]},
            "due_date": {"type": ["string", "null"], "format": "date"}
        }
    }
}

resp = client.messages.create(
    model=MODEL,
    tools=[EXTRACT_TOOL],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": source_text}],
)
```

## Anti-patrón

```python
# ✗ ANTI: prompt en prosa pidiendo JSON + parseo ciego
prompt = "Devuelve JSON con invoice_id, currency, status, due_date..."
resp = client.messages.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
data = json.loads(resp.text)  # alucina campos, llena vacíos con '', valores fuera de dominio
```

## Argumento de certificación

La extracción usa `tool_choice` forzado + schema con `required` reales + enums con escape + nullable explícito; nunca prosa.

## Cuándo activar

- Cuando hay que extraer campos estructurados de texto libre (facturas, tickets de soporte, formularios).
- Cuando el pipeline consume el JSON aguas abajo y un campo corrupto rompe silenciosamente.
- NO forzar `tool_choice` cuando el modelo debe decidir entre varias tools, o cuando una respuesta híbrida (texto + extracción) es válida.

## Skills relacionadas

- `katas-structured-errors-mcp`
- `katas-deterministic-guardrails-pretooluse`
- `katas-posttooluse-normalization`
