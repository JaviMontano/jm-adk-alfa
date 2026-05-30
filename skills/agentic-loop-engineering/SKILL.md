---
name: agentic-loop-engineering
version: 1.0.0
description: "Construir el bucle de control agentico que enruta por stop_reason tipado con budget duro y handlers explicitos, no por prosa."
owner: "JM Labs"
triggers:
  - agentic loop engineering
  - agent control loop
  - stop_reason routing
  - loop budget
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Agentic Loop Engineering

## Capacidad

Construir el bucle de control de un agente que enruta por `stop_reason` tipado, con budget duro y handlers explícitos por señal, en lugar de inferir el control desde la prosa del modelo. El loop es la columna vertebral del agente: cada iteración decide entre despachar herramientas, detenerse o fallar fuerte. La capacidad es saber diseñar esa máquina de estados para que sea determinista, observable y acotada en producción.

## Cuándo usarla

- Cuando se implementa el bucle que llama al modelo, ejecuta herramientas y reinyecta resultados.
- Cuando un agente entra en bucles infinitos, se detiene a destiempo o produce halts impredecibles.
- Cuando hay que poner un techo de iteraciones o tokens al gasto de un agente autónomo.
- Cuando se migra un agente desde control por texto (`"done" in text`) hacia control por señal estructurada.

## Cómo construir

1. Define la condición del loop como `while True` y resuelve el control únicamente con el campo `stop_reason` (o equivalente tipado) de la respuesta del modelo.
2. Para `stop_reason == "tool_use"`: despacha cada bloque de herramienta a su handler, recoge el resultado y reinyéctalo en el historial como mensaje `user` con `tool_result`; continúa el loop.
3. Para `stop_reason == "end_turn"`: detén el loop y devuelve el resultado final (halt limpio).
4. Para cualquier otra señal no contemplada: `raise UnhandledStop(stop_reason)` — falla fuerte, nunca un halt silencioso.
5. Acota el gasto: un contador `iterations` contra `max_iterations` que dispara `BudgetExceeded` cuando se supera. Hazlo configurable, no constante mágica.
6. Instrumenta cada transición (iteración, señal, herramienta, latencia) para poder auditar el loop después.

## Patrón correcto

```python
# GOOD: control enrutado por stop_reason tipado, budget duro, fallo fuerte
def run_agent_loop(client, messages, tools, handlers, max_iterations=20):
    for iteration in range(max_iterations):
        resp = client.messages.create(model=MODEL, messages=messages, tools=tools)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            return resp                       # halt limpio

        if resp.stop_reason == "tool_use":
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    handler = handlers[block.name]   # KeyError = fallo fuerte
                    result = handler(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        raise UnhandledStop(resp.stop_reason)  # señal no contemplada
    raise BudgetExceeded(max_iterations)        # techo duro
```

## Anti-patrón

```python
# ANTI: control por prosa -> halt silencioso o bucle infinito
while True:
    resp = client.messages.create(model=MODEL, messages=messages)
    text = resp.content[0].text
    if "done" in text.lower():     # frágil: el modelo dice "not done" y sale
        break
    if "use tool" in text.lower(): # no hay budget, no hay tool_result tipado
        run_some_tool()
    # sin max_iterations: si nunca aparece "done", bucle infinito
```

## Checklist de validación

- ¿El control vive en `stop_reason` (señal tipada) y no en el texto del modelo?
- ¿Cada señal posible tiene handler explícito y las no contempladas hacen `raise`?
- ¿Los `tool_result` se reinyectan como mensaje `user` con `tool_use_id` correcto?
- ¿Existe un budget configurable (`max_iterations` / tokens) que dispara `BudgetExceeded`?
- ¿Los fallos son fuertes y observables, no halts silenciosos?
- ¿Cada transición del loop queda instrumentada para auditoría?

## Katas y skills relacionadas

- Kata fundacional: `katas-01`.
- Skills relacionadas: `katas-deterministic-agent-loop`, `tool-result-injection`, `agent-budget-control`.
