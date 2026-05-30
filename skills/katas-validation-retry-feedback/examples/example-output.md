<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output — Kata 26

## Summary

Dos errores con tratamiento distinto: `effective_date` es **recuperable** (formato), `total_amount` es **no recuperable** (el dato no existe en la fuente). Se reintenta solo el campo recuperable con feedback específico; el monto se escala a humano en lugar de inventarse.

## Result (patrón correcto · GOOD)

Intento 2 con feedback específico inyectado:

```python
feedback = (
    "Intento previo falló: effective_date: invalid date format, expected ISO 8601\n"
    "Output previo: effective_date='01-15-2026'\n"
    "Corrige SOLO lo que el error señala (no toques otros campos)."
)
# La fuente dice 'January 15, 2026' -> recuperable
```

Salida final:

```json
{
  "party_name": "Acme Corp",
  "effective_date": "2026-01-15",
  "total_amount": null,
  "attempts": 2,
  "needs_human_review": true,
  "error_chain": "total_amount: dato ausente en la fuente (no recuperable)"
}
```

`effective_date` se corrigió porque el dato existía y el error era de formato. `total_amount` se marcó para revisión humana porque ningún monto aparece en el contrato: reintentar lo habría alucinado.

## Anti-patrón (ANTI)

```python
for _ in range(5):
    ext = extract(doc)        # mismo prompt, sin feedback
    try:
        return validate(ext)  # eventualmente "Decimal('0.00')" inventado
    except Exception:
        continue
```

Cinco reintentos ciegos terminan fabricando un `total_amount` para satisfacer el schema y aceptándolo en silencio: contrato downstream contaminado con un dato alucinado.

## Validation

- El retry inyectó el error de validación específico, no un mensaje genérico.
- El cap de 2 intentos se respetó; tras agotarse se escaló con la cadena de errores.
- El dato ausente en la fuente no se inventó: se marcó `needs_human_review`.
