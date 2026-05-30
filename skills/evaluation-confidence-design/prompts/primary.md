<!--
generated-by: scripts/scaffold-skill.py
generated-for: evaluation-confidence-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Evaluation Confidence Design Primary Prompt

## Objective

Diseña el sistema de evaluación de un agente/clasificador para que el corte de aceptación use confidence calibrada contra un labeled set, muestreo estratificado por `document_type`, criterios categóricos con ejemplos +/- y reporte de FP rate por categoría.

## Required Inputs

- El agente/pipeline a evaluar y cómo emite su `confidence`.
- Labeled set disponible (o plan para construirlo), con `document_type` y categoría.
- Categorías de hallazgo y su severidad.
- Restricciones de producción (latencia, costo, tolerancia a FP por categoría) y definition of done.

## Process

1. Construye/inventaría el labeled set etiquetado por `document_type` y categoría.
2. Estratifica la muestra con mínimo por estrato.
3. Calibra la confidence cruda contra el ground truth; fija el umbral sobre la calibrada.
4. Redacta criterios categóricos con ejemplos +/- por severidad.
5. Calcula FP rate por categoría; marca candidatas a disable temporal.
6. Valida con `scripts/qa/run-confidence-fp-tests.py` y reporta desglosado.

## Output

Markdown con: summary, evidencia (labeled set + mapa de calibración), resultado (umbral calibrado, categorías activas/desactivadas, accuracy y FP por categoría), validación (checklist) y riesgos residuales.
