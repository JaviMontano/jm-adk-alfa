<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hierarchical Claude Memory · Meta / Activación

## Activar cuando

- La tarea menciona `CLAUDE.md`, memoria jerárquica, `@imports`, o precedencia de memoria.
- Se debe decidir en qué nivel (usuario / equipo / módulo) colocar una convención.
- Hay que refactorizar un `CLAUDE.md` monolítico hacia `@imports` modulares.
- Dos niveles de memoria entran en conflicto y se necesita resolver precedencia.

## NO activar cuando

- La tarea es sobre reglas condicionales por glob de ruta (eso es `katas-path-conditional-rules`).
- La tarea no tiene relación con la memoria persistente del agente.
- El input está vacío: pedir el objetivo antes de actuar.

## Chequeo de coherencia

- ¿Las preferencias personales quedaron fuera del repo?
- ¿El archivo principal del equipo usa `@imports` y se mantiene corto?
- ¿La precedencia subpath > repo > user se aplica en los conflictos?
