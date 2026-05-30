<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Precondicion `limit_exceeded` (refund > tier2_limit) dispara `escalate_to_human`. El handoff emite un payload tipado autocontenido y corta la generacion: es el end-state del bucle, no una pausa.

## Evidence

- Politica: `tier2_limit = 500`; reembolsos por encima requieren humano (dado en el input).
- Tool `escalate_to_human` con input schema estricto (supuesto: ya existe en el SDK; si no, definirlo).

## Result

GOOD:

```python
def handle_refund(ctx, refund_amount):
    if refund_amount > ctx.tier2_limit:
        return tool_call("escalate_to_human", {
            "customer_id": ctx.customer_id,
            "issue_summary": f"Refund {refund_amount} exceeds tier2 limit {ctx.tier2_limit}",
            "actions_taken": ctx.actions_taken,
            "escalation_reason": "limit_exceeded",
            "recommended_action": "Approve manually or deny with policy 4.2",
        })  # end-state: el turno termina; no se genera mas prosa
    return process_refund(ctx, refund_amount)
```

ANTI:

```python
def handle_refund(ctx, refund_amount):
    if refund_amount > ctx.tier2_limit:
        say("Lo siento, ese reembolso supera mi limite. Voy a hablar con mi supervisor...")
        # sigue generando; el operador debe leer todo el transcript
    return keep_going(ctx)
```

## Validation

- Precondicion `limit_exceeded` enumerada como rama explicita.
- Payload autocontenido: el operador resuelve sin leer el chat.
- Generacion cortada al retornar el tool_call.
- Handoff es end-state (un hook PostToolUse puede terminar la sesion).
- Test estructural: toda rama de escalada produce payload completo y no emite prosa de continuacion.

## Risks and Limits

- Si `escalate_to_human` no esta disponible: degraded mode documentado.
- Contrato de reanudacion (resume vs fresh + summary) cuando el humano resuelve.
