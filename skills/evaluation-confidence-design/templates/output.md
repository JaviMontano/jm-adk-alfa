# Evaluation Confidence Design Output

## Summary

{summary_del_evaluador_y_decision_de_corte}

## Evidence

- Labeled set: {n_ejemplos}, estratos por `document_type`: {estratos}, balance +/-: {balance}.
- Calibration map: {metodo} ajustado sobre el labeled set; raw {raw} -> calibrada {cal}.

## Result

- Umbral de corte (sobre confidence **calibrada**): {umbral}.
- Categorías activas: {activas}. Categorías en disable temporal: {desactivadas}.

| Categoría | Accuracy | FP rate | Estado |
|---|---|---|---|
| {cat} | {acc} | {fp} | {activa/disabled} |

## Validation

- [ ] Umbral sobre confidence calibrada (no cruda).
- [ ] Muestreo estratificado por `document_type` con mínimo por estrato.
- [ ] Criterios categóricos con ejemplos +/- por severidad.
- [ ] FP rate reportada por categoría.
- [ ] `scripts/qa/run-confidence-fp-tests.py` en verde.

## Risks and Limits

{riesgos_residuales_drift_cobertura_supuestos_del_calibration_map}
