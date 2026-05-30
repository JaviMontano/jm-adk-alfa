<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Plan Mode Exploration

Kata 07 del kit JM-ADK. Exploración segura en Plan Mode read-only: el agente explora un repo desconocido sin permisos de escritura, redacta un `plan.md` con hallazgos y arquitectura propuesta, y solo transiciona a escritura tras la firma humana del plan. Evita la destrucción probabilística de soltar un agente con permisos de escritura sobre código desconocido.

## Triggers

- plan mode
- read-only exploration
- plan approval
- safe exploration

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill cuando vayas a operar sobre un repositorio desconocido o crítico y necesites explorar y proponer arquitectura antes de mutar nada. El patrón: `permission_mode="plan"` + `allowed_tools` solo de lectura (`Read`, `Glob`, `Grep`) + un hook `PreToolUse` que deniega herramientas de escritura mientras el modo sea plan. La salida es `plan.md`, que un humano firma antes de habilitar escritura.

## Output Format

Markdown con summary, evidence, result, validation y risks. El artefacto central es `plan.md` (hallazgos + arquitectura propuesta), auditable y firmado por humano.
