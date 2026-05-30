<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## GOOD (patrón correcto)

`tool_choice` forzado sobre `extract_invoice`; GBP no encaja en el enum → `'other'` + `details`; fecha ausente → `null`.

```json
{
  "invoice_id": "INV-2026-0042",
  "currency": "other",
  "currency_other_details": "GBP",
  "status": "pending",
  "due_date": null
}
```

## ANTI (anti-patrón)

Prompt en prosa "devuelve JSON con invoice_id..." + `json.loads(resp.text)`. El modelo alucina: fuerza `currency: "USD"` (valor fuera de la fuente) y rellena `due_date: ""` (default vacío). El JSON parsea sin error y el dato corrupto entra al pipeline.

```json
{
  "invoice_id": "INV-2026-0042",
  "currency": "USD",
  "due_date": ""
}
```

## Validation

- `required` (`invoice_id`, `currency`, `status`) confirmados presentes en la fuente.
- `currency` fuera de dominio resuelto con válvula de escape `'other'` + `currency_other_details: "GBP"`; no se mintió forzando un enum.
- `due_date` ausente → `null`, no `''`.
- tool_choice forzado: sí (`{"type":"tool","name":"extract_invoice"}`).
