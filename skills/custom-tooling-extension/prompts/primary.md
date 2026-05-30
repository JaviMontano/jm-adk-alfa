<!--
generated-by: scripts/scaffold-skill.py
generated-for: custom-tooling-extension
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Custom Tooling Extension Primary Prompt

## Objective

Diseñar e implementar la extensión de Claude Code (slash command o skill) que el usuario necesita, con el artefacto, scope, `context: fork` y `allowed-tools` correctos.

## Required Inputs

- Qué debe hacer la extensión y cómo se dispara (¿el usuario la invoca a mano o se activa por contexto?).
- ¿Debe replicarse al equipo? (define scope project vs user).
- ¿Muta repo/sistema o es read-only? (define `allowed-tools`).
- Convenciones del proyecto ya existentes (para no incrustar lo permanente en la skill).

## Process

1. **Clasifica**: disparo explícito → slash command; activación contextual → skill con `context: fork`.
2. **Fija scope**: project (`.claude/` versionado) si replica al equipo; user solo para experimentos personales.
3. **Declara interfaz**: `description` como contrato de routing, `argument-hint` para la entrada.
4. **Acota herramientas**: `allowed-tools` whitelist mínima; read-only salvo justificación para `Bash`.
5. **Separa convención**: mueve reglas permanentes a `CLAUDE.md`, deja la capacidad condicional en la skill.
6. **Valida** contra el checklist y los evals (incluidos los negativos: user scope, sin fork, sin whitelist).

## Output

Devuelve la extensión más el reporte en este formato: Markdown con summary, evidence, result, validation y risks (ver `templates/output.md`).
