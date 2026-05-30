<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hierarchical Claude Memory

Memoria jerárquica `CLAUDE.md` en tres niveles (usuario / equipo / módulo) con `@imports` y precedencia por especificidad de subpath.

## Resumen ejecutivo

`CLAUDE.md` es la memoria persistente del agente. Carga en cascada desde `~/.claude/CLAUDE.md` (usuario), `<repo>/CLAUDE.md` (equipo) y `<repo>/<subpath>/CLAUDE.md` (módulo). La regla más específica gana (subpath > repo > user). Las preferencias personales viven en el home, nunca en el repo. Los `@imports` mantienen el archivo principal corto y caché-friendly; un monolito de 2000 líneas inline degrada la caché y dispersa la atención.

## Triggers

- hierarchical memory
- claude md memory
- memory imports
- memory precedence

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill al diseñar o auditar la memoria persistente de un proyecto, decidir en qué nivel colocar una convención, refactorizar un `CLAUDE.md` monolítico hacia `@imports`, o resolver precedencia entre niveles en conflicto.

## Output Format

Markdown con summary, evidence, result, validation y risks.
