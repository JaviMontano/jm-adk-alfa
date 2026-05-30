<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Petición del usuario:

> Tengo un pipeline que extrae datos de facturas con Claude. Le paso el texto de la factura y al final del prompt pongo "devuelve un JSON con los campos" y luego hago `json.loads(resp.content[0].text)`. Falla una de cada veinte veces porque el modelo a veces mete prosa o un bloque de código. Además, cuando una factura no tiene fecha de vencimiento, sale `due_date: ""` y eso me ensucia la base de datos. Y el `status` lo tengo como enum cerrado `["paid","pending","overdue"]`, pero aparecen estados raros que se pierden.
>
> Campos: `invoice_id` (siempre está), `total_amount` (siempre está), `due_date` (a veces falta), `status` (categórico). El consumidor es un job que inserta en Postgres.

Aplica `structured-output-design` para rediseñar la extracción como contrato verificable.
