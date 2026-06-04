# Custom Tooling Extension Body of Knowledge

## Canon de la capacidad

Extender Claude Code es **diseñar el artefacto correcto con el scope correcto**, no escribir un `.md`. Dos artefactos:

- **Slash command** (`.claude/commands/X.md`): disparo explícito por el usuario (`/X arg`). Usa `$ARGUMENTS` y `argument-hint`. Bueno para acciones predecibles e invocadas a mano.
- **Skill** (`SKILL.md` con frontmatter): activación por contexto/semántica vía `description` (el contrato de routing). Soporta `context: fork` (ventana aislada), `allowed-tools` (whitelist) y `argument-hint`.

Conceptos clave:

- **Scope project vs user.** Project (`.claude/` versionado) se replica al equipo. User (`~/.claude/`) es personal y NO replica. Si el artefacto debe compartirse, va a project.
- **context: fork.** Aísla la sub-tarea en su propia ventana: economía de contexto y cero contaminación de la sesión principal. Obligatorio en skills de trabajo no trivial.
- **allowed-tools como whitelist.** Restringe el blast radius. Read-only por defecto (`Read, Grep, Glob`); `Bash`/mutaciones solo con justificación.
- **CLAUDE.md vs skill.** Convenciones permanentes (siempre activas) → `CLAUDE.md`. Capacidades condicionales/invocables → skill.

## Decisión de diseño

| Pregunta | Si SÍ | Si NO |
|---|---|---|
| ¿Disparo explícito por el usuario? | slash command | skill |
| ¿Debe replicarse al equipo? | scope project | user scope (solo personal) |
| ¿Trabajo no trivial / muchos tokens? | `context: fork` | fork opcional |
| ¿Muta repo o sistema? | `allowed-tools` con `Bash` + justificación | read-only whitelist |
| ¿Regla siempre activa del proyecto? | va a `CLAUDE.md` | puede ir en la skill |

## Señales de calidad

| Señal | Target |
|---|---|
| Artefacto correcto | command para disparo explícito; skill para activación contextual |
| Scope correcto | project si debe replicarse; user solo para experimentos personales |
| Economía de contexto | `context: fork` en skills de trabajo no trivial |
| Blast radius acotado | `allowed-tools` whitelist mínima; read-only salvo justificación |
| Separación de responsabilidades | convenciones permanentes en `CLAUDE.md`, no en la skill |

## Anti-patrón canónico

- **User scope** cuando el artefacto debe replicarse al equipo → no replica, cada quien lo recrea.
- **Skill sin `context: fork`** → contamina e infla la sesión principal.
- **Skill sin `allowed-tools`** ejecutando ops destructivas → blast radius abierto.
- **Convenciones permanentes incrustadas en la skill** en vez de `CLAUDE.md`.
- **`description` vaga** que no funciona como contrato de routing.
