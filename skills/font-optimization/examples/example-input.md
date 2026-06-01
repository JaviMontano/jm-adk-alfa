<!--
generated-by: scripts/scaffold-skill.py
generated-for: font-optimization
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Optimiza la carga de fuentes del landing `index.html`.

Contexto:

- Actualmente usa Google Fonts con `Poppins`, `Montserrat` y `JetBrains Mono`.
- El CSS usa `@import` en una hoja secundaria.
- Hay archivos `.ttf` legacy en `/fonts`.
- La pagina necesita mantener una fuente de encabezados, una de cuerpo y una mono para metadata.

Entrega:

- Hallazgos de auditoria.
- Snippets `@font-face` y preload.
- Recomendacion de subset/variable font.
- Checklist de validacion.
