<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Ejemplo de entrada — Structured Extraction (factura)

Escenario: pipeline de extracción de facturas. Llega una factura que declara un total y tiene tres líneas. Hay que verificar que el total declarado coincide con la suma de las líneas antes de aprobar el pago.

Documento:

```text
Factura INV-2026-0048
Línea 1: Consultoría     1.200,00 USD
Línea 2: Licencias         450,00 USD
Línea 3: Soporte           150,00 USD
Total declarado:         1.900,00 USD
```

Pedido: "Extrae el total y dime si la factura es consistente. Es moneda, así que admite el redondeo de centavos."

Nota: la suma de las líneas es 1.800,00 USD, pero el total declarado dice 1.900,00 USD. La diferencia (100,00 USD) excede cualquier epsilon de redondeo de centavos.
