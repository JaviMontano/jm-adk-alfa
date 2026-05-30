<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario: Customer Support. Un agente atiende tickets llamando a la API en un bucle y usando herramientas (consultar pedido, emitir reembolso). El bucle actual decide cuándo parar parseando la prosa del modelo:

```python
DONE = ["task complete", "done", "listo"]

while True:
    resp = create(messages=messages, tools=tools)
    text = resp.content[0].text if resp.content else ""
    if any(p in text for p in DONE):
        return resp
    dispatch(resp)
```

Problema observado: algunos tickets terminan a destiempo cuando el modelo menciona casualmente "task complete" dentro de una explicación; otros entran en bucle infinito porque el modelo nunca pronuncia ninguna frase de la lista. No hay límite de iteraciones.

Pedido: conviértelo en un bucle determinista basado en `stop_reason`, con manejo explícito de stops inesperados y un budget configurable.
