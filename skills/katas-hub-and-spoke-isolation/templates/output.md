<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hub And Spoke Isolation Output

## Summary

{summary — qué subtareas se aislaron en sesiones hub-and-spoke}

## Evidence

{evidence — bloque GOOD con AgentDefinition + ClaudeAgentOptions(agents=..., allowed_tools=["Task"])}

## Result

{result — mapa de subagentes, modelo asignado a cada uno y política de agregación de último mensaje}

## Validation

{validation — aislamiento estructural confirmado; blast radius acotado a una tarea; sin historial del coordinador filtrado}

## Risks and Limits

{risks — fuga de políticas cruzadas, tools de más, modelo caro donde haiku basta}
