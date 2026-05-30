<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-custom-commands-skills
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 24 · Slash Commands Custom y Skills

Slash commands (`.claude/commands/X.md`, trigger `/X`) y skills (`.claude/skills/X/SKILL.md`, on-demand con frontmatter) son los dos mecanismos de extensión de Claude Code. La skill enseña a escoger entre ambos, a diseñar el frontmatter (`context: fork`, `allowed-tools`, `argument-hint`) y a recordar que las convenciones permanentes van en CLAUDE.md, no en una skill ni en un command. Project scope (`.claude/`) viaja con git; user scope (`~/.claude/`) es personal y no replica al equipo.

## Triggers

- custom slash commands
- skills frontmatter
- context fork skill
- command vs skill

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando haya que decidir command vs skill, definir scope (project vs user), diseñar el frontmatter de una skill o ubicar convenciones permanentes del equipo. Regla rápida: `context: fork` aísla en sub-agente y ahorra contexto; `allowed-tools` limita operaciones destructivas; las convenciones siempre-aplicables van en CLAUDE.md.

## Output Format

Markdown con summary, evidence, result, validation y risks.
