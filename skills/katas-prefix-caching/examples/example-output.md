<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El `datetime.now()` y el `user_id` estaban al inicio del `system`, invalidando el cache KV en cada llamada. Se mueven al final del prompt, aislados en un tag `<reminder>`, y se marca el bloque estable con `cache_control: {type: "ephemeral"}`.

## Result (GOOD)

```python
messages = [
    {"role": "user", "content": REPO_CONTEXT_BIG},
    *prior_turns,
    {"role": "user", "content": f"<reminder>now: {datetime.now()} · user: {user_id}</reminder>\n{user_input}"},
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

## Evidence

- Antes: cada llamada reportaba `cache_creation_input_tokens` alto y `cache_read_input_tokens = 0` (cache nunca reusado).
- Después: a partir de la segunda llamada `cache_read_input_tokens` cubre ~90% del prefijo, facturado a ~10% del costo.

## Validation

- Ningún valor dinámico (timestamp, `user_id`) precede al bloque estable.
- El borde dinámico está aislado en `<reminder>` al final.
- Un cambio de un carácter en el sufijo ya no invalida el prefijo cacheado.
- Riesgos: si `SYSTEM_PROMPT_BIG_AND_STABLE` se edita entre despliegues, el cache se reconstruye una vez (esperado).
