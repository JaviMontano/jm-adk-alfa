---
name: katas-deterministic-agent-loop
version: 1.0.0
description: "Control de bucle agentico por stop_reason tipado (tool_use vs end_turn), nunca por prosa del modelo; halt y budget deterministas."
owner: "JM Labs"
triggers:
  - deterministic loop
  - stop_reason
  - agent loop control
  - budget exceeded
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Deterministic Agent Loop

## Qué es

Un bucle agéntico que decide continuar o detenerse mirando SOLO el campo estructurado `stop_reason` que devuelve la API (`tool_use` vs `end_turn`), nunca la prosa que escribe el modelo. Cada iteración llama a `create(...)`, inspecciona `stop_reason` y enruta: `tool_use` despacha la herramienta y reinyecta el `tool_result`; `end_turn` finaliza; cualquier otro valor (`max_tokens`, `pause_turn`, etc.) eleva un error explícito. Aplica a escenarios como Customer Support y Multi-Agent Research, donde el control del turno debe ser predecible.

## Por qué importa (falla que evita)

Detener el bucle por heurística de texto convierte una frase casual del modelo ("task complete", "listo") en un halt silencioso a destiempo o, peor, en un bucle infinito cuando el modelo nunca pronuncia la frase esperada. El parseo de prosa es no determinista por construcción: depende del idioma, del tono y de la redacción del modelo. El control debe vivir en el contrato estructurado de la API, no en la superficie textual.

## Modelo mental

- Cada iteración produce un `stop_reason`: `tool_use` → dispatch, `end_turn` → halt, otros → error explícito.
- El `tool_result` se reinyecta como `role=user`, manteniendo el contrato turn-by-turn de la conversación.
- `max_tokens` / `pause_turn` inesperados deben fallar fuerte (raise), nunca silenciosamente.
- El bucle se acota con un budget configurable (`max_iterations`) que eleva `BudgetExceeded` al excederse.
- La prosa del modelo es output para el humano, no señal de control para la máquina.

## Patrón correcto

```python
while True:
    resp = create(...)
    if resp.stop_reason == "tool_use":
        dispatch(resp)
        continue
    elif resp.stop_reason == "end_turn":
        return resp
    else:
        raise UnhandledStop(resp.stop_reason)
```

## Anti-patrón

```python
DONE = ["task complete", "done", "listo"]
if any(p in text for p in DONE):
    return  # parsea prosa: halt silencioso o bucle infinito
```

## Argumento de certificación

El control del bucle vive en `stop_reason` + budget + handlers tipados, no en heurísticas de texto. Una implementación certificada (1) enruta exclusivamente por `stop_reason`, (2) trata todo valor no manejado como error explícito, y (3) acota la ejecución con un budget configurable que eleva `BudgetExceeded`.

## Cuándo activar

- Diseñar o revisar un bucle agéntico que llama a la API en iteraciones.
- Detectar control de flujo basado en parseo de texto ("done", "task complete").
- Definir condiciones de halt, manejo de `tool_use`/`end_turn` o límites de iteración.
- Triggers: `deterministic loop`, `stop_reason`, `agent loop control`, `budget exceeded`.

## Skills relacionadas

- `katas-pretooluse-guardrails`
- `katas-error-propagation-multi-agent`
- `katas-human-handoff-protocol`
