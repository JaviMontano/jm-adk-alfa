# Prefix Caching (Kata 10)

> Convención de confiabilidad para JM-ADK. Reduce ~10x el costo de prompts grandes reusando el cache KV.

## Regla canónica

**Estático-prefix-first, dynamic-suffix-last.** La API de Claude reusa el cache KV cuando el prefijo del prompt es idéntico turno a turno. Si el primer ~90% del prompt es estable, se factura ~10% del costo.

| Zona | Contenido | Posición |
|------|-----------|----------|
| Estático (cacheable) | system prompt, CLAUDE.md, tool definitions, contexto pesado del repo | **arriba** |
| Dinámico (invalida cache) | input del usuario, timestamps, user_id, estado efímero | **abajo** |

El borde dinámico se aísla con tags XML (`<reminder>now: ...</reminder>`) para no contaminar el prefijo estable.

## Patrón

```python
messages = [
    {"role": "system",  "content": SYSTEM_PROMPT_BIG_AND_STABLE},  # estático
    {"role": "user",    "content": REPO_CONTEXT_BIG},              # estático
    *prior_turns,                                                  # estático
    {"role": "user",    "content": f"<reminder>now: {now}</reminder>\n{user_input}"},  # dinámico al final
]
resp = client.messages.create(
    system=[{"type": "text", "text": SYSTEM_PROMPT_BIG_AND_STABLE,
             "cache_control": {"type": "ephemeral"}}],
    messages=messages,
)
print(resp.usage)  # cache_read_input_tokens >> cache_creation_input_tokens
```

## Anti-patrón

```python
# Fecha al inicio del system prompt -> invalida cache en CADA llamada (10x más caro)
system_content = f"Today is {datetime.now()}\n" + SYSTEM_PROMPT_BIG_AND_STABLE
```

## Métrica

- `cache_creation_input_tokens`: tokens escritos al cache (primera vez / tras invalidación).
- `cache_read_input_tokens`: tokens leídos del cache (hit). Debe dominar en estado estacionario.
- Cambiar **un solo carácter** del prefijo invalida desde ese punto en adelante.

## Aplicación en JM-ADK

- `CLAUDE.md` + `PRISTINO.md` + tool/skill definitions son el prefijo estable → van primero, sin timestamps embebidos.
- Cualquier valor por-turno (hora, workspace-id efímero) va en un `<reminder>` al final del turno.
- Few-shot (Kata 14) va en la zona estática para reutilizar cache.
- El scratchpad (Kata 18) se lee una vez y se referencia, no se re-lee cada turno (preserva el prefijo).

Relacionado: `katas-prefix-caching`, `katas-fewshot-edge-calibration`, `katas-persistent-scratchpad`.
