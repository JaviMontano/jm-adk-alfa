<!--
generated-by: scripts/scaffold-skill.py
generated-for: evaluation-confidence-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Evaluation Confidence Design

Capacidad de ingeniería para diseñar la evaluación de un agente/clasificador de modo que el corte de aceptación use **confidence calibrada** (no cruda), muestreo **estratificado** por `document_type`, criterios categóricos con ejemplos +/- por severidad, **disable temporal** de categorías con muchos falsos positivos y reporte de accuracy/FP **desglosado por categoría**.

## Resumen ejecutivo

La confidence cruda de un modelo no es una probabilidad: usarla como umbral produce falsos positivos sesgados por estrato. Esta skill construye el labeled set, calibra el score, estratifica la muestra y reporta FP rate por categoría para que el evaluador sea apto para producción.

## Triggers

- evaluation confidence design
- confidence calibration
- stratified sampling
- false positive criteria

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Construye/etiqueta el labeled set por `document_type` y categoría.
2. Estratifica la muestra con mínimo por estrato.
3. Calibra la confidence contra el ground truth y fija el umbral sobre la calibrada.
4. Mide FP rate por categoría y desactiva temporalmente las categorías ruidosas.
5. Corre `scripts/qa/run-confidence-fp-tests.py` como gate antes de promover.

## Output Format

Markdown con summary, evidencia (labeled set + calibración), resultado (umbral y categorías activas), validación (checklist) y riesgos residuales.
