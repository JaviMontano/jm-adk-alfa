<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## GOOD — handoff tipado, end-state

Precondición detectada: `refund_amount (2400) > tier2_limit (1000)`. El agente invoca la tool y corta la prosa.

```python
if refund_amount > tier2_limit:
    return tool_call('escalate_to_human', {
        'customer_id': 'CUST-48217',
        'issue_summary': 'Cargo duplicado de USD 2,400 confirmado en historial de pagos.',
        'actions_taken': ['Identidad verificada', 'Cargo duplicado confirmado'],
        'escalation_reason': 'refund_amount (2400) excede tier2_limit (1000)',
        'recommended_action': 'Aprobar reembolso de USD 2,400 por cargo duplicado',
    })
```

El operador recibe un caso autocontenido: no necesita leer la conversación. El bucle termina; un hook `PostToolUse` cierra la sesión.

## ANTI — prosa que no termina el bucle

```python
return 'Lo siento, ese reembolso supera mi límite. Voy a hablar con mi supervisor...'
# ...y sigue generando, sin payload, sin terminar el bucle
```

El operador hereda un transcript crudo y debe reconstruir el contexto bajo presión.

## Validación

- Precondición de escalada declarada (límite excedido).
- Los cinco campos del payload presentes y autocontenidos.
- Generación cortada tras la llamada; end-state respetado.
