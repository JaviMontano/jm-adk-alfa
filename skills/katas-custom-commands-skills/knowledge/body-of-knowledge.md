<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-custom-commands-skills
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 24 · Body of Knowledge · Slash Commands Custom y Skills

## Canon

Claude Code ofrece dos mecanismos de extensión que NO son intercambiables:

- **Slash command** — archivo `.claude/commands/X.md`. Trigger explícito: el usuario escribe `/X`. Útil cuando el usuario quiere invocar un workflow a voluntad.
- **Skill** — directorio `.claude/skills/X/SKILL.md` con frontmatter. Activación on-demand: el modelo la elige cuando la metadata encaja con la tarea.

**Scope** determina la replicación:

- Project scope (`.claude/`) viaja con git → llega a todo el equipo.
- User scope (`~/.claude/`) es personal → NO se comparte ni replica.

**Frontmatter de skill** (contrato operativo):

- `context: fork` — aísla la ejecución en un sub-agente. El output verbose queda fuera de la sesión principal → economía de contexto.
- `allowed-tools` — whitelist de herramientas. Limita operaciones destructivas por diseño (p. ej. `["Read", "Grep", "Glob"]` impide Write y Bash).
- `argument-hint` — documenta los argumentos esperados (p. ej. `"<dir-or-feature>"`).

**Regla de ubicación:** las convenciones siempre-aplicables van en CLAUDE.md (reglas permanentes), no en una skill ni en un command (workflows on-demand / triggers explícitos).

## Quality Signals

| Signal | Target |
|---|---|
| Scope correcto | Lo que el equipo necesita compartir vive en project scope (`.claude/`), no en `~/.claude/` |
| Aislamiento de contexto | Skills exploratorias verbose declaran `context: fork` |
| Seguridad por whitelist | Toda skill declara `allowed-tools` con el mínimo necesario |
| Ubicación de convenciones | Reglas permanentes en CLAUDE.md, no en skills ni commands |

## Anti-patrón canónico

Una skill en `~/.claude/skills/...` (user scope, no replica al equipo), sin `context: fork` (los ~5000 tokens de exploración contaminan la sesión principal) y sin `allowed-tools` (puede Write/Bash y borrar por accidente). Tres fallas a la vez: no se comparte, contamina el contexto y es insegura.

## Quiz canónico (B·B·C)

- **P1 (B):** un slash command de cobertura de tests para el equipo va en `.claude/commands/test-coverage.md`, versionado en project scope.
- **P2 (B):** la skill de análisis declara `context: fork` + `allowed-tools: [Read, Grep, Glob]`.
- **P3 (C):** las convenciones siempre-aplicables van en CLAUDE.md, no en una skill ni en un command.
