<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Se reorganizó la memoria monolítica en tres niveles y se modularizó el nivel equipo con `@imports`. Las preferencias personales salieron del repo hacia el home.

## ANTI (estado inicial)

```text
# <repo>/CLAUDE.md  (2000 líneas inline)
## Style ... (300 líneas)
## Testing ... (400 líneas)
## Forbidden ...
- terse commits        # preferencia personal contaminando el repo
- ruff over black      # diverge entre máquinas
```

## GOOD (estado final)

```text
# <repo>/CLAUDE.md  (equipo, corto y caché-friendly)
## Style
@docs/style-guide.md

## Testing
@docs/testing-conventions.md

## Forbidden
- never run pip install without venv

# ~/.claude/CLAUDE.md  (usuario, fuera del repo)
- terse commits
- ruff over black
```

## Validation

- Preferencias personales fuera del repo: sí (movidas a `~/.claude/CLAUDE.md`).
- Nivel equipo modularizado con `@imports`: sí (`docs/style-guide.md`, `docs/testing-conventions.md`).
- Precedencia subpath > repo > user aplicada: sí (un `src/CLAUDE.md` futuro sobrescribiría al repo).
- Archivo principal corto / caché-friendly: sí (de 2000 líneas a secciones con `@imports`).

## Risks and Limits

- Verificar que las rutas de `@imports` existan y sean relativas al archivo que importa.
- La memoria no reemplaza revisión experta para decisiones de alto riesgo.
