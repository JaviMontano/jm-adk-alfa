<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Independent Reviewer Multipass Quick Variation

Úsala cuando el changeset es pequeño (pocos archivos) pero aún requiere un reviewer independiente.

- Salta el Pass B cross-file si los archivos no interactúan entre sí.
- Ejecuta el Pass A en sesión limpia y devuelve findings por archivo.
- Mantén la regla: nunca self-review, nunca quorum N-de-M.
