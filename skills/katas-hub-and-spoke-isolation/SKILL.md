---
name: katas-hub-and-spoke-isolation
version: 1.0.0
description: "Aislamiento multi-agente con AgentDefinition y built-in Task; cada subagente arranca con contexto vacio y modelo propio."
owner: "JM Labs"
triggers:
  - hub and spoke
  - subagent isolation
  - agentdefinition
  - task tool isolation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Hub And Spoke Isolation

## Qué es

Registrar subagentes como `AgentDefinition` dentro de `ClaudeAgentOptions.agents` y despacharlos a través del built-in Task tool. Cada invocación de Task abre una sesión nueva con su propio `system_prompt`, su propio set de `tools` y su propio `model`. El coordinador (hub) recibe SOLO el último mensaje del subagente como `tool_result`, no su historial interno. Aplica directamente a los escenarios Multi-Agent Research y Code Audit Pipeline.

## Por qué importa (falla que evita)

Pasar todo el historial del coordinador a cada subagente diluye la atención del modelo, filtra políticas y contexto que el subagente no debería ver, multiplica el costo (todo corre con el modelo caro) y aumenta el blast radius de un prompt injection: si un documento envenenado entra a un subagente sin aislamiento, contamina la sesión completa. El aislamiento estructural acota ese radio a una sola tarea.

## Modelo mental

- Topología hub-and-spoke: el coordinador despacha, los especialistas ejecutan con contexto vacío.
- Cada Task es una sesión nueva: el aislamiento es estructural por construcción del runtime, no convencional vía system prompt.
- Cada subagente puede tener `tools`, `system_prompt` y `model` distintos (por ejemplo `haiku`, barato, para extracción de hechos).
- El coordinador agrega solo el último mensaje de cada subagente, nunca su historial interno.
- Menos tools y menos contexto por subagente = menor superficie de ataque y menor costo.

## Patrón correcto

```python
extractor = AgentDefinition(
    description="Extrae hechos de UN documento",
    prompt="...",
    tools=[],
    model="haiku",
)
options = ClaudeAgentOptions(
    agents={"extractor": extractor},
    allowed_tools=["Task"],
    max_turns=15,
)
```

## Anti-patrón

```python
# Un solo agente con TODO el contexto concatenado:
# sin agents, sin Task -> contexto diluido, politicas cruzadas, modelo unico caro.
single_agent(prompt=coordinator_history + all_documents_concatenated)
```

## Argumento de certificación

El aislamiento entre tareas multi-agente es estructural vía `AgentDefinition` + Task, no convencional vía system prompt. Cada Task es una sesión nueva por construcción del SDK: el subagente no hereda el historial del coordinador, el blast radius queda acotado a una tarea, y cada subagente puede asignar un modelo distinto (haiku para extracción, sonnet/opus para síntesis) precisamente porque `AgentDefinition` lo permite. Respuestas del quiz: B · B · B.

## Cuándo activar

- Multi-Agent Research: coordinador que despacha extracción de hechos por documento.
- Code Audit Pipeline: auditoría con subagentes especializados por dominio (seguridad, estilo, dependencias).
- Cualquier diseño donde se quiera contexto vacío por tarea, modelo distinto por subagente o acotar el blast radius de un prompt injection.

## Skills relacionadas

- `katas-adaptive-investigation`
- `katas-multiagent-error-propagation`
- `katas-headless-code-review`
