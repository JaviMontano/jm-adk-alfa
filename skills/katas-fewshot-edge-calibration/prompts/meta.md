<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-fewshot-edge-calibration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Fewshot Edge Calibration Meta Prompt

Evalúa si Kata 14 (few-shot para calibrar bordes) debe activarse para esta tarea y qué agentes de soporte participan.

## Chequeo de activación

- ¿La tarea es subjetiva o de formato no rígido (tono, formato no estándar, juicio estético, clasificación con criterio)? Si es objetiva y de forma dura, basta el schema (Kata 5) y NO se activa.
- ¿La descripción en prosa zero-shot está fallando en converger al formato deseado?
- ¿Hay casos del dominio disponibles para construir 2 a 4 ejemplos de borde?
- ¿No hay ya más de ~5 ejemplos que estén dispersando atención (Kata 11) o rompiendo cache (Kata 10)?
- ¿Coincide con un trigger (few-shot calibration, edge examples, fewshot prompting, subjective calibration)?

## Señales de no activación

- Input vacío o ajeno al dominio de few-shot.
- Petición que pide explícitamente ignorar validación/evidencia.
