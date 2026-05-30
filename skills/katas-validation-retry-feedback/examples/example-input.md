<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input — Kata 26

Un pipeline de Structured Extraction procesa contratos PDF y extrae campos tipados con este schema:

```python
class ContractFields(BaseModel):
    party_name: str
    effective_date: date
    total_amount: Decimal
```

Una extracción sobre `contract-042.pdf` falló validación:

```
Output previo: {"party_name": "Acme Corp", "effective_date": "01-15-2026", "total_amount": "no disponible"}
ValidationError:
  - effective_date: invalid date format, expected ISO 8601 (YYYY-MM-DD)
  - total_amount: value is not a valid Decimal ('no disponible')
```

Notas del analista: el contrato menciona la fecha "January 15, 2026" pero NO contiene un monto total en ninguna cláusula. `max_retries=2`.

Pregunta: ¿cómo se debe reintentar y qué se escala?
