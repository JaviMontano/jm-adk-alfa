<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop Body of Knowledge

## Canon

Kata 01 · Bucle agéntico determinista. El bucle decide continuar o detenerse mirando SOLO el campo estructurado `stop_reason`, nunca la prosa del modelo.

### Conceptos clave

- **`stop_reason` como contrato de control**: la API devuelve un valor tipado por iteración. `tool_use` → despachar herramienta y continuar. `end_turn` → finalizar. Otros (`max_tokens`, `pause_turn`, `stop_sequence`) → error explícito.
- **Contrato turn-by-turn**: el `tool_result` se reinyecta como `role=user`, cerrando el turno de herramienta antes de la siguiente llamada.
- **Fail fuerte**: un `stop_reason` no manejado debe elevar (`raise UnhandledStop`), nunca degradar a un retorno silencioso.
- **Budget determinista**: el bucle se acota con un límite configurable (`max_iterations`) que eleva `BudgetExceeded` al excederse.
- **Separación output/control**: la prosa del modelo es output para el humano; la señal de control es el campo estructurado.

### Anti-patrón canónico

```python
DONE = ["task complete", "done", "listo"]
if any(p in text for p in DONE):
    return  # parsea prosa
```

Parsear prosa convierte una frase casual en halt silencioso a destiempo, o produce un bucle infinito cuando el modelo nunca pronuncia la frase. Depende del idioma, el tono y la redacción: es no determinista por construcción.

## Quality Signals

| Signal | Target |
|---|---|
| Enrutamiento por `stop_reason` | El halt depende del campo estructurado, no de texto |
| Manejo de stops inesperados | `max_tokens`/`pause_turn`/otros elevan error explícito |
| Budget | Límite configurable presente; eleva `BudgetExceeded` |
| Contrato de turno | `tool_result` regresa como `role=user` |
| Update safety | El trabajo manual existente se preserva |

## Open Knowledge

- Escenarios canónicos: Customer Support, Multi-Agent Research.
- Quiz de certificación: B · B · B. P3: limitar iteraciones con un budget configurable (`max_iterations`) y elevar `BudgetExceeded`.
