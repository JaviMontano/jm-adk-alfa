---
name: structured-output-design
version: 1.0.0
description: "Disenar extraccion estructurada con JSON Schema defensivo: required reales, nullable union, enums con valvula de escape y tool_choice forzado."
owner: "JM Labs"
triggers:
  - structured output design
  - json schema output
  - defensive schema
  - forced tool_choice
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Structured Output Design

## Capacidad

Diseñar la extracción estructurada de un modelo Claude como un contrato de datos verificable, no como prosa que luego se parsea. La capacidad consiste en definir un JSON Schema defensivo y forzar `tool_choice` para que el modelo emita exactamente ese schema: `required` que reflejan campos realmente presentes en la fuente, uniones `nullable` para opcionales (en vez de defaults silenciosos como `''` o `0`), y enums con válvula de escape (`'other'` + `details`) para no perder señal cuando el dato no encaja en el catálogo. El resultado es una salida parseable de forma determinista, auditable y resistente a alucinación de campos.

## Cuándo usarla

- Cuando necesitas que Claude devuelva datos que otro sistema consume por código (pipelines de extracción, ETL, ingest a base de datos).
- Cuando la salida en prosa + `json.loads(text)` se rompe de forma intermitente.
- Cuando un campo opcional ausente se está rellenando con un default falso (`''`, `0`, `"N/A"`) que contamina el dataset aguas abajo.
- Cuando un enum cerrado pierde casos reales que no encajan en las categorías previstas.
- Cuando el modelo a veces decide "conversar" en vez de emitir la estructura y necesitas forzar la herramienta.

## Cómo construir

1. **Inventaria los campos de la fuente.** Distingue lo que está garantizado en cada documento (→ `required`) de lo que aparece a veces (→ opcional). No marques `required` por deseo: marca por presencia real.
2. **Modela opcionales como unión nullable.** Un campo opcional es `["string", "null"]`, nunca `string` con default `''`. Ausente debe ser representable como `null`, no como cadena vacía.
3. **Añade válvula de escape a los enums.** Todo enum cerrado incluye `'other'` y un campo hermano `details` para capturar el valor textual cuando no encaja. Así el catálogo evoluciona con evidencia en vez de perder filas.
4. **Define la tool con el schema como `input_schema`.** El schema vive en la definición de la herramienta, no en el prompt en prosa.
5. **Fuerza `tool_choice` solo cuando no hay decisión de tool que tomar.** Si la única acción válida es emitir la estructura, usa `tool_choice={"type": "tool", "name": "..."}`. Si el modelo debe elegir entre varias herramientas, no lo fuerces.
6. **Parsea desde `tool_use.input`, nunca desde el texto.** El consumidor lee el bloque `tool_use` tipado, no aplica regex ni `json.loads` sobre prosa.
7. **Valida el bloque emitido contra el schema** antes de aceptarlo, y enruta los fallos al loop de retry/escalada.

## Patrón correcto

```python
# GOOD: defensive schema, forced tool_choice, parse from tool_use.input
extract_invoice = {
    "name": "extract_invoice",
    "description": "Emit invoice fields exactly as they appear in the source document.",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_id": {"type": "string"},          # required: always present
            "total_amount": {"type": "number"},         # required: always present
            "due_date": {"type": ["string", "null"]},   # optional -> nullable, not ""
            "status": {
                "type": "string",
                "enum": ["paid", "pending", "overdue", "other"],  # escape valve
            },
            "status_details": {"type": ["string", "null"]},       # captures 'other'
        },
        "required": ["invoice_id", "total_amount", "status"],
    },
}

resp = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    tools=[extract_invoice],
    tool_choice={"type": "tool", "name": "extract_invoice"},  # forced
    messages=[{"role": "user", "content": document_text}],
)

block = next(b for b in resp.content if b.type == "tool_use")
data = block.input  # typed dict, no json.loads on prose
```

## Anti-patrón

```python
# ANTI: "return JSON" in prose + json.loads(text); empty-string defaults; closed enum
resp = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": document_text + "\n\nReturn the invoice as JSON.",
    }],
)
text = resp.content[0].text
data = json.loads(text)          # breaks when the model adds prose or a code fence
due = data.get("due_date", "")   # "" hides a genuinely-absent value
status = data["status"]          # closed enum drops every unforeseen real case
```

## Checklist de validación

- ¿Cada campo `required` corresponde a algo realmente presente en la fuente (no a un deseo)?
- ¿Los opcionales son uniones `nullable` y se eliminó todo default `''`/`0`/`"N/A"`? Ausente = `null`/`unclear`, no cadena vacía.
- ¿Todo enum cerrado tiene válvula de escape (`'other'` + `details`)?
- ¿`tool_choice` se fuerza solo cuando no hay una decisión de tool legítima que tomar?
- ¿El consumidor parsea desde `tool_use.input` y nunca desde texto en prosa?
- ¿La salida se valida contra el schema antes de aceptarse, con ruta a retry/escalada en caso de fallo?
- ¿El diseño cumple `assets/structured-output-design-contract.json` y pasa `scripts/check.sh` con fixtures determinísticas?

## Assets y validación offline

- `assets/structured-output-design-contract.json` define el paquete JSON que documenta una tool estructurada.
- `assets/json-schema-policy.json` exige `type=object`, `additionalProperties=false`, `required` reales y propiedades declaradas.
- `assets/nullable-policy.json` prohíbe defaults falsos y requiere unión con `null`.
- `assets/enum-escape-policy.json` exige `other` + campo `*_details` para todo enum cerrado.
- `assets/tool-choice-policy.json` fija `tool_choice={"type":"tool","name":...}` cuando la única acción válida es emitir la estructura.
- `assets/refusal-error-policy.json` exige canal de error/refusal y parseo desde `tool_use.input`.
- `scripts/validate_structured_output_design.py` valida el paquete offline y `scripts/check.sh` ejecuta fixtures positivas y negativas.

## Katas y skills relacionadas

- Kata: `05`.
- Skills relacionadas: `katas-defensive-structured-extraction`, `katas-headless-code-review`.
- Capacidades vecinas: `validation-retry-design`, `self-correction-loops`, `provenance-engineering`.
