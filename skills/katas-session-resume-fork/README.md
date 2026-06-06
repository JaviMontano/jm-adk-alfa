<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 25 · Gestión de Sesiones (Resume y Fork)

Tres patrones de preservación de contexto entre corridas del agente y el criterio para elegir: `--resume` (contexto válido, misma investigación), `fork` (ramas paralelas desde una baseline, cero interferencia) y sesión fresh con summary tipado inyectado en el system prompt (cuando los tool results previos están stale porque el mundo cambió). El scratchpad estructurado (Kata 18) es la fuente del summary.

## Triggers

- session resume
- session fork
- fresh summary session
- stale tool results

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Pregunta: ¿el contexto previo sigue siendo válido? Si sí y la conversación avanza lógicamente → `--resume`.
2. ¿Necesitas explorar dos enfoques sin contaminación cruzada? → `fork` a dos sesiones nombradas desde la misma baseline.
3. ¿Hubo refactor, migración o deploy entre sesiones? Los tool results están stale → sesión fresh con summary tipado del scratchpad, recargando las fuentes actualizadas.
4. Nunca pegues el transcript completo viejo: infla contexto y reintroduce ruido.
5. Consulta `assets/manifest.json` y valida reportes JSON con `bash skills/katas-session-resume-fork/scripts/check.sh`.

## Output Format

Markdown con la decisión (resume / fork / fresh), la justificación (validez del contexto vs stale), el comando aplicado y los riesgos residuales.
