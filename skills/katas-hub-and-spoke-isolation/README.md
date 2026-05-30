<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hub-and-spoke-isolation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hub And Spoke Isolation

## Resumen ejecutivo

Kata 04 del kit JM-ADK. Enseña a aislar subagentes registrándolos como `AgentDefinition` en `ClaudeAgentOptions.agents` y despachándolos vía el built-in Task tool. Cada Task abre una sesión nueva con su propio `system_prompt`, `tools` y `model`; el coordinador recibe solo el último mensaje como `tool_result`. Esto acota el blast radius de prompt injection, evita la dilución de contexto y permite usar modelos baratos (haiku) por subagente. Escenarios: Multi-Agent Research y Code Audit Pipeline.

## Triggers

- hub and spoke
- subagent isolation
- agentdefinition
- task tool isolation

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill cuando el diseño multi-agente requiera contexto vacío por tarea, modelo distinto por subagente o acotar el blast radius de un prompt injection. El patrón canónico: `AgentDefinition(tools=[], model="haiku")` registrado en `agents={...}` con `allowed_tools=["Task"]`.

## Output Format

Markdown con summary, evidence, result, validation y risks.
