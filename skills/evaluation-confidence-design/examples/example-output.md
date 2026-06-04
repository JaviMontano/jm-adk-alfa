# Example Output

## Summary

Reemplazamos el corte sobre `confidence` cruda por un corte sobre confidence **calibrada** contra los 600 hallazgos etiquetados, estratificamos por `document_type` y medimos FP rate por categoría. `data_privacy` sobre NDA queda en disable temporal hasta rediseñar su criterio.

## Evidence

- Labeled set: 600 hallazgos; estratos `contract=410`, `NDA=120`, `DPA=70`; balance +/- ~ 0.45/0.55.
- Calibración (binning): `raw 0.70` mapea a precisión observada `0.61`; `raw 0.85` -> `0.82`. La cruda sobreestima.

## Result (GOOD)

```python
calibration_map = [(0.60, 0.40), (0.75, 0.61), (0.90, 0.82), (1.01, 0.93)]
threshold = 0.80           # sobre confidence CALIBRADA
disabled_categories = {"data_privacy"}  # FP rate 0.34 en NDA

accepted, fp_rate = evaluate(findings, calibration_map, threshold, disabled_categories)
# fp_rate -> {"indemnity": 0.06, "termination": 0.09, "payment_terms": 0.07}
```

| Categoría | Accuracy | FP rate | Estado |
|---|---|---|---|
| indemnity | 0.94 | 0.06 | activa |
| termination | 0.91 | 0.09 | activa |
| payment_terms | 0.93 | 0.07 | activa |
| data_privacy | 0.66 | 0.34 | disabled (NDA) |

## Anti-pattern (ANTI, lo que se reemplazó)

```python
accepted = [f for f in findings if f["raw_confidence"] >= 0.7]  # cruda
accuracy = 0.88  # agregada: oculta que data_privacy en NDA tiene FP 0.34
```

## Validation

- [x] Umbral sobre confidence calibrada (no cruda).
- [x] Muestreo estratificado por `document_type` con mínimo por estrato.
- [x] Criterios categóricos con ejemplos +/- por severidad.
- [x] FP rate reportada por categoría.
- [x] `scripts/qa/run-confidence-fp-tests.py` en verde.

## Risks and Limits

- El calibration map se ajustó al modelo actual; recalibrar al cambiar de modelo.
- `DPA` tiene solo 70 ejemplos: estrato frágil, ampliar el labeled set.
- `data_privacy` queda desactivada: documentar el plan de rediseño de su criterio.
