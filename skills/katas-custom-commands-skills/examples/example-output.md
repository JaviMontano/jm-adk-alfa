<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-custom-commands-skills
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Es una skill (activación on-demand), en project scope (`.claude/`) para que viaje con git al equipo, con `context: fork` (el análisis es verbose) y `allowed-tools` read-only.

## Patrón correcto (GOOD)

```
# .claude/skills/codebase-analysis/SKILL.md
---
name: codebase-analysis
description: "Mapea estructura y dependencias de un módulo o feature."
context: fork
allowed-tools: ["Read", "Grep", "Glob"]
argument-hint: "<dir-or-feature>"
---
# Body: Glob -> Grep -> resumen tipado.
```

## Anti-patrón (ANTI) — la propuesta del compañero

```
# ~/.claude/skills/codebase-analysis/SKILL.md   (user scope: NO replica al equipo)
---
name: codebase-analysis
# sin context: fork  -> ~5000 tokens contaminan la sesión principal
# sin allowed-tools  -> puede Write/Bash y borrar por accidente
---
```

## Validation

- Mecanismo correcto: skill on-demand, no command.
- Scope correcto: project (`.claude/`), no user (`~/.claude/`) que no replicaría.
- `context: fork` declarado: el output verbose queda aislado en sub-agente.
- `allowed-tools` mínimo (read-only): sin Write ni Bash, sin riesgo destructivo.
- Las convenciones siempre-aplicables del equipo, si las hubiera, irían en CLAUDE.md, no aquí.
