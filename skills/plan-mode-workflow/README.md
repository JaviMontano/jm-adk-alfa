<!--
generated-by: scripts/scaffold-skill.py
generated-for: plan-mode-workflow
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Plan Mode Workflow

Capacidad de ingeniería para operar repos o dominios desconocidos en dos modos: un Plan Mode read-only que solo lee y produce un `plan.md`, y un Execute Mode que se habilita únicamente tras una aprobación firmada del hash exacto del plan. La transición la aplica un hook `PreToolUse` que bloquea las tools de escritura mientras el modo sea `plan` — no se confía en la disciplina del modelo.

## Resumen ejecutivo

El valor no está en "pedir permiso" sino en hacer el gate **inviolable por construcción**: el modo es estado, la firma es un artefacto auditable (hash + aprobador + timestamp), y cualquier edición posterior del plan revierte a `plan` y re-exige firma. El plan firmado más el diff resultante son el rastro de auditoría de qué se autorizó y qué se ejecutó.

## Triggers

- plan mode workflow
- read-only exploration
- plan approval gate
- two-mode operation

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Usa esta skill cuando vas a tocar por primera vez un repo de blast radius desconocido, cuando se exige aprobación auditable antes de mutar, o cuando un write prematuro puede pisar trabajo compartido. Arranca en Plan Mode, redacta `plan.md`, fírmalo por hash, y solo entonces ejecuta.

## Output Format

Markdown con summary, evidence (plan firmado + hash), result (diff ejecutado), validation (checklist del gate) y risks.
