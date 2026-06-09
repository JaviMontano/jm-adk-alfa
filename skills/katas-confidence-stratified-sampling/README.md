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

Markdown con summary, evidence, result (decisiones de routing + tabla de accuracy por `document_type` y field), validation y risks. Para handoffs críticos, incluir un JSON compatible con `assets/confidence-calibration-report-contract.json`.

## Deterministic Assets

- `assets/manifest.json` lista el contrato local.
- `assets/calibration-policy.json` exige labeled validation y buckets empíricos.
- `assets/stratified-sampling-policy.json` exige cobertura por `document_type` y rango de score.
- `assets/accuracy-reporting-policy.json` rechaza accuracy agregada como única métrica.
- `assets/routing-policy.json` exige decisiones basadas en confianza calibrada.
- `assets/evidence-policy.json` exige evidencia local offline.

## Offline Check

Run:

```bash
bash skills/katas-confidence-stratified-sampling/scripts/check.sh
```
