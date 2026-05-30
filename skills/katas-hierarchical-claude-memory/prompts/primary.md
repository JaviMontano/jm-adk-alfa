<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hierarchical Claude Memory · Primary Prompt

## Objetivo

Diseñar o auditar la memoria persistente `CLAUDE.md` de un proyecto aplicando el patrón de tres niveles (usuario / equipo / módulo) con `@imports` y precedencia por especificidad.

## Inputs requeridos

- Estructura del repo y ubicación de los `CLAUDE.md` existentes.
- Convenciones a codificar y a qué audiencia pertenecen (personal vs. equipo vs. módulo).
- Restricciones de caché y tamaño del archivo principal.
- Definition of done.

## Proceso

1. **Clasificar cada convención por nivel.** Personal → `~/.claude/CLAUDE.md`. Equipo → `<repo>/CLAUDE.md`. Local → `<repo>/<subpath>/CLAUDE.md`.
2. **Modularizar el nivel equipo con `@imports`** a archivos chicos en `docs/` (`## Style @docs/style-guide.md`, `## Testing @docs/testing-conventions.md`).
3. **Dejar inline solo prohibiciones cortas** (p. ej. `never run pip install without venv`).
4. **Resolver conflictos** con la regla más específica: subpath > repo > user.
5. **Validar** que no hay preferencias personales en el repo ni monolito inline.

## Output

Markdown con summary, evidence, result, validation y risks. Bloques `CLAUDE.md` por nivel cuando aplique.
