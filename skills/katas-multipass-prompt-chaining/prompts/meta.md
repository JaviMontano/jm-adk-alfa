<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multipass Prompt Chaining Meta Prompt

Decidir si `katas-multipass-prompt-chaining` (Kata 12) debe activarse, si el alcance es seguro y qué agentes de soporte participan.

## Activation Check

- **Trigger match:** la petición menciona prompt chaining, multipass, "local then integrate" o schema de pases.
- **Domain fit:** la tarea no cabe en un solo prompt (muchos archivos, documento largo) y necesita salida tipada por unidad.
- **Sufficient input:** hay unidades enumerables y se pueden definir los schemas de pase 1 y pase 2.
- **No safer specialized skill:** no existe una skill más específica para el dominio concreto.

## Cuándo NO activar

- La tarea cabe holgadamente en single-pass y el overhead de coordinación supera el beneficio.
- No hay unidades separables ni schemas de transición definibles.
- La petición pide explícitamente saltarse validación o evidencia (conflicto con el filtro de calidad).
