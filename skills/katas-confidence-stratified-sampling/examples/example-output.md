<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-confidence-stratified-sampling
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Los `field_confidence` raw no se usan para routing. Se calibran contra labeled validation set por bucket, se reporta accuracy por `document_type` y field, y el tráfico high-confidence pasa a auto sólo con stratified sampling de control.

## Evidence

- Labeled validation set: 240 ejemplos con `invoice` y `receipt`.
- Buckets calibrados: `0.80-0.89` -> 0.81 accuracy empírica; `0.90-1.00` -> 0.92.
- Receipts quedan en control sample porque vendor tiene accuracy 0.82.

## Result

| document_type | field | accuracy | n | route |
|---|---:|---:|---:|---|
| invoice | total | 0.94 | 120 | auto |
| invoice | vendor | 0.91 | 120 | auto |
| receipt | total | 0.86 | 60 | control_sample |
| receipt | vendor | 0.82 | 60 | control_sample |

## Validation

- Labeled validation set presente.
- Calibration buckets empíricos definidos.
- Sampling estratificado por `document_type` y `score_bucket`.
- Accuracy no es aggregate-only.
- Routing usa `calibrated_confidence`, no raw score.

## JSON Report

See `scripts/fixtures/valid-invoice-routing.json` for a complete validator-ready report.
