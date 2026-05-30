<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-confidence-stratified-sampling
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 29 · Primary Prompt

## Objective

Diseñar un pipeline de extracción masiva con confianza calibrada y routing operativo, reportando accuracy desglosada por `document_type` y field.

## Required Inputs

- Conjunto de documentos a extraer y sus `document_type`.
- Labeled validation set (predicciones con verdad conocida) para calibrar.
- Campos a extraer y umbral de tolerancia de error por field.
- Definition of done: qué fracción puede ir a auto y qué cobertura de muestreo se exige.

## Process

1. Define el schema con `field_confidence` (number, 0..1) required por field.
2. Calibra: agrupa predicciones en buckets de score y mide accuracy empírica por bucket contra el labeled validation set.
3. Stratified sampling: muestrea proporcional por `document_type` y rango de score, cubriendo segmentos minoritarios.
4. Enruta high-confidence calibrada a auto (con muestreo de control) y low a revisión humana.
5. Reporta accuracy desglosada por `document_type` y field; nunca un único número global.

## Output

Markdown con summary, evidence, result (tabla de accuracy por `document_type` + decisiones de routing), validation y risks.
