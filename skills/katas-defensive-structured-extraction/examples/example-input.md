<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Structured Extraction. Texto fuente de una factura recibida por correo:

```
De: billing@acme.io
Factura INV-2026-0042
Total: 1,250.00 GBP
Vence: (no especificado en el documento)
Estado: pendiente de pago
```

Tarea: extraer `invoice_id`, `currency`, `status` y `due_date` de forma defensiva. Nota: la moneda (GBP) NO está en el enum `["USD","EUR","COP","other"]` y la fecha de vencimiento no aparece en la fuente.
