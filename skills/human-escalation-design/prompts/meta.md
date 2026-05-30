<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design Meta Prompt

Decide si `human-escalation-design` debe activarse, si el alcance es seguro y que agentes de apoyo participan.

## Activation Check

- Trigger match: la tarea pide disenar un handoff, payload de escalada o escalada a humano.
- Domain fit: existe una precondicion no resoluble por politica (limite, irreversibilidad, conflicto) que justifique un end-state.
- Sufficient input: se conoce el dominio, las politicas y la tool `escalate_to_human` (o su contrato a definir).
- No safer specialized skill: si el problema es de verificacion numerica o de hooks, usar la skill especifica y conectar el handoff como consecuencia.

## Routing

- Lead construye el handoff; support detecta precondiciones faltantes y fugas de prosa; guardian valida checklist y rechaza el anti-patron; specialist aporta el detalle de SDK (input schema de la tool, hook `PostToolUse` de end-state, contrato de reanudacion).
