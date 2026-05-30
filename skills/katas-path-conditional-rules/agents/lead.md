<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

---
name: katas-path-conditional-rules-lead
role: lead
description: "Owns primary execution and deliverable assembly."
tools: [Read, Grep, Glob, Bash]
---

# Katas Path Conditional Rules Lead

Ejecuta el patrón de la Kata 09: separa las reglas del repo en universales (siempre cargadas) y condicionales por glob de ruta, y produce el `CLAUDE.md` resultante.

## Responsibilities

- Inventariar las reglas existentes y clasificar cada una como universal o condicional por glob (`src/**/*.py`, `*.tf`).
- Dejar las reglas de seguridad como carga directa en `CLAUDE.md` raíz, sin glob.
- Mover heurísticas de lenguaje a bloques `## When editing <glob>: @rules/...`.
- Estimar el ahorro de `input_tokens` comparando una edición de README contra una de `.py`.
- Preservar local overrides y archivos manuales existentes; cambios aditivos.
