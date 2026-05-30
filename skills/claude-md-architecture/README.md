<!--
generated-by: scripts/scaffold-skill.py
generated-for: claude-md-architecture
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Claude Md Architecture

## Resumen ejecutivo

Capacidad de ingeniería para estructurar la memoria persistente de un proyecto Claude Code como una jerarquía `CLAUDE.md` de tres niveles (user / team / module) unida por `@imports`, con reglas condicionales por glob de ruta. Las reglas universales viven en un prefijo estable y cacheable; las heurísticas de un módulo se cargan solo cuando el trabajo toca ese subárbol. Evita el monolito de 2000 líneas que se carga en cada turno y rompe el cache KV.

## Triggers

- claude md architecture
- hierarchical memory
- path scoped rules
- memory imports

## Allowed Tools

- Read
- Grep
- Glob
- Bash

Solo lectura e inspección del árbol del repo; no muta archivos sin confirmación explícita.

## Quick Use

1. Inventaría las reglas actuales y clasifícalas: universal, por-módulo, por-usuario.
2. Deja en el `CLAUDE.md` raíz solo universales más un bloque de `@imports`.
3. Crea `module/CLAUDE.md` por subárbol con reglas activadas por glob.
4. Mueve las preferencias personales a `~/.claude/CLAUDE.md` (user scope), nunca al repo del equipo.
5. Valida con el checklist: separación de niveles, imports cache-friendly, precedencia por subpath.

## Output Format

Markdown con resumen, evidencia, resultado, validación y riesgos.
