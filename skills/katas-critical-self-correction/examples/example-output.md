<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Ejemplo de salida — Structured Extraction (factura)

## Patrón correcto (GOOD)

Se recalcula `computed` de forma determinista y se cruza contra `stated`. Como la diferencia (100,00 USD) excede el epsilon de centavos, se emite el mismatch flag con ambos valores y se escala. No se elige un total.

```python
stated = extract_stated_total(doc)            # 1900.00
computed = sum(line.amount for line in doc.lines)  # 1800.00
epsilon = Decimal("0.01")
if abs(stated - computed) > epsilon:
    result = {
        "stated_total": 1900.00,
        "computed_total": 1800.00,
        "mismatch": True,
        "delta": 100.00,
        "needs_human_review": True,
    }
```

Resultado tipado:

```json
{
  "stated_total": 1900.00,
  "computed_total": 1800.00,
  "mismatch": true,
  "delta": 100.00,
  "needs_human_review": true
}
```

Escalada: el mismatch se enruta vía `katas-human-handoff-protocol`; el origen de cada cifra se conserva vía `katas-provenance-preservation`.

## Anti-patrón (ANTI)

```python
# Confía en el total declarado sin recalcular: aprueba pagar 1900 cuando las líneas suman 1800.
total = extract_total(doc)  # 1900.00 → incidente operacional silencioso

# O corrige en silencio y oculta la discrepancia al humano:
if abs(stated - computed) > epsilon:
    total = computed  # 1800.00, sin avisar a nadie
```

## Validación

- Skill activada intencionalmente: hay un total declarado y líneas recalculables.
- Epsilon justificado: 0,01 USD por redondeo de centavos; la diferencia de 100,00 USD lo excede ampliamente.
- Conflicto preservado: se reportan `stated_total` y `computed_total`, no un valor elegido.
- Caso límite documentado: si la factura no declarara total, se devolvería `computed_total` con `stated_total=null` y `mismatch=false`.
