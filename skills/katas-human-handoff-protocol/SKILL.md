---
name: katas-human-handoff-protocol
version: 1.0.0
description: "Handoff a humano con payload tipado autocontenido (customer_id, issue_summary, actions_taken); end-state del bucle, no pausa."
owner: "JM Labs"
triggers:
  - human handoff
  - escalate to human
  - handoff payload
  - escalation protocol
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Human Handoff Protocol

## Qué es

Cuando el agente toca una política que no puede resolver por sí mismo (un límite excedido, una decisión irreversible o un conflicto de datos), invoca la tool `escalate_to_human`, suspende la generación de prosa y emite un payload JSON estricto y autocontenido. El payload contiene exactamente los campos que el operador humano necesita para decidir sin leer la conversación: `customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`.

El handoff es un **end-state del bucle**, no una pausa: el agente no continúa generando ni avanza hasta que el humano resuelve.

## Por qué importa (falla que evita)

Pasar al humano un transcript crudo es un desastre operacional: el operador tiene que leer toda la conversación, adivinar el contexto y decidir bajo presión. Un payload tipado y autocontenido reduce el tiempo de resolución y elimina la ambigüedad. El operador recibe un caso listo para actuar, no una conversación que descifrar.

## Modelo mental

- **Detectar la precondición de escalada**: límite excedido, irreversibilidad o conflicto de datos.
- Al cumplirse, llamar la tool `escalate_to_human` y **cortar la generación de texto**.
- El payload es **autocontenido**: el humano NO debe necesitar leer la conversación previa para decidir.
- Es un **end-state del bucle, no una pausa**: el agente no continúa hasta que el humano resuelve.
- El payload es **tipado**: campos fijos (`customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`), no prosa libre.

## Patrón correcto

```python
if refund_amount > tier2_limit:
    return tool_call('escalate_to_human', {
        'customer_id': customer_id,
        'issue_summary': issue_summary,
        'actions_taken': actions_taken,
        'escalation_reason': escalation_reason,
        'recommended_action': recommended_action,
    })
```

La llamada a la tool corta la generación: el agente no añade prosa después.

## Anti-patrón

```python
return 'Lo siento, ese reembolso supera mi límite. Voy a hablar con mi supervisor...'
# ...y sigue generando prosa, sin payload tipado, sin terminar el bucle
```

Devolver prosa tranquilizadora y continuar la conversación deja al operador sin un caso accionable y mantiene el bucle abierto cuando debía terminar.

## Argumento de certificación

- Enumerar las **precondiciones de escalada**: límite excedido, irreversibilidad, conflicto de datos.
- La **salida del handoff es tipada y autocontenida**: campos fijos, sin necesidad de leer la conversación previa.
- El handoff es **end-state, no pausa**: un hook `PostToolUse` puede terminar la sesión tras `escalate_to_human`.
- Conecta con `katas-hook-driven-policy-enforcement` (un hook puede forzar `ask_human`) y con `katas-numeric-cross-validation` (un mismatch numérico dispara el handoff).

## Cuándo activar

- El agente alcanza un límite de política que no puede resolver (p.ej. reembolso sobre el tope de su tier).
- La acción solicitada es irreversible y requiere aprobación humana.
- Hay un conflicto de datos que el agente no puede arbitrar.
- Se necesita diseñar el contrato del payload de escalada o el hook que cierra la sesión.

## Skills relacionadas

- `katas-hook-driven-policy-enforcement`
- `katas-numeric-cross-validation`
- `katas-mcp-structured-errors`
