<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Persistent Memory Design Meta Prompt

Evalúa si `persistent-memory-design` debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- Trigger match: la petición habla de memoria duradera, scratchpad, notas de investigación o supervivencia a `/compact`.
- Domain fit: hay una tarea larga o multi-sesión cuyo estado debe persistir; no es un apunte efímero de un turno.
- Sufficient input: hay un objetivo y un lugar donde vive el estado hoy.
- No safer specialized skill: si el foco real es resume/fork de sesión usa `session-lifecycle-management`; si es trazabilidad de claims usa `provenance-engineering`.

## Routing de agentes

- lead: construye el archivo (ruta + esquema + bootstrap + upserts).
- support: detecta relecturas, estado aún en la conversación y entradas sin evidencia.
- guardian: valida el checklist y veta el anti-patrón.
- specialist: aporta detalle de SDK/Claude Code (compact, prompt cache, ciclo de sesión).
