<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Human Handoff Protocol

Handoff a humano con payload tipado autocontenido (customer_id, issue_summary, actions_taken); end-state del bucle, no pausa.

## Triggers

- human handoff
- escalate to human
- handoff payload
- escalation protocol

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Cuando el agente toca una política que no puede resolver (límite excedido, decisión irreversible, conflicto de datos), invoca `escalate_to_human`, suspende la prosa y emite un payload JSON estricto: `customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`. El handoff es un end-state del bucle, no una pausa. El operador humano recibe un caso autocontenido y accionable, no un transcript crudo que descifrar.

## Quick Use

Activa esta skill cuando el request coincida con los triggers y el agente deba escalar a un humano con un payload tipado en vez de seguir conversando. Verifica primero la precondición de escalada (límite, irreversibilidad, conflicto), luego construye el payload con los cinco campos fijos.

## Output Format

Payload JSON tipado (`customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`) emitido vía `escalate_to_human`, más una nota de validación del contrato.
