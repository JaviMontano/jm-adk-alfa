<!--
generated-by: scripts/scaffold-skill.py
generated-for: custom-tooling-extension
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Custom Tooling Extension Meta Prompt

Decide si `custom-tooling-extension` debe activarse, si el scope es seguro y qué agentes de soporte participan, antes de construir el command o la skill.

## Activation Check

- ¿El pedido es crear/revisar un slash command o una skill de Claude Code? (trigger match)
- ¿Encaja el dominio: artefacto, scope, `context: fork`, `allowed-tools`? (domain fit)
- ¿Hay input suficiente para clasificar command vs skill y fijar scope? Si no, pregunta.
- ¿Existe una skill especializada más segura para este caso concreto?

## Scope-Safety Gate

- Si el artefacto debe replicarse al equipo y se propone user scope → bloquear (no replica).
- Si la skill hace trabajo no trivial sin `context: fork` → marcar contaminación de sesión.
- Si ejecuta ops destructivas sin `allowed-tools` whitelist → bloquear por blast radius.
- Si incrusta convenciones permanentes que deberían ir en `CLAUDE.md` → corregir antes de seguir.
