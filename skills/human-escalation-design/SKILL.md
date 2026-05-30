---
name: human-escalation-design
version: 1.0.0
description: "Disenar handoff tipado a humano como end-state del bucle con payload autocontenido; no prosa de escalada."
owner: "JM Labs"
triggers:
  - human escalation design
  - typed handoff
  - escalation payload
  - escalate to human
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Human Escalation Design

## Capacidad

Capacidad de ingenieria para disenar el handoff a un humano como **end-state tipado del bucle del agente**, no como una pausa conversacional. Cuando el agente toca una precondicion que no puede resolver por politica (limite excedido, decision irreversible, conflicto de datos), invoca la tool `escalate_to_human`, **corta la generacion de prosa** y emite un payload JSON autocontenido (`customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`). El operador humano resuelve leyendo solo el payload: nunca necesita reconstruir la conversacion previa.

## Cuando usarla

- Hay precondiciones de escalada enumerables: limite excedido (montos, tier), accion irreversible (borrado, transferencia), o conflicto de datos sin resolucion automatica.
- El operador humano debe decidir bajo presion y no puede leer un transcript crudo.
- El bucle del agente debe detenerse hasta que un humano resuelva (no es un mensaje de cortesia que precede a mas generacion).
- Conecta con verificacion numerica (un `mismatch=true` dispara handoff) y con hooks que fuerzan `ask_human`.

## Como construir

1. **Enumera precondiciones** de escalada en codigo, no en prosa: `limit_exceeded`, `irreversible_action`, `data_conflict`. Cada una es una rama explicita.
2. **Define el contrato del payload** como tipo estricto: `customer_id`, `issue_summary`, `actions_taken[]`, `escalation_reason`, `recommended_action`. Sin campos libres que obliguen a leer la conversacion.
3. **Invoca la tool y corta generacion**: el handoff retorna el `tool_call` y termina el turno. No se emite prosa adicional tras la llamada.
4. **Haz el payload autocontenido**: incluye lo ya intentado (`actions_taken`) y una recomendacion accionable, de modo que el humano resuelva sin contexto externo.
5. **Trata el handoff como end-state**: un hook `PostToolUse` puede terminar la sesion tras `escalate_to_human`; el agente no continua hasta resolucion humana.
6. **Valida estructuralmente**: un test verifica que toda rama de escalada produce payload completo y que ninguna emite prosa de continuacion.

## Patron correcto

```python
def handle_refund(ctx, refund_amount):
    if refund_amount > ctx.tier2_limit:
        return tool_call("escalate_to_human", {
            "customer_id": ctx.customer_id,
            "issue_summary": f"Refund {refund_amount} exceeds tier2 limit {ctx.tier2_limit}",
            "actions_taken": ctx.actions_taken,          # autocontenido
            "escalation_reason": "limit_exceeded",
            "recommended_action": "Approve manually or deny with policy 4.2",
        })  # end-state: el turno termina aqui, no se genera mas prosa
    return process_refund(ctx, refund_amount)
```

## Anti-patron

```python
# ANTI: prosa de cortesia + sigue generando, sin payload tipado
def handle_refund(ctx, refund_amount):
    if refund_amount > ctx.tier2_limit:
        say("Lo siento, ese reembolso supera mi limite. Voy a hablar con mi supervisor...")
        # el agente continua generando texto; el humano debe leer todo el transcript
    return keep_going(ctx)
```

## Checklist de validacion

- Precondiciones de escalada enumeradas (limite / irreversible / conflicto) como ramas explicitas.
- Payload autocontenido: el humano resuelve sin leer la conversacion previa.
- La generacion de prosa se corta al invocar `escalate_to_human`.
- El handoff es end-state del bucle, no una pausa que precede a mas texto.
- Existe test estructural que verifica payload completo por rama y ausencia de prosa de continuacion.

## Katas y skills relacionadas

- Kata 16. Relacionadas: `katas-human-handoff-protocol`.
- Conecta con `cross-validation-numeric-design` (mismatch dispara handoff) y con `hook-driven-ask-human`.
