<!--
generated-by: scripts/scaffold-skill.py
generated-for: custom-tooling-extension
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Artefacto: **skill** (activación contextual, no disparo fijo). Scope: **project** (`.claude/skills/release-notes/`, versionado) para que se replique al equipo y se deje de usar la versión personal de `~/.claude`.

## Evidence

- Trigger contextual ("genera el changelog") → skill con `description` como contrato de routing, no slash command.
- "Replicar al equipo" → scope project; la versión en `~/.claude` (user scope) no se replica y se descarta.
- "Que no infle la sesión" → `context: fork`.
- "Que no pueda borrar nada" → `allowed-tools: [Read, Grep, Bash]` (lectura + git read-only), sin permisos destructivos abiertos.

## Result — GOOD

```yaml
# .claude/skills/release-notes/SKILL.md  (project scope, versionado)
---
name: release-notes
description: "Genera notas de versión desde git log entre dos tags; se activa al pedir changelog/release notes."
context: fork
argument-hint: "<tag-desde> <tag-hasta>"
allowed-tools:
  - Read
  - Grep
  - Bash
---
```

## Anti-pattern — ANTI

```yaml
# ~/.claude/skills/release-notes/SKILL.md
---
name: release-notes
# ANTI: user scope -> no se replica al equipo
# ANTI: sin context: fork -> contamina la sesión principal
# ANTI: sin allowed-tools -> blast radius abierto a ops destructivas
description: "hace cosas con git"   # ANTI: vaga, no es contrato de routing
---
```

## Validation

- Artefacto correcto: skill por activación contextual.
- Scope correcto: project, no la versión personal en user scope.
- `context: fork` presente.
- `allowed-tools` whitelist mínima read-only + git.
- Convenciones permanentes del repo (no condicionales) quedaron en `CLAUDE.md`, fuera de la skill.

## Risks and Limits

- `Bash` habilitado para git; documentar que se usa solo lectura. Supuesto: el repo tiene tags válidos entre los que diferenciar.
