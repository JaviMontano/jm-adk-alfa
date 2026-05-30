<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Contexto: agente de customer support que procesa reembolsos. Politica: puede aprobar hasta `tier2_limit = 500`. Por encima de ese monto requiere aprobacion humana. El equipo de operaciones se queja de que, cuando el agente escala, le pasa el transcript completo del chat y el operador tarda en entender el caso.

Pedido: disena el handoff a humano para el caso `refund_amount > tier2_limit` usando la tool `escalate_to_human`, con un payload tipado autocontenido y comportamiento de end-state (el agente no debe seguir generando prosa tras escalar).
