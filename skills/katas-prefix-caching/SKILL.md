---
name: katas-prefix-caching
version: 1.0.0
description: "Prefix caching: estatico-first y dinamico-last; interpretar cache_creation vs cache_read input tokens para estimar ahorro."
owner: "JM Labs"
triggers:
  - prefix caching
  - kv cache
  - cache control
  - static prefix
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Prefix Caching

## Qué es

La API de Claude reusa el cache KV cuando el prefijo del prompt es idéntico turno a turno. Si organizas el contexto como estático primero y dinámico al final, el primer ~90% del prompt entra en cache y se factura ~10% del costo. El cache se activa marcando los bloques estables con `cache_control: {type: "ephemeral"}`, y la métrica de éxito vive en `usage`: `cache_creation_input_tokens` (lo que se escribió al cache) frente a `cache_read_input_tokens` (lo que se leyó del cache, ~10x más barato).

## Por qué importa (falla que evita)

Insertar la fecha actual o un `user_id` al inicio del prompt invalida el cache en cada llamada. El contenido es el mismo, pero el costo se multiplica por 10 sin que el log de la aplicación lo evidencie: no hay error, no hay excepción, solo una factura silenciosamente inflada. Es una fuga de costo invisible que solo se detecta auditando los `usage` tokens.

## Modelo mental

- **Estático** = system prompt, `CLAUDE.md`, tool definitions, contexto pesado del repo. Va arriba.
- **Dinámico** = input del usuario, timestamps, estado efímero del turno. Va abajo.
- **Regla:** estático arriba (prefix-first), dinámico abajo (suffix-last).
- El borde dinámico se aísla con tags XML: `<reminder>now: ...</reminder>`.
- **Invalidación encadenada:** cambiar UN solo carácter invalida el cache desde ese punto en adelante; por eso lo volátil nunca puede ir antes de lo estable.
- **Métrica:** comparar `cache_creation_input_tokens` vs `cache_read_input_tokens` en `usage` para estimar el ahorro (~10x en lecturas).

## Patrón correcto

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT_BIG_AND_STABLE},
    {"role": "user", "content": REPO_CONTEXT_BIG},
    *prior_turns,
    {"role": "user", "content": f"<reminder>now: {now}</reminder>\n{user_input}"},
]

client.messages.create(
    system=[{
        "type": "text",
        "text": SYSTEM_PROMPT_BIG_AND_STABLE,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=messages,
)
```

## Anti-patrón

```python
# ANTI: fecha al inicio invalida el cache en cada llamada
system_content = f"Today is {datetime.now()}..." + SYSTEM_PROMPT
```

El timestamp al frente reescribe el prefijo cada turno: mismo contenido, 10x más caro.

## Argumento de certificación

Para certificar esta kata hay que: enunciar la regla "estático-prefix-first, dynamic-suffix-last"; y saber interpretar `cache_creation_input_tokens` vs `cache_read_input_tokens` en `usage` para estimar el ahorro (~10x). Quien certifica explica por qué un valor dinámico al inicio (timestamp, `user_id`) rompe el prefix caching, por qué cambiar un carácter invalida desde ese punto en adelante, y dónde se ubica el dato dinámico (al final, aislado en un tag `<reminder>`).

## Cuándo activar

Activa esta skill cuando el trabajo toque organización del prompt para reuso de cache KV, `cache_control` ephemeral, prefijo estático vs sufijo dinámico, o interpretación de los tokens de cache en `usage`. Escenarios típicos: Customer Support y Developer Productivity con prompts grandes y estables reutilizados turno a turno.

## Skills relacionadas

- `katas-context-dilution-mitigation`
- `katas-persistent-scratchpad`
- `katas-multipass-prompt-chaining`
