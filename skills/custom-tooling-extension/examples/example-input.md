<!--
generated-by: scripts/scaffold-skill.py
generated-for: custom-tooling-extension
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

> "Quiero que todo el equipo pueda generar las notas de versión de nuestro repo pidiéndoselo a Claude. Debe leer el `git log` entre dos tags y producir el changelog. Que no infle la sesión y que no pueda borrar nada del repo. Hoy tengo una versión que armé en mi `~/.claude` personal."

Restricciones implícitas a resolver:

- Debe **replicarse al equipo** → scope project (`.claude/`), no la versión personal en `~/.claude`.
- Se activa por contexto ("genera el changelog"), no por un disparo fijo → candidato a **skill** con `description` como contrato de routing.
- "Que no infle la sesión" → `context: fork`.
- "Que no pueda borrar nada" → `allowed-tools` whitelist mínima (lectura + git, sin permisos destructivos abiertos).
