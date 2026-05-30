<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Tengo un paso de agente que extrae datos de una factura y debe devolver este JSON:

```json
{ "invoice_id": "string", "total": "number", "currency": "string" }
```

A veces el modelo devuelve JSON malformado o `total` como string con simbolo de moneda. Otras veces la factura simplemente no trae `currency` y no hay forma de inferirla. Hoy mi codigo reintenta 3 veces con el mismo prompt y, si sigue fallando, devuelve la ultima salida igual.

Disena el loop `extract -> validate -> retry-with-error-feedback` correcto: que reintente con el error especifico, distinga formato (recuperable) de dato ausente (no recuperable), tope de reintentos y escalada.
