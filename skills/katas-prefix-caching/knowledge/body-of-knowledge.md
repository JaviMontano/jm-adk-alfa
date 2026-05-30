<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching Body of Knowledge

## Canon

Conceptos clave de la kata Prefix Caching:

- **Cache KV reusable:** la API de Claude reusa el cache KV cuando el prefijo del prompt es idéntico turno a turno. Con el orden estático-primero / dinámico-último, el primer ~90% del prompt entra en cache y se factura ~10% del costo.
- **Estático vs dinámico:** estático = system prompt, `CLAUDE.md`, tool definitions, contexto pesado del repo. Dinámico = input del usuario, timestamps, `user_id`, estado efímero del turno.
- **Regla canónica:** estático arriba (prefix-first), dinámico abajo (suffix-last). El borde dinámico se aísla con tags XML como `<reminder>`.
- **Activación del cache:** marcar los bloques estables con `cache_control: {type: "ephemeral"}`.
- **Invalidación encadenada:** cambiar un solo carácter invalida el cache desde ese punto en adelante; lo volátil nunca puede preceder a lo estable.
- **Métrica de éxito:** `cache_creation_input_tokens` (escritura al cache) vs `cache_read_input_tokens` (lectura del cache, ~10x más barata) dentro de `usage`.

## Quality Signals

| Signal | Target |
|---|---|
| Orden del prompt | Estático en el prefijo, dinámico aislado en el sufijo (`<reminder>`) |
| Activación de cache | Bloques estables marcados con `cache_control: {type: "ephemeral"}` |
| Evidencia de ahorro | `cache_read_input_tokens` citado y comparado con `cache_creation_input_tokens` (~10x) |
| Update safety | Existing manual work is preserved |

## Anti-patrón canónico

```python
# Fecha al inicio invalida el cache en cada llamada
system_content = f"Today is {datetime.now()}..." + SYSTEM_PROMPT
```

Mismo contenido, 10x más caro, sin que el log lo evidencie. Cualquier dato dinámico (timestamp, `user_id`) ubicado antes del bloque estable produce esta fuga silenciosa de costo.

## Open Knowledge

- Escenarios de referencia: Customer Support y Developer Productivity con prompts grandes y estables reutilizados turno a turno.
