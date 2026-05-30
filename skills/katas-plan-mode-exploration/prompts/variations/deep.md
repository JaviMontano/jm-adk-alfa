<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Plan Mode Exploration Deep Variation

Úsala cuando el repo es grande, desconocido o crítico, con consecuencias cross-file.

- Configura `permission_mode="plan"` + `allowed_tools=["Read","Glob","Grep"]` y registra el hook `PreToolUse` que deniega escritura (`Write`, `Edit`, `NotebookEdit`, `Bash` con redirecciones) mientras `mode=="plan"`.
- Explora a fondo: estructura, convenciones, dependencias, puntos de acoplamiento y riesgos.
- Redacta `plan.md` con notas de descubrimiento, opciones consideradas, arquitectura seleccionada, validación y riesgos.
- Solicita firma humana del plan congelado; cualquier cambio posterior vuelve a Plan Mode y re-pide aprobación antes de transicionar a escritura.
