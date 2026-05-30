<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Tool Use Design Primary Prompt

## Objective

Diseñar (o refactorizar) el tool surface de un agente para que el planner enrute sin ambigüedad: descripciones-contrato con frontera recíproca + estrategia `Grep → Read → Edit`.

## Required Inputs

- Lista de tools actuales (nombres + descripciones vigentes).
- Síntomas observados: el agente elige mal, pide aclaración, o satura contexto.
- Restricciones del runtime (SDK Anthropic, Claude Code, MCP) y archivos/repos sobre los que opera.
- Definition of done: cada par de tools que compite tiene frontera recíproca y el flujo de lectura evita el read-all.

## Process

1. **Inventaria** el tool surface y marca solapamientos (overloading).
2. **Reescribe** cada descripción como contrato: propósito, input format, 1–2 ejemplos, frontera recíproca.
3. **Resuelve** overloading con rename + split (no prosa).
4. **Documenta** el failure mode de Edit (anchor no único) + fallback Read+Write.
5. **Codifica** la estrategia `Grep → Read → Edit`; prohíbe `Glob("**/*") + Read all`.
6. **Valida** con el checklist.

## Output

Markdown con summary, evidence, result (bloque GOOD de descripciones-contrato), anti-pattern (bloque ANTI), validation checklist y risks.
