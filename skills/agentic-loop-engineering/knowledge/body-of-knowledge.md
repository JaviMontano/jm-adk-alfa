# Agentic Loop Engineering Body of Knowledge

## Canon

El bucle de control es la máquina de estados que gobierna a un agente. Su única fuente de verdad para decidir entre continuar, detenerse o fallar debe ser una señal tipada (`stop_reason`), no el texto generado por el modelo.

### Conceptos clave

- **Loop de control (`while True`):** estructura que repite llamada-al-modelo → enrutado → acción hasta un halt o un fallo. No es un `for` sobre datos; es una máquina de estados sobre señales.
- **`stop_reason` tipado:** campo estructurado de la respuesta que codifica por qué el modelo se detuvo. Es el conmutador del loop. Valores típicos: `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`.
- **Dispatch de herramientas:** ante `tool_use`, cada bloque se enruta a su handler por nombre; un nombre desconocido debe fallar fuerte (`KeyError`/`raise`), no ignorarse.
- **Reinyección de `tool_result`:** el resultado de cada herramienta vuelve al historial como mensaje `user` con `tool_use_id` correlacionado al bloque que lo originó.
- **Budget duro:** techo configurable de iteraciones o tokens que dispara `BudgetExceeded`. Sin él, el loop puede no terminar nunca.
- **Fallo fuerte:** cualquier señal no contemplada hace `raise UnhandledStop`, dejando rastro, en lugar de un `break` o halt silencioso.

### Decisión de diseño

Control por señal estructurada frente a control por prosa. La prosa es ambigua (`"not done yet"` contiene `"done"`), no versionable y sensible al fraseo del modelo. La señal `stop_reason` es determinista, exhaustiva (se puede enumerar) y auditable. Toda lógica de halt/continuación vive sobre la señal.

## Quality Signals

| Señal | Objetivo |
|---|---|
| Control tipado | El halt/continuación depende de `stop_reason`, no de texto |
| Exhaustividad | Cada `stop_reason` posible tiene handler o `raise` |
| Budget | Existe techo configurable que dispara `BudgetExceeded` |
| Fallo fuerte | Las señales no contempladas hacen `raise`, no halts silenciosos |
| Correlación | Cada `tool_result` reinyecta con su `tool_use_id` |
| Observabilidad | Cada transición del loop queda instrumentada |

## Anti-patrón

Enrutar el control parseando prosa (`"done" in text`). Consecuencias: halt silencioso cuando el modelo nunca dice la palabra esperada, o bucle infinito sin budget. Es frágil ante reformulaciones y no auditable.

## Open Knowledge

- Budget por tokens usando el campo `usage` de la respuesta, además del techo de iteraciones.
- Manejo de `pause_turn` y transporte degradado (`Transport closed`).

## Deterministic package

La skill ahora incluye un contrato ejecutable para convertir decisiones de arquitectura del loop en artefactos verificables. `assets/loop-contract.schema.json` define campos requeridos, `assets/loop-policy.json` define acciones permitidas y anti-patrones bloqueados, y `scripts/compile-agentic-loop.py` genera codigo Python solo si el contrato cumple budget, stop handlers, reinyeccion de `tool_result`, fallos fuertes e instrumentacion.
