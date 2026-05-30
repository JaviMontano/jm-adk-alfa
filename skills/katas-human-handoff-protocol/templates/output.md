<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-human-handoff-protocol
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Human Handoff Protocol Output

## Precondición de escalada

{precondicion}  <!-- límite excedido | irreversibilidad | conflicto de datos -->

## Payload de handoff

```json
{
  "customer_id": "{customer_id}",
  "issue_summary": "{issue_summary}",
  "actions_taken": [{actions_taken}],
  "escalation_reason": "{escalation_reason}",
  "recommended_action": "{recommended_action}"
}
```

## Validación del contrato

- [ ] Precondición de escalada identificada y declarada.
- [ ] Los cinco campos del payload presentes.
- [ ] Payload autocontenido: el humano no necesita leer la conversación.
- [ ] Generación de prosa cortada tras `escalate_to_human`.
- [ ] End-state: el bucle termina; no hay continuación automática.

## Riesgos y límites

{risks}
