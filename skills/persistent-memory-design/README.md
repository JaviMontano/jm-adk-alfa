<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Persistent Memory Design

Capacidad de ingeniería de contexto para diseñar un scratchpad persistente en disco: un archivo estructurado con conclusiones validadas (Hipótesis / Decisiones / Hallazgos / Pendientes) que sobrevive a `/compact` y a resets de sesión, se lee una sola vez y después se referencia. Separa la memoria de trabajo volátil (la conversación) de la memoria persistente auditada (el archivo).

## Triggers

- persistent memory design
- scratchpad file
- durable agent memory
- investigation notes

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando una investigación o tarea larga deba sobrevivir a compactaciones o a sesiones nuevas, o cuando el agente repite trabajo por "olvidar" conclusiones ya validadas. Define una ruta estable y un esquema fijo de secciones, escribe solo conclusiones validadas con evidencia, lee el archivo una vez y referéncialo después. Verifica que tras `/compact` el estado se reconstruye solo desde el archivo.

## Output Format

Markdown con summary, evidence, result, validation y risks. El artefacto central es el archivo scratchpad con secciones tipadas, donde cada hallazgo queda trazado a su source y fecha.
