<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design Primary Prompt

## Objective

Disena el handoff a humano como end-state tipado del bucle para la tarea del usuario: identifica las precondiciones de escalada, define el contrato del payload e implementa la invocacion de `escalate_to_human` que corta la generacion.

## Required Inputs

- Dominio del agente y las politicas que puede / no puede resolver (limites, acciones irreversibles, fuentes de conflicto).
- La tool de escalada disponible (`escalate_to_human`) o el contrato a definir.
- Quien es el operador humano y bajo que presion decide.
- Definition of done: que test estructural prueba el handoff.

## Process

1. Enumera precondiciones de escalada como ramas explicitas (`limit_exceeded`, `irreversible_action`, `data_conflict`).
2. Define el payload tipado autocontenido (`customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`).
3. Implementa la invocacion de la tool cortando la generacion; el turno termina ahi.
4. Asegura el end-state (hook `PostToolUse` que termina la sesion si aplica).
5. Valida con test estructural: payload completo por rama + cero prosa de continuacion.

## Output

Devuelve el deliverable: Markdown con summary, evidence, result (codigo del handoff con bloque GOOD), validation (checklist) y risks. Marca supuestos cuando falte evidencia.
