<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Un solo hook `PostToolUse` con matcher sobre las tools del ERP normaliza el XML a JSON canónico. El modelo recibe `{order_id, status, amount}`; el XML crudo nunca entra al historial. La garantía es del runtime, así que `get_invoice`, `get_shipment` y cualquier tool legacy futura quedan cubiertas sin tocar sus handlers.

## STATUS_MAP

```python
STATUS_MAP = {"0xA1": "paid", "0xB2": "pending", "0xC3": "overdue"}
```

## Patrón correcto (GOOD)

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
            "updatedMCPToolOutput": {"type": "text", "text": json.dumps(clean)},
            "additionalContext": "source=legacy_erp_xml; normalized=true",
        }
    }
# Registrado con un matcher sobre get_order|get_invoice|get_shipment.
```

## Anti-patrón (ANTI)

```python
@tool
def get_order(id):
    return normalize(legacy_erp.fetch(id))   # OK por casualidad

@tool
def get_shipment(id):
    return legacy_erp.fetch(id)              # el dev olvidó normalizar -> XML crudo al contexto
```

## Validation

- El XML crudo nunca entra al historial: el modelo solo ve el JSON de `updatedMCPToolOutput`.
- El matcher cubre las tres tools legacy y futuras, no una por una.
- `0xD4` u otro código no mapeado cae en `"unknown"` (fallback explícito).
- `additionalContext` lleva solo metadatos de auditoría.

## Argumento

La normalización de outputs heterogéneos es responsabilidad del runtime vía `PostToolUse`, no convención de cada tool. Quiz: C·B·B.
