<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-message-batch-processing
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 17 · Meta Prompt

Evalúa si `katas-message-batch-processing` debe activarse, si el alcance es seguro y qué agentes de soporte deben participar.

## Chequeo de activación

- ¿La carga es offline y tolerante a latencia (auditoría, backfill, evaluación, extracción masiva)?
- ¿El volumen justifica un batch (cientos o miles de requests) en vez de llamadas individuales?
- ¿Aparecen triggers como `message batches`, `batch processing`, `custom_id`, `offline batch`?
- ¿El costo importa y se puede aprovechar el ~50% de ahorro frente al modo real-time?

## NO activar si

- La tarea requiere respuesta interactiva en tiempo real.
- Hay una única request o un puñado de ellas sin restricción de costo ni latencia.
- Las requests dependen unas de otras y no pueden procesarse de forma independiente.
