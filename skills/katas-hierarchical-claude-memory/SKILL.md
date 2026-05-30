---
name: katas-hierarchical-claude-memory
version: 1.0.0
description: "Memoria jerarquica CLAUDE.md user/team/module con at-imports y precedencia por especificidad de subpath."
owner: "JM Labs"
triggers:
  - hierarchical memory
  - claude md memory
  - memory imports
  - memory precedence
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Hierarchical Claude Memory

## Qué es

`CLAUDE.md` es la memoria persistente del agente, organizada en tres niveles que cargan en cascada:

- `~/.claude/CLAUDE.md` — nivel **usuario** (preferencias personales, viven en el home, nunca en el repo).
- `<repo>/CLAUDE.md` — nivel **equipo** (convenciones compartidas, versionadas con el código).
- `<repo>/<subpath>/CLAUDE.md` — nivel **módulo** (reglas locales de un paquete o directorio).

Cada nivel se compone modularmente con `@imports` para mantener el archivo principal corto y caché-friendly. La regla más específica gana: `repo/src/CLAUDE.md` sobrescribe `repo/CLAUDE.md`, que a su vez se apila sobre `~/.claude/CLAUDE.md`.

## Por qué importa (falla que evita)

Repetir convenciones en cada prompt cuesta tokens y diverge entre miembros del equipo. Sin una fuente de verdad por nivel, el agente improvisa: cada sesión reinventa el estilo, los lints y las prohibiciones, y el equipo paga el costo en inconsistencia y retrabajo. Un `CLAUDE.md` monolítico de 2000 líneas con todo inline degrada la caché y dispersa la atención del modelo.

## Modelo mental

- **Más específico gana:** `repo/src/CLAUDE.md` sobrescribe `repo/CLAUDE.md`; la precedencia es subpath > repo > user para el scope del proyecto.
- **Frontera de privacidad:** lo personal (preferencias del usuario) NO va en el repo; va en el home (`~/.claude/CLAUDE.md`).
- **Modularidad con `@imports`:** mantienen el archivo principal corto y caché-friendly; cada sección importa archivos chicos en `docs/`.
- **Anti-monolito:** un `CLAUDE.md` de 2000 líneas con todo inline degrada caché y dispersa atención. Modularizar y separar por nivel es la cura.

## Patrón correcto

```text
# <repo>/CLAUDE.md  (nivel equipo, versionado)
## Style
@docs/style-guide.md

## Testing
@docs/testing-conventions.md

## Forbidden
- never run pip install without venv

# ~/.claude/CLAUDE.md  (nivel usuario, NO versionado)
- terse commits
- ruff over black
```

## Anti-patrón

```text
# <repo>/CLAUDE.md  (ANTI: monolítico + mezcla de niveles)
# 2000 líneas con TODO inline (style + testing + forbidden + ...)
# además incluye preferencias personales del autor:
- terse commits        # <- esto es del usuario, contamina el repo del equipo
- ruff over black      # <- diverge entre máquinas, no es convención de equipo
```

## Argumento de certificación

Separación estricta usuario/equipo/módulo en `CLAUDE.md` y uso de `@imports` para modularidad y caché-friendliness. El agente certifica cuando: las preferencias personales viven solo en el home, las convenciones de equipo en el repo, las reglas locales en el módulo, y el archivo principal se mantiene corto vía `@imports` en lugar de inline monolítico.

## Cuándo activar

- Diseñar o auditar la memoria persistente de un proyecto con `CLAUDE.md`.
- Decidir dónde colocar una convención (¿usuario, equipo o módulo?).
- Refactorizar un `CLAUDE.md` monolítico hacia `@imports` modulares.
- Resolver precedencia entre niveles que entran en conflicto.

## Skills relacionadas

- `katas-path-conditional-rules`
- `katas-context-cache-discipline`
- `katas-subagent-isolation`
