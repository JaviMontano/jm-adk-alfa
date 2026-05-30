<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Body of Knowledge · Memoria jerárquica con CLAUDE.md

## Conceptos clave

- **Tres niveles en cascada.** La memoria persistente del agente vive en `~/.claude/CLAUDE.md` (usuario), `<repo>/CLAUDE.md` (equipo) y `<repo>/<subpath>/CLAUDE.md` (módulo). Cargan apilándose en ese orden.
- **Más específico gana.** La precedencia es subpath > repo > user. `repo/src/CLAUDE.md` sobrescribe `repo/CLAUDE.md` para los archivos bajo `src/`.
- **Frontera de privacidad.** Las preferencias personales (estilo de commits, herramientas favoritas) van en el home y NUNCA en el repo, porque divergen entre miembros del equipo y entre máquinas.
- **Modularidad con `@imports`.** El archivo principal se mantiene corto importando archivos chicos en `docs/`: `## Style @docs/style-guide.md`, `## Testing @docs/testing-conventions.md`. Esto es caché-friendly (ver Kata 10).
- **Reglas universales inline.** Prohibiciones de seguridad cortas (p. ej. `never run pip install without venv`) pueden ir inline en el nivel correspondiente.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Frontera de privacidad | Preferencias personales solo en `~/.claude/CLAUDE.md` |
| Modularidad | Nivel equipo usa `@imports` a archivos chicos en `docs/`, no inline masivo |
| Precedencia | Conflictos se resuelven por la regla más específica (subpath > repo > user) |
| Caché-friendliness | Archivo principal corto; no monolito de 2000 líneas |
| Alcance de módulo | Reglas locales justificadas por especificidad de subpath |

## Anti-patrón canónico

Mezclar preferencias personales en el repo del equipo (p. ej. `terse commits` o `ruff over black` en `<repo>/CLAUDE.md`) y mantener un `CLAUDE.md` monolítico de 2000 líneas con todo inline. El primero contamina la fuente de verdad compartida y diverge entre máquinas; el segundo degrada la caché y dispersa la atención del modelo.

## Argumento de certificación

Separación estricta usuario/equipo/módulo en `CLAUDE.md` y uso de `@imports` para modularidad y caché-friendliness.

## Conocimiento abierto

- Conectar con `katas-context-cache-discipline` (Kata 10) para el impacto de caché de los `@imports`.
- Conectar con `katas-path-conditional-rules` (Kata 09) para reglas que cargan por glob.
