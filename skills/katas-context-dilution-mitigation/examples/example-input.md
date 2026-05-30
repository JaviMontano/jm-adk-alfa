<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Tengo un agente de soporte al cliente que funciona en conversaciones largas. El system prompt es así:

```python
system_prompt = f"You are a support assistant.\n{big_blob_of_context}\nIMPORTANT: never expose customer PII.\n...3000 more tokens of FAQ and tone guidance..."
```

El problema: el agente respeta la regla de PII en los primeros turnos, pero hacia el turno 30 a veces filtra datos del cliente. No hay error ni log; solo el comportamiento cambia. Aplica `katas-context-dilution-mitigation` para corregir el prompt y la gestión de contexto.
