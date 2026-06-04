---
name: custom-tooling-extension
version: 1.0.0
description: "Extender Claude Code con slash commands y skills usando context fork, allowed-tools whitelist y argument-hint, con scope correcto."
owner: "JM Labs"
triggers:
  - custom tooling extension
  - slash command authoring
  - skill frontmatter
  - context fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Custom Tooling Extension

## Capacidad

Diseñar e implementar extensiones de Claude Code de producción: slash commands (`.claude/commands/X.md`) y skills (con `context: fork`, `allowed-tools` y `argument-hint`), eligiendo el artefacto correcto y el scope correcto. La capacidad no es "escribir un archivo .md"; es decidir command vs skill por trigger y scope, economizar contexto con fork y blindar las operaciones destructivas con una whitelist de herramientas, sin contaminar la sesión ni romper la replicabilidad del equipo.

## Cuándo usarla

- Necesitas un disparador explícito que el usuario invoca por nombre (`/comando arg`): candidato a **slash command**.
- Necesitas que Claude active una capacidad por contexto/semántica, con su propia ventana y herramientas acotadas: candidato a **skill** con `context: fork`.
- El artefacto debe **replicarse a todo el equipo** vía repositorio: scope **project** (`.claude/commands/`, `.claude/skills/`), nunca user.
- Una skill ejecuta operaciones que pueden mutar el repo o el sistema y necesitas restringir el blast radius con `allowed-tools`.
- Quieres mover convenciones permanentes del proyecto (no condicionales) fuera de skills hacia `CLAUDE.md`.

## Cómo construir

1. **Clasifica el artefacto.** ¿Disparo explícito y predecible por el usuario? → command. ¿Activación por contexto + economía de ventana + herramientas acotadas? → skill con `context: fork`.
2. **Fija el scope.** Si debe replicarse al equipo, va a `.claude/` versionado (project). User scope solo para experimentos personales que NO deben llegar al repo de nadie más.
3. **Declara la interfaz.** En command/skill define `argument-hint` para que el invocante sepa qué pasar; en skill define `description` como contrato de routing.
4. **Aísla el contexto.** En skills de trabajo no trivial usa `context: fork` para que la sub-tarea no contamine ni infle la sesión principal.
5. **Whitelist de herramientas.** Declara `allowed-tools` con el mínimo necesario. Si la skill no muta nada, mantenla read-only (`Read, Grep, Glob`). Si necesita ejecutar, añade `Bash` explícitamente y documenta por qué.
6. **Separa convención de capacidad.** Reglas permanentes del proyecto → `CLAUDE.md`. La skill solo encapsula la capacidad condicional/invocable.
7. **Valida con katas y evals** antes de mergear (ver checklist).

## Patrón correcto

```yaml
# .claude/skills/release-notes/SKILL.md  (project scope, versionado)
---
name: release-notes
description: "Genera notas de versión desde git log entre dos tags; se activa al pedir changelog/release notes."
context: fork                 # GOOD: aísla y economiza la ventana principal
argument-hint: "<tag-desde> <tag-hasta>"
allowed-tools:               # GOOD: whitelist mínima; solo lectura + git
  - Read
  - Grep
  - Bash
---
```

```markdown
<!-- .claude/commands/deploy-check.md  (GOOD: disparo explícito, project scope) -->
---
argument-hint: "<env>"
---
Verifica readiness de deploy para $ARGUMENTS. Solo lectura.
```

## Anti-patrón

```yaml
# ANTI: user scope -> no se replica al equipo (cada quien tendría que recrearla)
# ~/.claude/skills/release-notes/SKILL.md

---
name: release-notes
# ANTI: sin context: fork -> la sub-tarea contamina e infla la sesión principal
# ANTI: sin allowed-tools -> ops destructivas sin whitelist (blast radius abierto)
description: "hace cosas con git"   # ANTI: description vaga, no es contrato de routing
---
# ANTI: la skill incrusta convenciones permanentes del proyecto
#       (esas reglas van en CLAUDE.md, no en una skill condicional)
```

## Checklist de validación

- ¿Elegiste **command vs skill** por trigger (explícito vs contextual) y por scope?
- ¿El scope es **project** si el artefacto debe replicarse al equipo? (user scope no replica)
- ¿Usaste `context: fork` para economía de contexto en skills de trabajo no trivial?
- ¿`allowed-tools` es una **whitelist mínima**? ¿Read-only salvo justificación explícita para `Bash`/mutaciones?
- ¿`description`/`argument-hint` funcionan como contrato de activación e interfaz?
- ¿Las **convenciones permanentes** viven en `CLAUDE.md` y NO dentro de la skill?

## Paquete deterministico

- Usa `assets/extension-schema.json` y `assets/extension-policy.json` para declarar la extension antes de escribir `.claude/commands/` o `.claude/skills/`.
- Ejecuta `scripts/compile-custom-tooling.py <extension.json> --output <plan.md>` para generar un plan reproducible con artefacto, scope, frontmatter, seguridad y validaciones.
- Ejecuta `bash skills/custom-tooling-extension/scripts/check.sh` antes de marcar la skill como lista.
- Rechaza artefactos de equipo en user scope, skills contextuales sin `context: fork`, herramientas irrestrictas, commands con trigger contextual y frontmatter sin interfaz clara.

## Katas y skills relacionadas

- Kata: `katas-custom-commands-skills`
- Relacionadas: `session-lifecycle-management`, `validation-retry-design`
