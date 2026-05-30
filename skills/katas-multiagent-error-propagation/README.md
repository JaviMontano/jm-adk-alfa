<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation

Propagacion de errores multi-agente: distinguir access failure de valid empty, local recovery primero y coverage gap annotation.

## Triggers

- multiagent error propagation
- access failure vs empty
- coverage gap
- local recovery

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

En hub-and-spoke, los subagentes propagan errores al coordinador con contexto estructurado (`failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`). Cuatro reglas: local recovery primero, distinguir access failure de valid empty, coverage gap annotation explícita, y nunca enmascarar un error como success vacío. La falla que evita: un `{results:[]}` en timeout que produce un report confiado con hueco silencioso.

## Quick Use

Activa esta skill al diseñar o revisar orquestación multi-agente donde un coordinador sintetiza resultados de subagentes, o cuando un report "se ve completo" pero podría omitir fuentes que fallaron. Aplica el patrón GOOD del SKILL.md (`empty_valid` para vacíos legítimos, `success:False` con contexto para fallos de acceso) y rechaza el anti-patrón `except Exception: return {"results":[]}`.

## Output Format

Markdown con summary, evidence, result, validation y risks.
