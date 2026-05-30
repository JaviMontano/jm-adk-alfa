<!--
generated-by: scripts/scaffold-skill.py
generated-for: agentic-loop-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Agentic Loop Engineering Output

## Summary

{summary}

## Evidence

Patrón correcto (GOOD) vs. anti-patrón (ANTI):

```python
{evidence}
```

## Result

Loop de control construido (enrutado por `stop_reason`, dispatch de herramientas, reinyección de `tool_result`, budget duro):

```python
{result}
```

## Validation

- [ ] Control en `stop_reason`, no en texto del modelo.
- [ ] Cada señal posible tiene handler o `raise`.
- [ ] `tool_result` reinyectado como `user` con `tool_use_id`.
- [ ] Budget configurable dispara `BudgetExceeded`.
- [ ] Fallos fuertes, no halts silenciosos.
- [ ] Transiciones instrumentadas.

{validation}

## Risks and Limits

{risks}
