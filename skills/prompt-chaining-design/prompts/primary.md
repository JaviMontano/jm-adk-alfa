<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Prompt Chaining Design Primary Prompt

## Objective

Diseñar la cadena multi-pass para la tarea del usuario: pase local tipado + pase de integración sobre resúmenes, con schema de transición explícito.

## Required Inputs

- Tarea grande a resolver y volumen de unidades a procesar.
- Definición de la unidad atómica (qué es procesable de forma independiente).
- Restricciones de la integración final (qué decisión o síntesis produce el pase 2).
- Definition of done y criterio de justificación frente a single-pass.

## Process

1. Delimita la unidad atómica.
2. Define el schema de salida del pase local (campos + estado de error tipado).
3. Define el schema de transición (colección tipada de resúmenes).
4. Implementa el pase local aislado, idempotente y paralelizable.
5. Implementa el pase de integración que solo lee resúmenes.
6. Justifica el chaining frente a single-pass o colápsalo.

## Output

Devuelve: summary, evidence (los schemas tipados de cada pase y el contrato de transición), result (la cadena diseñada), validation (checklist) y risks. El pase de integración nunca debe ver datos crudos.
