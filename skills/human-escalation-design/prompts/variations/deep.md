<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design Deep Variation

Usar cuando hay multiples precondiciones de escalada, disparadores upstream (verificacion numerica, hooks `ask_human`), o el contrato de reanudacion no es trivial.

Incluye: discovery de todas las rutas que tocan limites o acciones irreversibles; opciones de contrato de payload consideradas; diseno del end-state (hook `PostToolUse` que termina la sesion); contrato de reanudacion tras resolucion humana; degraded mode cuando la tool no esta disponible; el test estructural; y los riesgos. Cierra con el bloque GOOD vs ANTI.
