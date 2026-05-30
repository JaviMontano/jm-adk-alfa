<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation Primary Prompt

## Objective

Diseñar o auditar un prompt/agente para mitigar la dilución softmax: edge placement de reglas críticas + compactación al cruzar el umbral de contexto.

## Required Inputs

- El system prompt o la arquitectura del agente.
- Las reglas críticas (seguridad, compliance, invariantes) que NO pueden diluirse.
- El modelo y su ventana de contexto (para calcular `usage_fraction`).
- Si la conversación es multi-turno y crece con el tiempo.

## Process

1. Identifica las reglas críticas. Colócalas al inicio del prompt como `<rules>critical_policy</rules>`.
2. Repite las mismas reglas al final como `REMINDER:<rules>critical_policy</rules>`. Ambos bordes son zonas de atención alta.
3. Ubica los datos ricos y voluminosos en el centro.
4. Instrumenta el gate: `if usage_fraction(history) > 0.55: history = compact(history, preserve=['rules','decisions','escalations'])`.
5. Valida que las reglas aparecen en ambos bordes y que la compactación no borra lo crítico.

## Output

Devuelve el entregable en este formato: Markdown con summary, evidence, result, validation y risks. Incluye el argumento de certificación (curva U, regla bordes/centro, umbral justificado).
