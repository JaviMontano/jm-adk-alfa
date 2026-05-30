<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El `total` declarado de INV-2026-0042 (1.250.000 COP) NO coincide con la suma recomputada de lineas (1.200.000 COP). Delta = 50.000 > epsilon. Se emite `mismatch=true` y se escala a finanzas. El total NO se sobreescribe.

## Evidence — Declarado vs Calculado

| Campo | Declarado | Calculado | Delta | Epsilon | Estado |
|---|---|---|---|---|---|
| total | 1250000 | 1200000 | 50000 | 0.005 | mismatch |

## Patron correcto (GOOD)

```python
def verify_total(invoice: dict) -> dict:
    computed = sum(line["amount"] for line in invoice["lines"])  # 1_200_000, independiente
    declared = invoice["total"]                                  # 1_250_000
    epsilon = 0.005
    mismatch = abs(declared - computed) > epsilon
    record = {
        "field": "total",
        "declared": declared,
        "computed": computed,
        "delta": declared - computed,
        "mismatch": mismatch,
    }
    if mismatch:
        record["action"] = "escalate_to_human"   # el total NO se reescribe
    return record
```

Salida:

```json
{
  "field": "total",
  "declared": 1250000,
  "computed": 1200000,
  "delta": 50000,
  "mismatch": true,
  "action": "escalate_to_human"
}
```

## Anti-patron (ANTI)

```python
# Oculta el conflicto: carga 1_200_000 como si la fuente nunca hubiera estado mal.
def verify_total_bad(invoice: dict) -> dict:
    invoice["total"] = sum(line["amount"] for line in invoice["lines"])
    return invoice
```

## Validation

- [x] Campo `total` verificable con recomputo independiente (suma de lineas).
- [x] Epsilon 0.005 justificado (moneda, redondeo a centavo).
- [x] Calculado derivado de las lineas, no del total declarado.
- [x] Mismatch tipado con declarado y calculado visibles.
- [x] Escala a humano; total NO sobreescrito.
- [x] Cubierto por test de mismatch inyectado.

## Risks and Limits

- Si llegan facturas sin `lines`, el `total` es no verificable: marcar como tal en lugar de aprobar.
- Epsilon asume moneda entera; revisar para monedas con subunidades fraccionarias.
