---
name: context-window-engineering
version: 1.0.0
description: "Ingenieria de ventana de contexto: prefix caching estatico-first y mitigacion de dilucion softmax con edge placement y compactacion."
owner: "JM Labs"
triggers:
  - context window engineering
  - prefix cache optimization
  - context dilution
  - edge placement
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Context Window Engineering

## Capacidad

Capacidad de ingeniería para diseñar el ensamblado de la ventana de contexto de un agente de modo que (1) maximice el reuso de prefix cache (KV cache) y (2) minimice la pérdida de instrucciones por dilución softmax. Se logra organizando el contexto **estático-first / dinámico-last** —el prefijo estable se cachea y se reutiliza con factores cercanos a ~10x— y colocando lo que el modelo no puede olvidar en los **bordes** del contexto (apertura y cierre), donde la atención es más alta (curva en U). Cuando el contexto se acerca al límite, se aplica **compactación** por encima de un umbral fijo (>55%) para preservar las instrucciones de borde.

## Cuándo usarla

- Estás construyendo o tuneando un system prompt / context assembler de un agente de producción.
- El costo o la latencia de inferencia importan y quieres habilitar prefix caching real.
- Observas que el modelo "olvida" reglas críticas en conversaciones largas (síntoma de dilución).
- Inyectas estado por-turno (timestamps, contadores, recordatorios) y necesitas decidir dónde colocarlo.
- Vas a fijar una política de compactación / truncado para sesiones largas.

## Cómo construir

1. **Particiona el contexto en estático vs dinámico.** Identifica qué bloques no cambian entre turnos (rol, herramientas, políticas, esquema) y cuáles cambian cada turno (hora, estado, último mensaje).
2. **Ordena estático-first.** Coloca todo el bloque estático al inicio, byte-idéntico entre turnos, para que el prefijo sea cacheable. NUNCA pongas un valor por-turno (timestamp, request-id) en el prefijo: invalida el cache completo.
3. **Empuja lo dinámico al final.** Renderiza el estado volátil dentro de un bloque `<reminder>` al cierre del contexto, después del prefijo estable.
4. **Coloca reglas críticas en los bordes.** Las instrucciones que el modelo no debe olvidar van al inicio (parte del prefijo) y se reafirman al final (en el `<reminder>`), nunca enterradas en el centro de un bloque largo.
5. **Fija un umbral de compactación.** Define un porcentaje de ocupación (p. ej. >55%) a partir del cual se compacta/resume el historial intermedio, preservando intactos los bordes.
6. **Valida el cache y la retención.** Mide el cache-hit rate y verifica con una prueba de retención que la regla crítica sobrevive a un contexto largo.

## Patrón correcto

```python
# GOOD: estatico-first (cacheable), dinamico-last, reglas criticas en bordes
def build_context(turn_state: TurnState, history: list[Message]) -> list[Block]:
    static_prefix = [
        Block("role", ROLE_AND_TOOLS),           # estable byte a byte -> cacheable
        Block("policies", CRITICAL_RULES),       # regla critica en el borde inicial
        Block("schema", OUTPUT_SCHEMA),
    ]
    compacted = compact_if_over(history, threshold=0.55)  # umbral fijo
    dynamic_tail = [
        Block("reminder", render_reminder(
            now=turn_state.timestamp,             # volatil -> SOLO aqui, al final
            critical=CRITICAL_RULES_RESTATED,     # reafirma regla en borde final
        )),
    ]
    return static_prefix + compacted + dynamic_tail
```

## Anti-patrón

```python
# ANTI: timestamp al inicio invalida el cache; regla critica enterrada en el centro
def build_context(turn_state, history):
    return [
        Block("header", f"Current time: {turn_state.timestamp}"),  # rompe prefix cache
        Block("role", ROLE_AND_TOOLS),
        Block("history", history),                # regla critica queda sepultada aqui
        Block("rules", CRITICAL_RULES),           # zona de minima atencion (centro de la U)
    ]
    # Sin umbral de compactacion -> al crecer el historial, las reglas se diluyen.
```

## Checklist de validación

- ¿El prefijo es estable byte a byte, sin ningún valor por-turno (timestamp, request-id, contador)?
- ¿El estado dinámico vive en un bloque `<reminder>` al final del contexto?
- ¿Las reglas críticas están en los bordes (inicio + reafirmadas al final) y no en el centro?
- ¿Hay un umbral de compactación fijado y aplicado (>55% u otro valor explícito)?
- ¿Se midió el cache-hit rate y se probó la retención de la regla crítica en contexto largo?

## Paquete deterministico

- Usa `assets/context-assembly-schema.json` y `assets/context-policy.json` para declarar el ensamblado antes de escribir prompts o adapters.
- Ejecuta `scripts/compile-context-window.py <contexto.json> --output <reporte.md>` para generar un reporte reproducible de prefijo, zona compactable, cola dinamica, reglas criticas y validaciones.
- Ejecuta `bash skills/context-window-engineering/scripts/check.sh` antes de marcar la skill como lista.
- Rechaza timestamps en prefijo, reglas criticas solo en el centro, falta de compactacion, dynamic tail que no sea final y compactacion que toque bordes.

## Katas y skills relacionadas

- Katas: `katas-10`, `katas-11`.
- Relacionadas: `katas-prefix-caching`, `katas-context-dilution-mitigation`.
