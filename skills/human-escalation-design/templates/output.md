<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design Output

## Summary

{summary: que precondiciones disparan el handoff y como queda el end-state}

## Evidence

{evidence: rutas del codigo que tocan limites/irreversibilidad/conflicto; tool escalate_to_human; marca supuestos}

## Result

{result: codigo del handoff con payload tipado autocontenido (customer_id, issue_summary, actions_taken, escalation_reason, recommended_action) y corte de generacion}

## Validation

- [ ] Precondiciones enumeradas como ramas explicitas.
- [ ] Payload autocontenido (humano resuelve sin leer la conversacion).
- [ ] Generacion cortada al invocar escalate_to_human.
- [ ] Handoff es end-state, no pausa.
- [ ] Test estructural: payload completo por rama + cero prosa de continuacion.

## Risks and Limits

{risks: degraded mode si la tool no esta disponible; contrato de reanudacion}
