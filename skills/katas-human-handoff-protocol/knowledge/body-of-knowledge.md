<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Human Handoff Protocol Body of Knowledge

## Canon

El handoff a humano es un end-state del bucle del agente. Cuando se cumple una precondición de escalada, el agente invoca `escalate_to_human`, suspende la generación de prosa y emite un payload JSON estricto y autocontenido.

### Conceptos clave

- **Precondiciones de escalada**: tres disparadores canónicos — límite excedido (p.ej. `refund_amount > tier2_limit`), decisión irreversible, conflicto de datos.
- **Payload tipado**: cinco campos fijos — `customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`. Sin prosa libre.
- **Autocontención**: el operador humano NO debe necesitar leer la conversación previa para decidir. El payload lleva todo el contexto.
- **End-state, no pausa**: el agente no continúa tras escalar. Un hook `PostToolUse` puede terminar la sesión después de `escalate_to_human`.
- **Corte de generación**: la llamada a la tool detiene la prosa; no hay texto tranquilizador posterior.

### Señales de calidad

| Señal | Target |
|---|---|
| Precondición detectada | La escalada se dispara por límite, irreversibilidad o conflicto, no por "no sé" genérico |
| Payload completo | Los cinco campos presentes y autocontenidos |
| End-state respetado | El bucle termina tras escalar; no hay prosa posterior |
| Sin transcript crudo | El humano recibe un caso accionable, no la conversación entera |

## Anti-patrón canónico

Devolver prosa ("Lo siento, ese reembolso supera mi límite. Voy a hablar con mi supervisor...") y seguir generando texto, sin payload tipado y sin terminar el bucle. Esto entrega al operador un transcript crudo que debe descifrar bajo presión, en vez de un caso listo para actuar.

## Conexiones

- `katas-hook-driven-policy-enforcement`: un hook puede forzar `ask_human` / `escalate_to_human`.
- `katas-numeric-cross-validation`: un mismatch numérico dispara el handoff.
- `katas-mcp-structured-errors`: misma filosofía de payload tipado para decisiones del agente.
