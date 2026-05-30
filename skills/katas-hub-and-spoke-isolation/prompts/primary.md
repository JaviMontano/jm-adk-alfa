<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hub And Spoke Isolation Primary Prompt

## Objective

Diseñar un sistema multi-agente con aislamiento hub-and-spoke: registrar subagentes como `AgentDefinition` en `ClaudeAgentOptions.agents` y despacharlos vía el built-in Task tool, de modo que cada subagente arranque con contexto vacío y modelo propio.

## Required Inputs

- Tarea del coordinador (qué se debe sintetizar al final).
- Lista de subtareas o documentos a despachar a subagentes.
- Restricciones de costo (qué tareas pueden correr en `haiku`).
- Definición de done: qué cuenta como deliverable agregado por el coordinador.

## Process

1. Identifica las subtareas independientes (un documento, un dominio de auditoría).
2. Define cada subagente con `AgentDefinition(description, prompt, tools, model)`; usa `tools=[]` y `model="haiku"` cuando solo extrae hechos.
3. Registra el mapa en `ClaudeAgentOptions(agents={...}, allowed_tools=["Task"], max_turns=...)`.
4. Despacha cada subtarea vía Task (sesión nueva, contexto vacío).
5. Agrega en el coordinador SOLO el último mensaje (`tool_result`) de cada subagente.

## Output

Devuelve el deliverable en este formato: Markdown con summary, evidence, result, validation y risks. Incluye el bloque de código GOOD con `AgentDefinition` + `ClaudeAgentOptions`.
