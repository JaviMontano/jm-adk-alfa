---
name: katas-confidence-stratified-sampling
version: 1.0.0
description: "Confidence calibration contra labeled set y stratified sampling por document_type; accuracy desglosada, nunca agregada."
owner: "JM Labs"
triggers:
  - confidence calibration
  - stratified sampling
  - calibrated confidence
  - accuracy by segment
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 29 · Confidence Calibration y Stratified Sampling

## Qué es

En extracciones masivas el modelo emite `field_confidence` scores a nivel de campo. Esos scores deben CALIBRARSE contra un labeled validation set, porque la confianza raw está sesgada: un `0.9` raw no significa 90% de probabilidad real de correctitud. Una vez calibrados, los scores enrutan el trabajo: high confidence calibrada va a procesamiento automático con stratified sampling de control; low confidence va a revisión humana. La accuracy se mide siempre desglosada por `document_type` y por field, nunca agregada.

## Por qué importa (falla que evita)

Reportar "97% accuracy global" y automatizar todo lo high-confidence suena seguro hasta que un `document_type` específico falla en silencio dentro del promedio. El número agregado oculta que un segmento minoritario tiene 60% de accuracy. El stratified sampling es la red que detecta nuevos modos de error que un validation set viejo no captura, especialmente drift en segmentos poco frecuentes.

## Modelo mental

- `field_confidence` raw != probabilidad real de correctitud: el score crudo está sesgado.
- Calibración: comparar score raw vs accuracy empírica por bucket en el labeled validation set.
- Stratified sampling: muestrear proporcionalmente por `document_type` y por rango de score, no aleatorio sobre el total.
- La accuracy agregada miente; reportar siempre desglosada por `document_type` y field.
- Routing operativo: high confidence calibrada → auto + muestreo de control; low → revisión humana.

## Patrón correcto

```python
# Schema: cada extracción exige field_confidence tipado y acotado
EXTRACT_WITH_CONF = {
    "field_value": {"type": "string"},
    "field_confidence": {"type": "number", "min": 0, "max": 1},  # required
}

def calibrate(predictions, labeled_set):
    # buckets por threshold; compara confianza predicha vs verdad
    buckets = {}
    for pred, truth in zip(predictions, labeled_set):
        b = round(pred["field_confidence"], 1)
        buckets.setdefault(b, []).append(pred["field_value"] == truth)
    # accuracy empírica por bucket = confianza calibrada
    return {b: sum(hits) / len(hits) for b, hits in buckets.items()}

def stratified_sample(extractions, n_per_type=10):
    # muestrea high-confidence proporcional por document_type
    by_type = {}
    for e in extractions:
        by_type.setdefault(e["document_type"], []).append(e)
    return {t: sample_high_conf(items, n_per_type) for t, items in by_type.items()}

# Routing por accuracy empírica calibrada, no por score raw
```

## Anti-patrón

```python
if extraction["field_confidence"] >= 0.9:
    return "auto"  # confía ciegamente en el score raw, sin calibrar

print(f"Accuracy: {global_acc}")  # 97% global que oculta 60% en un segmento
```

## Argumento de certificación

- Diferenciar confianza raw de confianza calibrada y explicar por qué la raw está sesgada.
- Describir stratified sampling y por qué supera al random sampling para detectar drift en segmentos minoritarios.
- Rechazar reportar accuracy agregada; exigir desglose por `document_type` y field.
- Conectar la calibración con el routing operativo (auto vs human).

## Cuándo activar

Activar en extracciones estructuradas masivas donde el modelo emite confidence scores y hay que decidir qué se automatiza y qué va a revisión humana; o cuando se pide medir/repor­tar accuracy de un pipeline de extracción.

## Skills relacionadas

- `katas-provenance-preservation`
- `katas-false-positive-criteria`
- `katas-multipass-prompt-chaining`
