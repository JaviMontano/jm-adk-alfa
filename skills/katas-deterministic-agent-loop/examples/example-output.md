<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El bucle del agente de Customer Support se reescribe para enrutar por `stop_reason` en lugar de parsear prosa. Se añade manejo explícito de stops inesperados y un budget configurable que evita el bucle infinito.

## Anti-patrón (antes)

```python
DONE = ["task complete", "done", "listo"]

while True:
    resp = create(messages=messages, tools=tools)
    text = resp.content[0].text if resp.content else ""
    if any(p in text for p in DONE):  # parsea prosa: halt silencioso / bucle infinito
        return resp
    dispatch(resp)
```

## Patrón correcto (después)

```python
class UnhandledStop(Exception): ...
class BudgetExceeded(Exception): ...

def run(messages, tools, max_iterations=25):
    for _ in range(max_iterations):
        resp = create(messages=messages, tools=tools)
        if resp.stop_reason == "tool_use":
            tool_result = dispatch(resp)
            messages.append({"role": "user", "content": tool_result})
            continue
        elif resp.stop_reason == "end_turn":
            return resp
        else:
            raise UnhandledStop(resp.stop_reason)  # max_tokens / pause_turn / etc.
    raise BudgetExceeded(max_iterations)
```

## Validation

- [x] El halt depende de `stop_reason`, no de prosa del modelo.
- [x] `tool_use` despacha y reinyecta `tool_result` como `role=user`.
- [x] `end_turn` finaliza el bucle.
- [x] Todo `stop_reason` no manejado eleva `UnhandledStop` (fail fuerte).
- [x] Budget `max_iterations` presente; eleva `BudgetExceeded`.

## Risks and Limits

- Si el modelo usa `pause_turn`, el bucle lo trata hoy como `UnhandledStop`; añadir reanudación explícita si el modelo en uso lo emite.
- `max_iterations=25` es un default; calibrar según el flujo de Customer Support.
