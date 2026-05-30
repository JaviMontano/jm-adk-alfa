<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Persistent Memory Design Primary Prompt

## Objective

Diseña e implementa un scratchpad persistente en disco para esta tarea o investigación: un archivo estructurado con conclusiones validadas que sobreviva a `/compact` y a un reset de sesión, se lea una sola vez y se referencie después.

## Required Inputs

- Goal: qué investigación o tarea larga necesita memoria duradera.
- Context: cuánto contexto hay, cada cuánto se compacta, si es multi-sesión.
- Constraints: ruta del archivo, convenciones del repo (CLAUDE.md), evidencia exigida.
- Definition of done: el estado se reconstruye solo desde el archivo tras `/compact`.

## Process

1. Discover: identifica qué conclusiones deben sobrevivir y dónde vive hoy el estado.
2. Analyze: define ruta estable y esquema fijo (Hypotheses / Decisions / Findings / Open).
3. Execute: implementa bootstrap de lectura única y upserts tipados de conclusiones validadas con su source y fecha.
4. Validate: simula `/compact`/reset y confirma que el agente reconstruye estado solo desde el archivo, sin relectura por turno.

## Output

Devuelve el resultado como Markdown con summary, evidence, result, validation y risks. El artefacto central es el archivo scratchpad con secciones tipadas; cada hallazgo trazado a source y fecha.
