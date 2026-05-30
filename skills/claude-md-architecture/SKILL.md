---
name: claude-md-architecture
version: 1.0.0
description: "Estructurar memoria jerarquica CLAUDE.md user/team/module con at-imports y reglas condicionales por glob de ruta."
owner: "JM Labs"
triggers:
  - claude md architecture
  - hierarchical memory
  - path scoped rules
  - memory imports
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Claude Md Architecture

## Capacidad

Diseñar la memoria persistente de un proyecto Claude Code como una jerarquía explícita de archivos `CLAUDE.md` en tres niveles (user, team, module), conectados por `@imports` y complementados con reglas condicionales por glob de ruta. El objetivo de ingeniería es que las reglas universales estén siempre presentes en el prefijo cacheable, mientras que las heurísticas específicas de un subárbol se carguen solo cuando el trabajo toca ese subárbol. El resultado en producción es una memoria que no crece sin control, que respeta la precedencia por subpath y que mantiene la economía de contexto (cache KV) en cada turno.

## Cuándo usarla

- El `CLAUDE.md` del repo superó ~300 líneas y empieza a cargar reglas que solo aplican a un módulo.
- Hay reglas que deben aplicar solo a `frontend/**`, `infra/**` o `tests/**`, y hoy viven en un único archivo global.
- Las preferencias personales (tono, atajos individuales) están filtrándose al repo de equipo.
- Se necesita separar lo que es política de equipo (versionada) de lo que es preferencia de usuario (no versionada) de lo que es contrato de módulo.

## Cómo construir

1. Inventaría las reglas actuales y clasifícalas en tres cubos: universal (siempre), por-módulo (subárbol concreto), por-usuario (preferencia personal no versionada).
2. Crea el `CLAUDE.md` raíz de equipo solo con universales más un bloque de `@imports` hacia los módulos. Mantén el raíz lean y estable: es el prefijo que se cachea.
3. Por cada módulo con reglas propias, crea `module/CLAUDE.md` con reglas activadas por glob (p. ej. `apply to: "src/api/**"`), no copiadas al raíz.
4. Mueve las preferencias personales a `~/.claude/CLAUDE.md` (user scope) e impórtalas con `@import`; nunca al repo del equipo.
5. Define la precedencia: la regla más específica por subpath gana; documenta el orden de resolución para que sea predecible.
6. Verifica que el prefijo (raíz + imports universales) no contenga valores por-turno ni reglas que solo apliquen a un subárbol.

## Patrón correcto

```markdown
# team CLAUDE.md (versioned, stable prefix)
@import ./CONVENTIONS.md          # universal, always loaded
@import ~/.claude/CLAUDE.md       # user prefs, not in repo

## Rules (universal)
- Conventional commits; never push to main directly.

## Path-scoped rules
- apply to: "frontend/**"  ->  @import ./frontend/CLAUDE.md
- apply to: "infra/**"     ->  @import ./infra/CLAUDE.md
```

```markdown
# frontend/CLAUDE.md (loaded only when work touches frontend/**)
- Use the design-system tokens; no inline styles.
- Co-locate tests as *.test.tsx next to the component.
```

## Anti-patrón

```markdown
# CLAUDE.md (ANTI: monolithic, 2000 lines, always loaded)
- Use design-system tokens.        # only relevant to frontend
- Prefer pnpm over npm.            # personal preference, leaked into repo
- ABAP naming is Z-prefixed.       # only relevant to one legacy module
- ...1990 more lines that load on every single turn, blowing the cache...
```

## Checklist de validación

- ¿Hay separación clara user / team / module en archivos distintos?
- ¿Los `@imports` son estables y cache-friendly (sin valores por-turno en el prefijo)?
- ¿Las reglas de subárbol están activadas por glob, no copiadas al raíz?
- ¿La precedencia por subpath está definida y es predecible (más específico gana)?
- ¿Las preferencias personales están fuera del repo de equipo (user scope)?

## Katas y skills relacionadas

- Katas: `katas-08`, `katas-09`.
- Relacionadas: `katas-hierarchical-claude-memory`, `katas-path-conditional-rules`, `context-window-engineering`.
