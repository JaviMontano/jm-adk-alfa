<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation Meta Prompt

Evalúa si `katas-multiagent-error-propagation` debe activarse para la tarea entrante.

## Activation Check

- ¿Hay una topología multi-agente / hub-and-spoke donde un coordinador sintetiza resultados de subagentes? → activa.
- ¿El problema es cómo un subagente reporta un fallo (timeout, permission) versus un resultado vacío legítimo? → activa.
- ¿Hay sospecha de huecos silenciosos en un report que "se ve completo"? → activa.
- ¿La tarea es de errores tipados de un solo servidor MCP sin orquestación multi-agente? → considera `katas-mcp-structured-errors`.
- ¿La tarea es retry de extracción tipada con feedback? → considera `katas-validation-retry-feedback`.
- Input vacío o ajeno al dominio multi-agente → NO activar.
