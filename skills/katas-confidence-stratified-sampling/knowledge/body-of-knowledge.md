<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-confidence-stratified-sampling
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 29 · Body of Knowledge

## Canon

Escenarios: Multi-Agent, Structured Extraction.

En extracciones masivas el modelo emite `field_confidence` scores. Esos scores se CALIBRAN contra un labeled validation set porque la confianza raw está sesgada. Calibrados, enrutan trabajo: high confidence → auto + stratified sampling; low → revisión humana. La accuracy se mide por `document_type` y field, nunca agregada.

## Conceptos clave

- **Confianza raw vs calibrada:** `field_confidence` raw != probabilidad real de correctitud. Un `0.9` crudo puede corresponder a 70% de accuracy empírica.
- **Calibración:** comparar score vs accuracy empírica por bucket en el labeled validation set. La accuracy por bucket es la confianza calibrada.
- **Stratified sampling:** muestreo proporcional por `document_type` y rango de score. Supera al random porque garantiza cobertura de segmentos minoritarios donde aparece el drift.
- **Routing operativo:** high confidence calibrada → auto + muestreo de control; low → revisión humana.
- **Desglose obligatorio:** accuracy agregada miente; reportar por `document_type` y field.

## Señales de calidad

| Señal | Target |
|---|---|
| Calibración real | Scores comparados contra labeled validation set por bucket, no usados raw |
| Desglose | Accuracy reportada por `document_type` y field, nunca solo agregada |
| Cobertura de muestreo | Stratified sampling alcanza document_types minoritarios |
| Routing conectado | La decisión auto vs human deriva de la accuracy calibrada |
| Update safety | El trabajo manual existente se preserva |
| Offline contract | `assets/` y `scripts/check.sh` validan labeled set, buckets, sampling, accuracy y routing |

## Anti-patrón canónico

```python
if extraction["field_confidence"] >= 0.9:
    return "auto"  # confía ciegamente en el score raw, sin calibrar

print(f"Accuracy: {global_acc}")  # 97% global que oculta 60% en un segmento
```

El número global "97% accuracy" da seguridad falsa mientras un `document_type` falla en silencio. El stratified sampling es la red que captura nuevos modos de error.

## Deterministic Validation

- Exigir `labeled_validation_set.size > 0`, campos y `document_types`.
- Calibrar con `method=empirical-bucket-calibration` y `uses_raw_confidence_for_routing=false`.
- Exigir buckets con `sample_count`, `empirical_accuracy` y `calibrated_confidence` en rango 0..1.
- Exigir `sampling.strategy=stratified`, `random_total_only=false` y cobertura de todos los `document_types`.
- Rechazar `accuracy_report.aggregate_only=true`.
- Exigir `routing.basis=calibrated_confidence`.

## Quiz canónico (B·B·B)

- P1: NO automatizar sin calibración; comparar contra labeled validation por bucket.
- P2: reportar accuracy desglosada por `document_type` y field.
- P3: stratified sampling muestreando el bucket high-confidence detecta drift en segmentos minoritarios.
