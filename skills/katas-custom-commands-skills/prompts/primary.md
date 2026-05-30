<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-custom-commands-skills
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 24 · Primary Prompt · Slash Commands Custom y Skills

## Objetivo

Aplicar el patrón correcto de extensión de Claude Code: decidir command vs skill, fijar el scope y diseñar el frontmatter de la skill.

## Inputs requeridos

- Qué se quiere extender (un workflow invocable, un análisis on-demand, una convención permanente).
- Si debe replicarse al equipo (project scope) o quedar personal (user scope).
- Si la extensión genera output verbose (candidata a `context: fork`).
- Qué herramientas necesita realmente (para fijar `allowed-tools` mínimo).

## Proceso

1. **Clasificar.** ¿Es trigger explícito (command), workflow on-demand (skill) o regla permanente (CLAUDE.md)?
2. **Fijar scope.** Si el equipo lo necesita → `.claude/`. Si es personal → `~/.claude/`.
3. **Diseñar frontmatter.** `name`, `description`, `context: fork` si es verbose, `allowed-tools` mínimo, `argument-hint`.
4. **Validar.** Confirmar que no se cayó en el anti-patrón (user scope que no replica, sin fork, sin allowed-tools) y que las convenciones permanentes quedaron en CLAUDE.md.

## Output

Markdown con summary, evidence, result, validation y risks. Incluir el bloque de frontmatter resultante.
