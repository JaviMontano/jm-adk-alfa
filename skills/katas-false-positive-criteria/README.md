<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-false-positive-criteria
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas False Positive Criteria

Kata 30 · Criterios Explícitos para Reducir Falsos Positivos. Criterios categóricos con ejemplos positivos y negativos por severidad para reducir falsos positivos; disable temporal por categoría para preservar la confianza cross-categoría.

## Resumen ejecutivo

Las instrucciones vagas ("sé conservador", "solo alta confianza") fallan porque el modelo las interpreta distinto cada turno. Esta skill reemplaza esos adjetivos por criterios categóricos con ejemplos positivos y negativos por severidad, mide FP rate por categoría (no agregada) y deshabilita temporalmente la categoría ruidosa para no destruir la confianza en todas las demás. La precisión es prerrequisito de la utilidad: un reviewer con 1 de 5 falsos positivos hace que los devs ignoren incluso los flags reales.

## Triggers

- false positive criteria
- categorical criteria
- fp rate by category
- explicit criteria

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando haya que reescribir un prompt de clasificación o review que usa lenguaje vago de confianza, diagnosticar por qué los devs ignoran los flags de un reviewer automático, o decidir qué hacer con una categoría que dispara demasiados falsos positivos.

## Output Format

Markdown con summary, evidence, result, validation y risks. El result entrega los criterios categóricos por severidad (con ejemplos positivo/negativo) y, cuando aplica, la decisión de disable temporal por categoría.
