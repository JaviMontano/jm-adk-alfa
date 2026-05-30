<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design Body of Knowledge

## Canon

El handoff a humano es el **end-state tipado** del bucle del agente, no una pausa conversacional. Cuando se toca una precondicion no resoluble por politica, el agente invoca `escalate_to_human`, corta la generacion de prosa y emite un payload JSON autocontenido. El operador humano resuelve leyendo solo el payload.

### Conceptos clave

- **Precondicion de escalada**: condicion enumerable que dispara el handoff: `limit_exceeded` (montos, tier), `irreversible_action` (borrado, transferencia), `data_conflict` (verificacion cruzada con `mismatch=true`).
- **Payload tipado autocontenido**: `customer_id`, `issue_summary`, `actions_taken[]`, `escalation_reason`, `recommended_action`. El humano NO necesita leer la conversacion previa.
- **End-state vs pausa**: el agente no continua tras el handoff; un hook `PostToolUse` puede terminar la sesion. No es un mensaje de cortesia que precede a mas texto.
- **Corte de generacion**: invocar la tool retorna el `tool_call` y termina el turno; no se emite prosa adicional.

## Decision de diseno

| Decision | Criterio |
|---|---|
| Que dispara handoff | Limite excedido, accion irreversible o conflicto de datos sin resolucion automatica |
| Que va en el payload | Solo lo necesario para resolver sin contexto externo: lo intentado + recomendacion |
| Cuando termina el bucle | Inmediatamente tras `escalate_to_human`; resolucion humana reanuda |
| Como se valida | Test estructural: payload completo por rama + cero prosa de continuacion |

## Quality Signals

| Signal | Target |
|---|---|
| Precondiciones | Enumeradas como ramas explicitas, no inferidas en prosa |
| Autocontencion | El operador resuelve sin leer el transcript |
| End-state | La generacion se corta; el bucle no continua hasta resolucion humana |
| Test estructural | Verifica payload completo y ausencia de prosa post-handoff |

## Anti-patron

Prosa de cortesia ("Lo siento, ese reembolso supera mi limite. Voy a hablar con mi supervisor...") seguida de mas generacion, sin payload tipado. Obliga al humano a leer todo el transcript y decidir bajo presion.

## Open Knowledge

- Contrato de reanudacion: como retoma el agente cuando el humano resuelve (resume vs fresh + summary).
- Degraded mode cuando la tool de escalada no esta disponible.
