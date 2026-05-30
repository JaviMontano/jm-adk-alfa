<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-adaptive-investigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Adaptive Investigation Meta Prompt

Decide si `katas-adaptive-investigation` (Kata 19) debe activarse para esta tarea.

## Activation Check

- El dominio o repositorio es desconocido y no hay un mapa previo confiable.
- La tarea pide investigar, mapear, auditar o entender una base de codigo o documento extenso.
- Hay riesgo de quemar contexto leyendo de mas si no se acota la exploracion.
- Existe (o se puede definir) un presupuesto de exploracion: archivos / queries / minutos.

## No activar cuando

- La tarea ya esta totalmente especificada y el plan es trivial y estable -> no se gana nada con re-plan.
- El input esta vacio o no hay objetivo de investigacion -> pedir el objetivo primero.
- Solo se necesita una edicion puntual conocida -> usar `katas-builtin-tool-selection`.
