# Example Input

Un extractor entrega facturas con el `total` ya declarado y las lineas que lo componen. Quiero verificar cada total antes de cargarlo al ERP: si el declarado no coincide con la suma de las lineas, debe marcarse y escalar a finanzas, no cargarse corregido en silencio.

```json
{
  "invoice_id": "INV-2026-0042",
  "currency": "COP",
  "total": 1250000,
  "lines": [
    { "sku": "A-1", "amount": 500000 },
    { "sku": "B-2", "amount": 450000 },
    { "sku": "C-3", "amount": 250000 }
  ]
}
```

La suma de lineas es 1.200.000 pero el `total` declarado es 1.250.000. Construye el bucle de verificacion cruzada con epsilon de medio centavo, emite el contrato de `assets/self-correction-loops-contract.json` y aplica la regla de no-silencio.
