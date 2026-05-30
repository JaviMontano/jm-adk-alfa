<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Builtin Tool Selection Deep Variation

Úsala cuando hay que rastrear un flujo cross-file (p. ej. auth: `authenticate`/`login`/`session`), cuando un `Edit` falla por anchor ambiguo, o cuando el cambio cruza varios archivos.

Incluye: notas de descubrimiento (qué `Grep`/`Glob` se corrieron y por qué), opciones consideradas para cada tool, la estrategia seleccionada (`Grep` → `Read` selectivo siguiendo imports → `Edit`), el manejo del failure mode de `Edit` con fallback `Read` + `Write`, validación y riesgos. Justifica explícitamente por qué se rechazó el `Read` masivo upfront.
