<!--
generated-by: scripts/scaffold-skill.py
generated-for: human-escalation-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Human Escalation Design

Capacidad construible para disenar el handoff a un humano como end-state tipado del bucle del agente: ante una precondicion no resoluble (limite, irreversibilidad, conflicto) se invoca `escalate_to_human`, se corta la generacion y se emite un payload JSON autocontenido. El humano resuelve sin leer la conversacion.

## Resumen ejecutivo

- Problema: pasar al humano un transcript crudo es desastre operacional; el operador adivina contexto y decide bajo presion.
- Solucion: payload tipado (`customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`) que reduce tiempo de resolucion y elimina ambiguedad.
- Invariante: el handoff es end-state, no una pausa; el agente no continua hasta resolucion humana.

## Triggers

- human escalation design
- typed handoff
- escalation payload
- escalate to human

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Usa esta skill cuando el diseno requiera convertir una situacion de escalada en un handoff tipado: enumera precondiciones, define el contrato del payload, corta la generacion al invocar la tool y valida con un test estructural. Ver `SKILL.md` para los pasos de construccion y el bloque GOOD vs ANTI.

## Output Format

Markdown con summary, evidence, result (codigo del handoff), validation y risks.
