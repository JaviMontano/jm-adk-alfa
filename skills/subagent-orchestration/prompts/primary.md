<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration Primary Prompt

## Objetivo

Diseñar e implementar un coordinador hub-and-spoke para la tarea del usuario: descomponer en spokes aislados (`AgentDefinition` + `Task`), agregar con errores estructurados y reportar coverage gaps.

## Inputs requeridos

- Tarea global a coordinar y subtareas candidatas.
- Tools y modelo disponibles por spoke (qué es extracción barata vs razonamiento).
- Restricciones de costo, latencia y tolerancia a fallo parcial.
- Definición de done: shape del resultado agregado.

## Proceso

1. Descompón la tarea en spokes independientes; justifica el fan-out frente a un pase único.
2. Declara cada spoke con prompt, `tools` mínimas y `model` (Haiku para extracción, Sonnet para razonamiento).
3. Despacha con `Task` en sesiones nuevas de contexto vacío; el hub consume solo el último mensaje.
4. Implementa el error tipado del spoke (`failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`) con local recovery previo.
5. Agrega distinguiendo `access_failure` de `valid_empty` y registra coverage gaps explícitos.
6. Valida contra el checklist antes de entregar.

## Output

Markdown con summary, evidence, result, validation y risks. El bloque de código del coordinador debe mostrar el patrón GOOD (no el anti-patrón).
