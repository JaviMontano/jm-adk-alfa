<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration

## Resumen ejecutivo

Capacidad de ingeniería para diseñar coordinadores hub-and-spoke: un hub despacha subagentes aislados con `AgentDefinition` + `Task`, cada uno en sesión nueva con contexto vacío, tools y modelo propios, y agrega sus resultados con errores estructurados. El valor central es contener el blast radius y nunca enmascarar un fallo de acceso como un resultado vacío válido.

## Triggers

- subagent orchestration
- hub and spoke
- coordinator agents
- error propagation

## Allowed tools

- Read
- Grep
- Glob
- Bash

## Quick use

1. Descompón la tarea en subtareas independientes que se beneficien de contexto aislado.
2. Declara cada spoke como `AgentDefinition` con tools mínimas y modelo barato cuando sea extracción.
3. Despacha con `Task`; el hub consume solo el último mensaje de cada spoke.
4. Modela el error del spoke con `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`.
5. Agrega distinguiendo `access_failure` de `valid_empty` y anota coverage gaps explícitos.

Detalle de construcción, patrón GOOD/ANTI y checklist en `SKILL.md`. Canon en `knowledge/body-of-knowledge.md`.

## Output format

Markdown con summary, evidence, result, validation y risks. Plantilla en `templates/output.md`.
