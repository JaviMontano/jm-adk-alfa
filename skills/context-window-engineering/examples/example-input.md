<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Tenemos un agente de soporte en producción. Cada turno construimos el contexto así:

```python
def build_context(turn_state, history):
    return [
        Block("header", f"Current time: {turn_state.timestamp}"),
        Block("role", ROLE_AND_TOOLS),
        Block("history", history),
        Block("rules", "Nunca cierres un ticket sin confirmacion del cliente."),
    ]
```

Síntomas: el cache-hit rate es casi cero (la latencia por turno es alta) y, en conversaciones largas, el agente cierra tickets sin confirmar. Rediseña el ensamblado para habilitar prefix caching y evitar que la regla crítica se diluya. El límite de contexto es de 200k tokens.
