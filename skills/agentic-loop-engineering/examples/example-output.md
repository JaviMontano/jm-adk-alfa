# Example Output

## Summary

Se reemplaza el control por prosa (`"done" in text`) por un bucle que enruta sobre `stop_reason` tipado, con dispatch de herramientas, reinyección de `tool_result` y un techo duro de 20 iteraciones. El agente deja de colgarse y de detenerse a destiempo.

## Evidence

```python
# ANTI (lo que había): control por prosa, sin budget
while True:
    resp = client.messages.create(model=MODEL, messages=messages)
    if "done" in resp.content[0].text.lower():  # frágil + sin techo
        break
    run_some_tool()
```

## Result

```python
# GOOD: control por stop_reason, dispatch, reinyeccion, budget duro
class UnhandledStop(Exception): ...
class BudgetExceeded(Exception): ...

HANDLERS = {"search": run_search, "read_file": run_read_file}

def run_agent_loop(client, messages, tools, max_iterations=20):
    for _ in range(max_iterations):
        resp = client.messages.create(model=MODEL, messages=messages, tools=tools)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            return resp

        if resp.stop_reason == "tool_use":
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    handler = HANDLERS[block.name]            # nombre desconocido = fallo fuerte
                    out = handler(**block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": out,
                    })
            messages.append({"role": "user", "content": results})
            continue

        raise UnhandledStop(resp.stop_reason)                  # senal no contemplada
    raise BudgetExceeded(max_iterations)                        # techo duro
```

## Validation

- [x] Control en `stop_reason`, no en texto.
- [x] `end_turn` y `tool_use` con handler; el resto hace `raise`.
- [x] `tool_result` reinyectado como `user` con `tool_use_id`.
- [x] `max_iterations=20` configurable dispara `BudgetExceeded`.
- [x] Fallos fuertes, no halts silenciosos.

## Risks and Limits

- El budget está en iteraciones; para gastos largos conviene añadir techo por tokens vía `resp.usage`.
- Si el SDK introduce nuevas señales (`pause_turn`), caerán en `UnhandledStop` por diseño: revisar al actualizar versión.
- `Transport closed` debe tratarse como `degraded_transport` con reintento acotado, fuera de este loop base.
