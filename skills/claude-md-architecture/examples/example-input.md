<!--
generated-by: scripts/scaffold-skill.py
generated-for: claude-md-architecture
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Nuestro monorepo tiene un único `CLAUDE.md` de ~600 líneas en la raíz. Mezcla convenciones de commits (aplican a todos), reglas de tokens del design-system (solo `frontend/**`), naming ABAP con prefijo Z (solo el módulo legacy `sap/**`) y una preferencia personal del lead ("prefiere pnpm sobre npm"). Se carga entero en cada turno y el cache se invalida seguido.

Pedido: reestructura la memoria en una jerarquía user / team / module con `@imports` y reglas por glob, de modo que el prefijo raíz quede estable y cada módulo cargue solo sus reglas cuando se trabaja en él.
