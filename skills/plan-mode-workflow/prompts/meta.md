<!--
generated-by: scripts/scaffold-skill.py
generated-for: plan-mode-workflow
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Plan Mode Workflow Meta Prompt

Evalúa si `plan-mode-workflow` debe activarse, si el gate diseñado es inviolable y qué agentes de soporte participan.

## Activation Check

- ¿La tarea implica una primera escritura sobre un repo/dominio de blast radius desconocido?
- ¿Se exige aprobación auditable antes de mutar?
- ¿Hay riesgo de pisar trabajo compartido si se escribe sin plan?
- ¿No existe ya un gate más específico que cubra el caso?

## Safety Review

- ¿La escritura está deshabilitada por hook (no por convención) en `mode == "plan"`?
- ¿La firma referencia el hash exacto del plan?
- ¿Un cambio del plan revierte a `plan`?
- Rechaza si la configuración usa `bypassPermissions` o escribe antes de firmar.
