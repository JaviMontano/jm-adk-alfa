<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Independent Reviewer Multipass

Multi-pass review con reviewer independiente en sesion limpia; per-file y cross-file; rechazo de quorum N-de-M.

## Triggers

- independent reviewer
- multipass review
- self-review bias
- per-file cross-file

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Kata 27 · Multi-Pass Review e Independent Reviewer. El modelo que generó el código es mal revisor de su propio output: retiene el contexto sesgado de su razonamiento. Esta skill aplica el patrón de reviewer independiente —una sesión limpia que solo ve el código resultante— y descompone PRs grandes en dos pases: Pass A per-file deep dive y Pass B cross-file integration. Rechaza explícitamente el quorum N-de-M (consensuar 2 de 3 reviews), que suprime issues raros legítimos.

## Quick Use

1. Detecta el caso: PR grande o changeset generado por un modelo que ahora se pediría revisar.
2. Pass A: revisa cada archivo en una sesión nueva e independiente (sin la cadena de generación), salida tipada por archivo.
3. Pass B: integración cross-file que opera solo sobre los resúmenes del Pass A (interacciones, duplicados de findings).
4. Nunca consenses por mayoría: preserva los findings de minoría como señal legítima.

## Output Format

Markdown con resumen, findings per-file (Pass A), findings cross-file (Pass B), evidencia, y riesgos. Cada finding referencia el archivo y la línea cuando aplica.
