<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Human Handoff Protocol Primary Prompt

## Objective

Aplicar el protocolo de handoff a humano: detectar la precondición de escalada, invocar `escalate_to_human` con un payload tipado autocontenido y terminar el bucle.

## Required Inputs

- El caso de soporte y su estado (`customer_id`, historial de acciones).
- La política o límite aplicable (p.ej. tope de reembolso del tier).
- El motivo de la escalada (límite excedido, irreversibilidad o conflicto de datos).

## Process

1. Evalúa la precondición de escalada: límite excedido, decisión irreversible o conflicto de datos.
2. Si se cumple, invoca `escalate_to_human` y corta la generación de prosa.
3. Construye el payload tipado: `customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`.
4. Trata la escalada como end-state: no continúes hasta que el humano resuelva.

## Output

Payload JSON emitido vía `escalate_to_human` con los cinco campos fijos, autocontenido (el humano no debe leer la conversación previa). Sin prosa posterior a la llamada.
