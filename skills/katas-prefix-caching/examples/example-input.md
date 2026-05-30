<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Developer Productivity: un agente de soporte de código se llama turno a turno con un system prompt grande y estable más el contexto del repo. El equipo reporta que la factura de tokens es 10x más alta de lo esperado, aunque el log no muestra errores. El prompt actual es:

```python
# ANTI: fecha al inicio invalida el cache cada llamada
system_content = f"Today is {datetime.now()} for user {user_id}.\n" + SYSTEM_PROMPT_BIG_AND_STABLE
messages = [
    {"role": "user", "content": REPO_CONTEXT_BIG},
    *prior_turns,
    {"role": "user", "content": user_input},
]
client.messages.create(system=system_content, messages=messages)
```

Pregunta: reorganiza el prompt para reusar el cache KV y explica cómo verificar el ahorro.
