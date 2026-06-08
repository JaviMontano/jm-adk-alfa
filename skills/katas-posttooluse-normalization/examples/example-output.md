# Example Output

## Summary

Un hook `PostToolUse` central normaliza outputs del ERP legacy antes de que entren al historial del modelo. `updatedMCPToolOutput` entrega JSON canónico y `additionalContext` conserva metadatos auditables sin XML crudo.

## Status Map

```python
STATUS_MAP = {"0xA1": "paid", "0xB2": "pending", "0xC3": "overdue"}
```

## PostToolUse Hook

```python
async def normalize_legacy(input, tool_use_id, ctx):
    raw = input["tool_response"]
    clean = {
        "order_id": raw.find("OrderId"),
        "status": STATUS_MAP.get(raw.find("StatusCode"), "unknown"),
        "amount": float(raw.find("Total")),
    }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedMCPToolOutput": {
                "type": "text",
                "text": json.dumps(clean),
            },
            "additionalContext": "source=legacy_erp_xml; normalized=true",
        }
    }
```

## Transformation Matrix

| tool | raw status | normalized status | raw visible |
|---|---|---|---|
| `get_order` | `0xA1` | `paid` | no |
| `get_invoice` | `0xB2` | `pending` | no |
| `legacy_erp_get_shipment` | `0xD4` | `unknown` | no |

## Validation

- `updatedMCPToolOutput.text` parsea a JSON con `order_id`, `status` y `amount`.
- El matcher cubre `legacy_erp_*` y las tools ERP nombradas.
- `additionalContext` no contiene XML ni payload crudo.
- El anti-patrón por-tool queda rechazado.

## Risks And Limits

- Cambios de dialecto XML requieren actualizar parser y fixtures.
- Campos nuevos deben agregarse al esquema canónico y a la validación offline.
