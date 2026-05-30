<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario de Customer Support. El cliente `CUST-48217` pide un reembolso de USD 2,400 por un cargo duplicado. El agente confirmó el cargo duplicado en el historial de pagos y ya verificó la identidad del cliente. El límite de reembolso del tier-2 del agente es USD 1,000.

```python
refund_amount = 2400
tier2_limit = 1000
customer_id = "CUST-48217"
```

El agente debe escalar a un humano porque el monto excede su límite. ¿Cómo termina el turno?
