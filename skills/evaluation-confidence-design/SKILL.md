---
name: evaluation-confidence-design
version: 1.0.0
description: "Disenar evaluacion con confidence calibrada contra labeled set, stratified sampling y criterios categoricos para reducir falsos positivos."
owner: "JM Labs"
triggers:
  - evaluation confidence design
  - confidence calibration
  - stratified sampling
  - false positive criteria
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Evaluation Confidence Design

## Capacidad

Diseñar e implementar el sistema de evaluación de un agente o pipeline de clasificación de modo que la decisión de aceptar/rechazar un hallazgo no dependa de la `confidence` cruda del modelo, sino de un umbral **calibrado contra un labeled set**. La capacidad incluye: muestreo estratificado por `document_type` (u otra dimensión de riesgo) para que cada estrato esté representado, criterios categóricos con ejemplos positivos y negativos por severidad, capacidad de desactivar temporalmente una categoría con alta tasa de falsos positivos, y reporte de accuracy desglosada por estrato y por categoría en vez de una métrica agregada que oculta el sesgo.

## Cuándo usarla

- Cuando un agente emite hallazgos con un score de `confidence` y alguien propone usar ese número crudo como umbral de corte.
- Cuando el equipo evalúa con una sola muestra global y reporta una accuracy agregada.
- Cuando una categoría concreta dispara muchos falsos positivos y no hay forma de aislarla.
- Cuando el criterio de una categoría es vago ("sé conservador") en lugar de categórico con ejemplos +/-.
- Antes de promover un evaluador a producción: la calibración es un gate de release.

## Cómo construir

1. **Construir el labeled set.** Reúne ejemplos etiquetados por humano (positivo/negativo) y, crucialmente, etiquétalos también por `document_type` y por categoría de hallazgo. Sin ground truth no hay calibración posible.
2. **Estratificar el muestreo.** Muestrea por `document_type` (u otra dimensión de riesgo) en vez de aleatorio global, garantizando un mínimo por estrato para que los estratos raros no desaparezcan de la métrica.
3. **Calibrar la confidence.** Ajusta un mapeo (p. ej. binning o isotonic/Platt) de `confidence` cruda a probabilidad observada en el labeled set. El umbral de corte se elige sobre la confidence calibrada, no sobre la cruda.
4. **Definir criterios categóricos.** Para cada categoría, redacta un criterio categórico con ejemplos positivos y negativos por nivel de severidad. Evita instrucciones vagas.
5. **Medir FP rate por categoría.** Calcula la tasa de falsos positivos por categoría, no solo la accuracy global. Una categoría puede arrastrar la precisión sin que la métrica agregada lo muestre.
6. **Habilitar disable temporal.** Implementa un flag para desactivar una categoría con FP rate alto mientras se rediseña su criterio, sin tumbar el resto del evaluador.
7. **Reportar desglosado.** Emite accuracy y FP rate por estrato y por categoría. Corre `scripts/qa/run-confidence-fp-tests.py` como gate.

## Patrón correcto

```python
# GOOD: corte sobre confidence CALIBRADA + muestreo estratificado + FP por categoria
from collections import defaultdict

def calibrate(raw_conf: float, calibration_map: list[tuple[float, float]]) -> float:
    # calibration_map: bins (raw_upper, observed_precision) fit on labeled set
    for upper, observed in calibration_map:
        if raw_conf <= upper:
            return observed
    return calibration_map[-1][1]

def stratified_sample(labeled: list[dict], per_stratum: int) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in labeled:
        buckets[row["document_type"]].append(row)
    sample = []
    for doc_type, rows in buckets.items():
        sample.extend(rows[:per_stratum])  # guarantee min per stratum
    return sample

def evaluate(findings, calibration_map, threshold, disabled_categories):
    fp_by_category: dict[str, list[bool]] = defaultdict(list)
    accepted = []
    for f in findings:
        if f["category"] in disabled_categories:
            continue  # temporal disable for high-FP category
        if calibrate(f["raw_confidence"], calibration_map) >= threshold:
            accepted.append(f)
            fp_by_category[f["category"]].append(f["label"] == "negative")
    fp_rate = {c: sum(v) / len(v) for c, v in fp_by_category.items()}
    return accepted, fp_rate  # report FP per category, not aggregate accuracy
```

## Anti-patrón

```python
# ANTI: confidence cruda como umbral, muestra global, accuracy agregada
def evaluate_bad(findings, raw_threshold=0.7):
    accepted = [f for f in findings if f["raw_confidence"] >= raw_threshold]
    # criterio vago: "be conservative" sin ejemplos +/-
    # sin estratificacion: estratos raros invisibles
    accuracy = sum(f["label"] == "positive" for f in accepted) / len(accepted)
    return accepted, accuracy  # metrica agregada oculta el sesgo por categoria
```

## Checklist de validación

- ¿El umbral usa confidence **calibrada** contra el labeled set, no la cruda?
- ¿El muestreo es **estratificado** por `document_type` con mínimo por estrato?
- ¿Cada categoría tiene **criterio categórico con ejemplos +/-** por severidad?
- ¿Se reporta **FP rate por categoría**, no solo accuracy agregada?
- ¿Existe **disable temporal** para categorías con FP alto?
- ¿Corre `scripts/qa/run-confidence-fp-tests.py` y pasa como gate?

## Katas y skills relacionadas

- Katas: 29, 30.
- Skills relacionadas: `katas-confidence-stratified-sampling`, `katas-false-positive-criteria`.
