<!--
generated-by: scripts/scaffold-skill.py
generated-for: custom-tooling-extension
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Custom Tooling Extension

Capacidad de ingeniería para extender Claude Code con **slash commands** y **skills** de producción: elegir command vs skill por trigger y scope, aislar la ventana con `context: fork`, restringir el blast radius con `allowed-tools` whitelist y exponer la interfaz con `argument-hint`. Mantiene las convenciones permanentes en `CLAUDE.md` y las capacidades condicionales en skills versionadas a nivel project para que se repliquen al equipo.

## Triggers

- custom tooling extension
- slash command authoring
- skill frontmatter
- context fork

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Úsala cuando vayas a crear o revisar un slash command o una skill de Claude Code y necesites decidir el artefacto, el scope (project para replicar al equipo), el uso de `context: fork` y la whitelist de `allowed-tools`. Read-only por defecto; `Bash` solo cuando la extensión deba ejecutar y esté justificado.

## Output Format

Markdown con summary, evidence, result, validation y risks (ver `templates/output.md`).
