<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Independent Reviewer Multipass Primary Prompt

## Objetivo

Revisar un PR o changeset aplicando el patrón de reviewer independiente multi-pass de la Kata 27.

## Inputs requeridos

- Conjunto de archivos a revisar (path + contenido).
- Confirmación de que el reviewer corre en una sesión NUEVA, sin la cadena de generación.
- Criterios de severidad y categorías de finding (si existen).

## Proceso

1. **Pass A (per-file):** para cada archivo, lanza una sesión independiente que revisa solo ese archivo y emite findings tipados. Nunca reutilices la sesión del generador.
2. **Pass B (cross-file):** integra solo los resúmenes tipados del Pass A. Instruye al modelo: "Detecta interacciones cross-file y duplicados de findings." No vuelvas a pasar el código crudo completo.
3. **Ensamblaje:** consolida findings preservando los de minoría. Prohibido aplicar quorum N-de-M.

## Output

Markdown con: resumen, findings Pass A (per-file), findings Pass B (cross-file), evidencia (archivo:línea) y riesgos.
