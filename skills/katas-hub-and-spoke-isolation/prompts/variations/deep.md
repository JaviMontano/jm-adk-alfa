<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hub And Spoke Isolation Deep Variation

Úsala cuando el diseño multi-agente tiene impacto alto, superficie de prompt injection real o consecuencias cross-tarea.

Incluye:

- Notas de discovery: qué subtareas son independientes y por qué cada una merece sesión propia.
- Opciones consideradas: un agente monolítico (anti-patrón) vs hub-and-spoke con `AgentDefinition` + Task, con su trade-off de costo y blast radius.
- Enfoque seleccionado: mapa `agents={...}`, asignación de `model` por subagente, `tools` mínimas por sesión y política de agregación de último mensaje en el coordinador.
- Validación: confirmar que el aislamiento es estructural (no vía system prompt) y que el blast radius queda acotado a una tarea.
- Riesgos: fuga de políticas cruzadas, sobre-aprovisionamiento de tools, modelo caro en tareas que `haiku` cubriría.
