<!--
generated-by: scripts/scaffold-skill.py
generated-for: claude-md-architecture
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Claude Md Architecture Body of Knowledge

## Canon

`CLAUDE.md` es la memoria persistente de un proyecto Claude Code. La capacidad consiste en estructurarla como una jerarquía de tres niveles en lugar de un único archivo:

- **User scope** (`~/.claude/CLAUDE.md`): preferencias personales del individuo; no se versiona en el repo del equipo.
- **Team scope** (repo-root `CLAUDE.md`): políticas universales del equipo; versionado; constituye el prefijo estable y cacheable.
- **Module scope** (`subdir/CLAUDE.md`): contrato de un subárbol; se carga solo cuando el trabajo toca ese subárbol.

Los `@imports` conectan niveles y deben mantenerse cache-friendly: el raíz importa universales y delega lo específico. Las reglas condicionales por glob (`apply to: "frontend/**"`) activan heurísticas solo donde aplican. La precedencia se resuelve por subpath: la regla más específica gana.

## Conceptos clave

- **Jerarquía de tres niveles**: separar user / team / module evita que una preferencia personal o una regla de módulo contamine el prefijo global.
- **`@imports` cache-friendly**: el prefijo (raíz + imports universales) debe ser estable, sin valores por-turno, para preservar el cache KV.
- **Reglas por glob**: la heurística vive en el módulo y se activa por ruta, no se copia al raíz.
- **Precedencia por subpath**: orden de resolución predecible; más específico gana.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Separación de niveles | user / team / module en archivos distintos |
| Imports cache-friendly | prefijo estable, sin valores por-turno |
| Activación por glob | reglas de subárbol no copiadas al raíz |
| Precedencia predecible | la regla más específica por subpath gana |

## Decisión de diseño

¿La regla aplica siempre? → raíz de equipo (universal). ¿Solo a un subárbol? → `module/CLAUDE.md` por glob. ¿Es preferencia personal? → user scope, fuera del repo. Si dudas entre raíz y módulo, pregunta: ¿esta regla tiene sentido para alguien que solo trabaja en otro módulo? Si no, va al módulo.

## Anti-patrón

`CLAUDE.md` monolítico de cientos o miles de líneas que se carga en cada turno, mezclando universales, reglas de un solo módulo y preferencias personales. Resultado: rompe el cache KV, diluye atención y filtra preferencias individuales al repo de equipo.
