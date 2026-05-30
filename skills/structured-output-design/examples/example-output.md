<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Resumen

Se reemplaza el "devuelve JSON" + `json.loads(text)` por una tool `extract_invoice` con `input_schema` defensivo y `tool_choice` forzado. `due_date` pasa a unión nullable; `status` gana válvula `'other'` + `status_details`. El consumidor parsea desde `tool_use.input`.

## Inventario de campos

| Campo | Presencia | Modelado |
|---|---|---|
| `invoice_id` | garantizado | `string` en `required` |
| `total_amount` | garantizado | `number` en `required` |
| `due_date` | ocasional | `["string","null"]` (ausente = `null`, no `""`) |
| `status` | categórico | enum + `'other'`, con `status_details` nullable |

## Patrón GOOD

```python
extract_invoice = {
    "name": "extract_invoice",
    "description": "Emit invoice fields exactly as they appear in the source document.",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_id": {"type": "string"},
            "total_amount": {"type": "number"},
            "due_date": {"type": ["string", "null"]},
            "status": {
                "type": "string",
                "enum": ["paid", "pending", "overdue", "other"],
            },
            "status_details": {"type": ["string", "null"]},
        },
        "required": ["invoice_id", "total_amount", "status"],
    },
}

resp = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    tools=[extract_invoice],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": invoice_text}],
)

block = next(b for b in resp.content if b.type == "tool_use")
record = block.input  # typed; insert into Postgres directly
```

## Anti-patrón reemplazado

```python
# ANTI: prose JSON + json.loads(text)
resp = client.messages.create(
    model="claude-opus-4-1", max_tokens=1024,
    messages=[{"role": "user", "content": invoice_text + "\n\nReturn a JSON."}],
)
record = json.loads(resp.content[0].text)  # breaks 1/20; due_date "" pollutes DB
```

## Checklist de validación

- [x] `required` = `invoice_id`, `total_amount`, `status` (siempre presentes)
- [x] `due_date` nullable; eliminado el default `""`
- [x] `status` con `'other'` + `status_details`
- [x] `tool_choice` forzado: la única acción válida es emitir la factura
- [x] Consumidor parsea desde `tool_use.input`
- [x] Validar contra el schema antes del insert; fallo -> retry/escalada

## Riesgos y límites

- Si aparecen documentos donde `total_amount` falta, reclasificarlo a nullable (revisar muestra).
- Los valores capturados en `status_details` deben revisarse periódicamente para promover nuevos estados al enum con evidencia.

