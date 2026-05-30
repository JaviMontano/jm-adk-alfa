<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-persistent-scratchpad
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Persistent Scratchpad Primary Prompt

## Objective

Aplicar el patrón de scratchpad persistente: mantener `investigation-scratchpad.md` como memoria durable de la investigación, que sobreviva a `/compact` y a reinicios de sesión.

## Required Inputs

- Objetivo de la investigación o tarea de largo aliento.
- Estado previo, si lo hay (existencia de `investigation-scratchpad.md`).
- Restricciones y criterio de hecho.

## Process

1. Al reanudar, leer `investigation-scratchpad.md` UNA vez para reconstruir el estado (decisiones, hallazgos, pendientes).
2. Investigar; cuando una conclusión quede validada, anexarla a la sección correspondiente con fecha y referencia a la evidencia.
3. NO persistir monólogo interno, hipótesis sin confirmar ni dudas pasajeras.
4. NO re-leer el scratchpad cada turno: referenciar lo ya cargado (preserva el cache, Kata 10).

## Output

Devuelve el scratchpad estructurado (`## Decisiones`, `## Hallazgos`, `## Pendientes`) más el estado de validación y los riesgos residuales.
