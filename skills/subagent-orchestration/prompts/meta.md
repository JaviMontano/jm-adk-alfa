<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration Meta Prompt

Decide si `subagent-orchestration` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation check

- Trigger match: la petición habla de coordinar subagentes, hub-and-spoke, agregación o propagación de errores.
- Domain fit: la tarea se descompone en subtareas independientes que se benefician de contexto aislado o de modelos distintos.
- Suficiencia de input: hay subtareas, tools/modelo por spoke y un shape de agregación esperado.
- No hay skill más segura: si la tarea es secuencial con estado denso compartido, considerar `prompt-chaining-design` en su lugar.

## Routing de agentes

- `lead` construye el coordinador y la agregación.
- `support` detecta blind spots: aislamiento nominal, errores swallowed, dependencias entre spokes.
- `guardian` valida el checklist y veta el anti-patrón (`except: return {"results": []}`).
- `specialist` aporta detalle de `AgentDefinition`, `Task`, selección de modelo y fan-out asíncrono.
