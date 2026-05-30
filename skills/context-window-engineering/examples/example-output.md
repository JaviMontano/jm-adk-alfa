<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El diseño original tenía dos defectos acoplados: el `timestamp` al inicio invalidaba el prefix cache en cada turno, y la regla crítica quedaba sepultada tras el historial (zona de mínima atención). Se reordena a estático-first / dinámico-last, con la regla crítica en ambos bordes y un umbral de compactación al 55%.

## Anti-patrón (lo que había)

```python
# ANTI
def build_context(turn_state, history):
    return [
        Block("header", f"Current time: {turn_state.timestamp}"),  # rompe el cache cada turno
        Block("role", ROLE_AND_TOOLS),
        Block("history", history),
        Block("rules", "Nunca cierres un ticket sin confirmacion del cliente."),  # enterrada
    ]
```

## Patrón correcto (GOOD)

```python
def build_context(turn_state: TurnState, history: list[Message]) -> list[Block]:
    static_prefix = [
        Block("role", ROLE_AND_TOOLS),                       # byte-identico -> cacheable
        Block("policies", "Nunca cierres un ticket sin confirmacion del cliente."),  # borde inicial
        Block("schema", OUTPUT_SCHEMA),
    ]
    compacted = compact_if_over(history, threshold=0.55)     # preserva los bordes
    dynamic_tail = [
        Block("reminder", render_reminder(
            now=turn_state.timestamp,                        # volatil -> solo aqui, al final
            critical="Recuerda: NO cierres tickets sin confirmacion del cliente.",  # borde final
        )),
    ]
    return static_prefix + compacted + dynamic_tail
```

## Evidence

- Cache-hit esperado: el prefijo (`role` + `policies` + `schema`) ahora es byte-idéntico entre turnos, habilitando cache-read en lugar de cache-write tras el primer turno.
- Prueba de retención: en una sesión sintética de >150k tokens, la regla aparece en ambos bordes y es reafirmada en cada turno por el `<reminder>`.

## Validation

- [x] Prefijo byte-idéntico, sin valores por-turno (el timestamp se movió al `<reminder>`).
- [x] Estado dinámico solo en el `<reminder>` final.
- [x] Regla crítica en bordes (inicio + reafirmada al final).
- [x] Umbral de compactación fijado (>55%).
- [x] Cache-hit + retención validados.

## Risks and Limits

- Si el tokenizer o el cliente cambian el render del prefijo, el cache se invalida: mantener el prefijo estable es responsabilidad continua.
- La compactación debe resumir solo el historial intermedio; nunca tocar los bloques de borde.
