<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hub And Spoke Isolation Body of Knowledge

## Canon

Aislamiento hub-and-spoke con subagentes. Los subagentes se registran como `AgentDefinition` en `ClaudeAgentOptions.agents` y se despachan vía el built-in Task tool. Cada Task abre una sesión nueva con su propio `system_prompt`, `tools` y `model`; el coordinador recibe SOLO el último mensaje como `tool_result`.

### Conceptos clave

- **Topología hub-and-spoke**: el coordinador (hub) despacha, los especialistas (spokes) ejecutan con contexto vacío.
- **AgentDefinition**: contrato de un subagente con `description`, `prompt`, `tools` y `model` propios.
- **Built-in Task tool**: el mecanismo de despacho; cada invocación es una sesión nueva.
- **Aislamiento estructural por runtime**: el aislamiento no se pide en el system prompt; lo garantiza la construcción del SDK.
- **Modelo por subagente**: `haiku` barato para extracción; el modelo caro queda para la síntesis del coordinador.
- **Agregación de último mensaje**: el coordinador integra solo el `tool_result` final, no el historial interno del subagente.

### Señales de calidad

| Señal | Target |
|---|---|
| Aislamiento | Cada subagente arranca con contexto vacío vía Task, no con el historial del coordinador |
| Blast radius | Un prompt injection queda acotado a una sola tarea |
| Costo por tarea | Extracción corre en `haiku`; el modelo caro solo sintetiza |
| Superficie de tools | Cada subagente declara solo las tools que necesita (a veces `tools=[]`) |
| Agregación | El coordinador integra solo el último mensaje, sin fugar políticas cruzadas |

## Anti-patrón canónico

Un solo agente con TODO el contexto concatenado, sin `agents` y sin Task. Resultado: contexto diluido, políticas cruzadas filtradas entre tareas, blast radius amplio ante prompt injection y un único modelo caro para todo. El argumento de certificación se cae porque el aislamiento dependería del system prompt en lugar de ser estructural.

## Open Knowledge

- Quiz de referencia: B · B · B (blast radius acotado por aislamiento; modelo distinto por subagente vía `AgentDefinition`).
- Conecta con `katas-adaptive-investigation` (subagentes para deep-dive paralelo) y `katas-multiagent-error-propagation` (propagación estructurada de errores al coordinador).
