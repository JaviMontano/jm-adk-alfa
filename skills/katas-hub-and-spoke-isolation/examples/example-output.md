<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Se rediseña la investigación multi-agente como hub-and-spoke: un subagente `extractor` procesa UN documento por sesión, con contexto vacío y `model="haiku"`. El coordinador despacha vía Task y agrega solo el último mensaje de cada subagente.

## Evidence (GOOD)

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

## Anti-patrón evitado (ANTI)

```python
# Un solo agente con TODO concatenado: sin agents, sin Task.
# Contexto diluido, politicas cruzadas, un unico modelo caro (opus) para los 30 docs,
# y blast radius amplio: un documento envenenado contamina la sesion completa.
single_agent(prompt=coordinator_history + thirty_documents_concatenated, model="opus")
```

## Result

- 30 invocaciones de Task, una por documento, cada una en sesión nueva con `haiku`.
- El coordinador (modelo caro) corre una sola vez para sintetizar, agregando solo los `tool_result` finales.
- Blast radius de cualquier documento envenenado acotado a su propia sesión de extracción.

## Validation

- Aislamiento estructural vía `AgentDefinition` + Task, no vía system prompt.
- Cada Task abre una sesión nueva por construcción del SDK.
- El coordinador no recibe el historial interno de ningún subagente.
- Quiz coherente: B · B · B.

## Risks and Limits

- Si se añaden tools innecesarias al extractor, vuelve a crecer la superficie de ataque.
- La síntesis final sigue dependiendo de la calidad de los hechos extraídos por `haiku`.
