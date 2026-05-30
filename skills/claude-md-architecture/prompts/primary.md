<!--
generated-by: scripts/scaffold-skill.py
generated-for: claude-md-architecture
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Claude Md Architecture Primary Prompt

## Objetivo

Estructurar la memoria `CLAUDE.md` del proyecto en una jerarquía user / team / module con `@imports` y reglas condicionales por glob, preservando el prefijo cacheable.

## Inputs requeridos

- Árbol del repo y `CLAUDE.md` actuales (raíz y subdirectorios).
- Lista de reglas vigentes y a qué ámbito aplican.
- Módulos que necesitan reglas propias (p. ej. `frontend/`, `infra/`, `tests/`).
- Preferencias personales que hoy estén en el repo de equipo.

## Proceso

1. Inventaría las reglas actuales y clasifícalas: universal / por-módulo / por-usuario.
2. Deja en el raíz de equipo solo universales más un bloque de `@imports`.
3. Crea `module/CLAUDE.md` por subárbol con reglas activadas por glob.
4. Mueve las preferencias personales a `~/.claude/CLAUDE.md` (user scope).
5. Documenta la precedencia por subpath (más específico gana).
6. Verifica que el prefijo no contenga valores por-turno ni reglas de un solo módulo.

## Output

Devuelve el deliverable en Markdown con resumen, evidencia (rutas y reglas reubicadas), resultado (jerarquía propuesta), validación (checklist) y riesgos.
