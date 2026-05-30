<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-confidence-stratified-sampling
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 29 · Confidence Calibration y Stratified Sampling

## Resumen ejecutivo

Para extracciones masivas, calibra los `field_confidence` scores del modelo contra un labeled validation set antes de confiar en ellos: la confianza raw está sesgada. Con scores calibrados, enruta el trabajo (high confidence → auto + stratified sampling de control; low → revisión humana) y reporta accuracy desglosada por `document_type` y field, nunca agregada. El stratified sampling detecta modos de error nuevos que un promedio global oculta.

## Triggers

- confidence calibration
- stratified sampling
- calibrated confidence
- accuracy by segment

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Invoca esta skill cuando un pipeline de extracción estructurada emita confidence scores y haya que decidir qué automatizar, o cuando se pida medir la accuracy real del pipeline. Calibra antes de enrutar y reporta desglosado por segmento.

## Output Format

Markdown con summary, evidence, result (decisiones de routing + tabla de accuracy por `document_type`), validation y risks.
