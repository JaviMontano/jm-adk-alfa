<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Provenance Engineering Meta Prompt

Decide si `provenance-engineering` debe activarse, si el alcance es seguro, y qué agentes de soporte participan.

## Activation Check

- Trigger match: provenance, claim/source, conflicto entre fuentes, traza tipada.
- Domain fit: el output será usado para decidir, firmar o citar, y existe más de una fuente con posible contradicción.
- Sufficient input: hay fuentes con fecha y atributos a consolidar identificados.
- No safer specialized skill available: si la tarea es solo formato de salida o una única fuente indiscutible, esta skill no aplica.

## Routing de agentes

- **lead**: construye el modelo `Claim`, la captura de provenance y la fusión con marcado de conflictos.
- **support**: caza blind spots donde la provenance se pierde (derivados sin source, conflictos colapsados).
- **guardian**: ejecuta el checklist y bloquea el anti-patrón (prosa sin source/fecha, conflicto promediado).
- **specialist**: detalle SDK/Claude Code (schema tipado, claims a través de subagentes, cola de escalación, test como gate de CI).
