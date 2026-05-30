<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Builtin Tool Selection Primary Prompt

## Objective

Resolver una tarea de exploración o modificación de codebase escogiendo el built-in tool correcto y aplicando la estrategia incremental `Grep` → `Read` → `Edit`, sin cargar el repositorio entero.

## Required Inputs

- Objetivo concreto (qué encontrar o qué cambiar).
- Codebase o conjunto de archivos de referencia.
- Restricciones (lenguaje, patrón de path, símbolo a localizar).
- Definition of done.

## Process

1. `Grep` para localizar los entry points por contenido (`pattern` + `glob`); usa `Glob` si el criterio es el nombre de archivo (p. ej. `**/*.test.tsx`).
2. `Read` selectivo solo de los archivos relevantes, siguiendo imports.
3. `Edit` con un anchor único; si el anchor matchea varias líneas, amplíalo con contexto suficiente o cae a `Read` entero + `Write` completo.
4. Valida: el tool elegido coincide con la intención, no hubo `Read` masivo upfront, el anchor era único.

## Output

Devuelve el deliverable en este shape: Markdown con summary, evidence (matches de `Grep`/`Glob`), result (el `Edit`/`Write` aplicado), validation y risks.
