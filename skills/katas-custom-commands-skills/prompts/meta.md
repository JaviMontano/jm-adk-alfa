<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-custom-commands-skills
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 24 · Meta Prompt · Slash Commands Custom y Skills

Revisa si `katas-custom-commands-skills` debe activarse, si el scope es seguro y qué agentes de soporte participan.

## Activation Check

- **Trigger match:** la tarea menciona slash commands custom, frontmatter de skills, `context: fork`, decidir command vs skill o scope project/user.
- **Domain fit:** la tarea trata de extender Claude Code, no de otra cosa.
- **Sufficient input:** se sabe qué se quiere extender y si debe replicarse al equipo.
- **No safer specialized skill:** no hay una skill más específica que cubra el caso.

## No activar cuando

- La tarea es ajena al dominio de extensión de Claude Code.
- El input está vacío.
- El requisito es contradictorio (p. ej. pide la skill pero exige ignorar validación y evidencia).
