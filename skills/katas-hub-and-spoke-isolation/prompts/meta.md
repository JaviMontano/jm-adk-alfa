<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hub And Spoke Isolation Meta Prompt

Decide si `katas-hub-and-spoke-isolation` debe activarse, si el alcance es seguro y qué agentes de soporte participan.

## Activation Check

- Trigger match: el request menciona hub-and-spoke, subagent isolation, `AgentDefinition` o aislamiento vía Task.
- Domain fit: el problema es multi-agente (Multi-Agent Research, Code Audit Pipeline) y se busca contexto vacío por tarea, modelo distinto por subagente o acotar el blast radius.
- Sufficient input: hay una tarea de coordinador y subtareas/documentos despachables.
- No safer specialized skill available: si el foco es descomposición dinámica usar `katas-adaptive-investigation`; si es propagación de errores entre agentes usar `katas-multiagent-error-propagation`.

## No activar si

- Se trata de un único agente sin subtareas independientes.
- El usuario pide explícitamente concatenar todo el contexto (anti-patrón) sin querer aislamiento.
