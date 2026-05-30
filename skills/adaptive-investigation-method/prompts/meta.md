<!--
generated-by: scripts/scaffold-skill.py
generated-for: adaptive-investigation-method
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Adaptive Investigation Method Meta Prompt

Decide si `adaptive-investigation-method` debe activarse, si el alcance es seguro y que agentes de apoyo participan.

## Activation Check

- ¿El dominio es desconocido y grande, y leerlo todo es inviable?
- ¿El costo de exploracion debe estar acotado por diseno?
- ¿Hay un objetivo concreto y un budget (o se puede inferir uno)?
- ¿No hay una skill mas especifica que ya resuelva el caso de forma determinista?

## Routing de agentes

- **Lead** construye el loop (budget, mapa, ranking, deep-dive).
- **Support** caza blind spots y sesgo de confirmacion en la priorizacion.
- **Guardian** valida el checklist y bloquea el anti-patron (plan rigido, `read_all_files`, re-plan reflejo).
- **Specialist** aporta detalle de Claude Code / Agent SDK (persistencia del scratchpad, `context: fork`, regla de re-plan como funcion pura).

## No activar si

El dominio es pequeno (leerlo entero es mas barato que mapearlo) o la tarea es determinista sin descubrimiento.
