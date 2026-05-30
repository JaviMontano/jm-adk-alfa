---
name: katas-custom-commands-skills
version: 1.0.0
description: "Slash commands vs skills: context fork, allowed-tools whitelist y argument-hint; convenciones permanentes van en CLAUDE.md."
owner: "JM Labs"
triggers:
  - custom slash commands
  - skills frontmatter
  - context fork skill
  - command vs skill
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 24 · Slash Commands Custom y Skills

## Qué es

Claude Code extiende la sesión con dos mecanismos de extensión distintos. Los slash commands viven en `.claude/commands/X.md` y se disparan explícitamente escribiendo `/X`. Las skills viven en `.claude/skills/X/SKILL.md` y se activan on-demand cuando el modelo detecta que la metadata del frontmatter encaja con la tarea. El frontmatter de una skill declara su contrato operativo: `context: fork` aísla la ejecución en un sub-agente, `allowed-tools` define la whitelist de herramientas permitidas, y `argument-hint` documenta los argumentos esperados.

## Por qué importa (falla que evita)

Un command guardado en `~/.claude/commands/` no se replica al equipo: solo existe en la máquina personal de quien lo creó, así que el resto del equipo nunca lo recibe vía git. Una skill sin `context: fork` contamina la sesión principal con output verbose (un análisis exploratorio puede inyectar unos 5000 tokens de ruido en el contexto activo). Y una skill sin `allowed-tools` puede escribir o borrar archivos por accidente, porque nada limita las operaciones destructivas que tiene disponibles.

## Modelo mental

- Slash command = trigger explícito que el usuario invoca; skill = workflow on-demand con metadata que el modelo decide activar.
- Project scope (`.claude/`) viaja con git y llega a todo el equipo; user scope (`~/.claude/`) es personal y no se comparte.
- `context: fork` aísla la skill en un sub-agente → economía de contexto: el output verbose no contamina la sesión principal.
- `allowed-tools` es una whitelist que limita las operaciones destructivas por diseño (una skill exploratoria con `[Read, Grep, Glob]` no puede escribir ni ejecutar Bash).
- Las convenciones siempre-aplicables van en CLAUDE.md, no en una skill ni en un command: CLAUDE.md es para reglas permanentes, las skills para workflows on-demand.

## Patrón correcto

```
# .claude/skills/codebase-analysis/SKILL.md
---
name: codebase-analysis
description: "Mapea estructura y dependencias de un módulo o feature."
context: fork
allowed-tools: ["Read", "Grep", "Glob"]
argument-hint: "<dir-or-feature>"
---
# El body hace Glob -> Grep -> devuelve un resumen tipado.
# context:fork aísla los ~5000 tokens de exploración en un sub-agente.
# allowed-tools sin Write ni Bash impide mutaciones por accidente.
```

## Anti-patrón

```
# ~/.claude/skills/codebase-analysis/SKILL.md   (user scope: NO replica al equipo)
---
name: codebase-analysis
# sin context: fork  -> 5000 tokens contaminan la sesión principal
# sin allowed-tools  -> puede Write/Bash y borrar por accidente
---
```

## Argumento de certificación

- Escoger command vs skill según trigger (explícito vs on-demand) y scope (project vs user).
- Explicar el frontmatter: `context`, `allowed-tools` y `argument-hint`.
- Conectar `context: fork` con la economía de contexto (sub-agente aislado).
- Defender que las convenciones permanentes van en CLAUDE.md, no en una skill ni en un command.

## Cuándo activar

- El usuario pregunta por crear o versionar slash commands custom.
- Hay que decidir entre command y skill, o entre project scope y user scope.
- Se diseña el frontmatter de una skill (`context: fork`, `allowed-tools`, `argument-hint`).
- Se discute dónde ubicar convenciones permanentes del equipo.

## Skills relacionadas

- `katas-context-dilution-mitigation`
- `katas-prefix-caching`
- `katas-session-resume-fork`
