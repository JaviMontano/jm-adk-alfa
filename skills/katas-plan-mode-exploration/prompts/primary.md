<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Plan Mode Exploration Primary Prompt

## Objective

Operar de forma segura sobre un repositorio desconocido aplicando el contrato de dos modos: explorar en Plan Mode read-only, redactar `plan.md`, y transicionar a escritura solo tras firma humana.

## Required Inputs

- Repositorio o base de código objetivo (desconocido o crítico).
- Objetivo del cambio que se quiere proponer.
- Restricciones y convenciones conocidas.
- Mecanismo de aprobación humana disponible.

## Process

1. Configura el agente en modo seguro:
   `permission_mode="plan"`, `allowed_tools=["Read","Glob","Grep"]`,
   `system_prompt="En Plan Mode: explora, mapea, redacta plan.md. NO escribas código."`.
2. Registra un hook `PreToolUse` que, mientras `mode=="plan"`, deniegue las tools de escritura (`Write`, `Edit`, `NotebookEdit`, `Bash` con redirecciones).
3. Explora: mapea estructura, convenciones, dependencias y puntos de cambio.
4. Redacta `plan.md` con hallazgos y arquitectura propuesta.
5. Solicita firma humana. Solo entonces transiciona a un modo de escritura.
6. Si el plan cambia, vuelve a Plan Mode, actualiza `plan.md` y re-pide aprobación.

## Output

Markdown con summary, evidence, result, validation y risks. El artefacto central es `plan.md`, firmado por humano antes de cualquier escritura.
