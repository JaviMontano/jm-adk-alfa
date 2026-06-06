<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-persistent-scratchpad
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Persistent Scratchpad

Scratchpad persistente en disco (`investigation-scratchpad.md`) curado por el agente. Almacena conclusiones validadas (decisiones, hallazgos, pendientes), sobrevive a `/compact` y a reinicios, se lee una vez al inicio y se referencia/anexa después.

## Resumen ejecutivo

La conversación es memoria volátil: cuando se compacta (Kata 11) se pierde detalle, y un hallazgo crítico que solo vivía en el historial desaparece. Este skill enseña a mantener memoria persistente en disco: el agente escribe únicamente conclusiones validadas en un archivo estructurado, lo lee una vez al reanudar la sesión y luego anexa en lugar de re-leer cada turno (para no romper el cache de prefijo de Kata 10).

## Triggers

- persistent scratchpad
- investigation scratchpad
- durable memory
- scratchpad file

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívalo en investigaciones largas o multisesión donde el detalle no puede perderse al compactar. Al reanudar, lee `investigation-scratchpad.md` una sola vez; durante la sesión anexa conclusiones validadas a las secciones `## Decisiones`, `## Hallazgos` y `## Pendientes`. Nunca vuelques monólogo interno ni hipótesis sin confirmar.

Consulta `assets/manifest.json` para los contratos determinísticos y valida reportes JSON con `bash skills/katas-persistent-scratchpad/scripts/check.sh`.

## Output Format

Markdown estructurado por secciones (Decisiones, Hallazgos, Pendientes) más estado de validación y riesgos residuales.
