<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hierarchical Claude Memory · Variación Deep

Usar cuando hay que rediseñar toda la memoria de un proyecto, hay conflictos entre niveles, o el `CLAUDE.md` es un monolito que degrada la caché.

- **Discovery:** inventariar todos los `CLAUDE.md` existentes (home, repo, subpaths) y clasificar cada convención por nivel y alcance.
- **Opciones:** evaluar qué mover al home, qué modularizar vía `@imports` a `docs/`, qué dejar inline (solo prohibiciones cortas).
- **Conflictos:** documentar cada choque entre niveles y resolver por la regla más específica (subpath > repo > user).
- **Caché:** medir el tamaño del archivo principal antes y después; objetivo: corto y caché-friendly.
- **Salida:** notas de discovery, opciones consideradas, enfoque elegido, bloques `CLAUDE.md` por nivel, validación y riesgos.
