<!--
generated-by: scripts/scaffold-skill.py
generated-for: plan-mode-workflow
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Plan Mode Workflow Primary Prompt

## Objective

Diseñar e implementar el gate de dos modos para operar `{repo_or_domain}` con escritura bloqueada hasta firma del plan.

## Required Inputs

- Repo o dominio destino y su blast radius conocido.
- Lista de tools de escritura disponibles (Write, Edit, MultiEdit, NotebookEdit, MCP mutantes, Bash mutante).
- Mecanismo de aprobación esperado (quién firma, cómo se persiste el hash).
- Criterio de aceptación del cambio.

## Process

1. Arranca en `mode = "plan"`. Solo Read/Grep/Glob/Bash de inspección.
2. Explora y redacta `plan.md`: objetivo, archivos a tocar, orden, criterio de aceptación, riesgos.
3. Calcula el hash del plan y solicita firma (`approve_plan(hash, approver)`).
4. Implementa/activa el hook `PreToolUse` que deniega write-tools mientras `mode == "plan"`.
5. Solo tras firma del hash exacto, transición a `mode = "execute"` y aplica el diff.
6. Si el plan cambia, revierte a `plan` y re-pide firma.

## Output

Markdown con summary, evidence (plan + hash firmado), result (diff ejecutado), validation (checklist del gate) y risks.
