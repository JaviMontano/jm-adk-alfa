<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Queremos correr code review automatizado con Claude Code en GitHub Actions sobre cada PR. El equipo abre ~80 PRs/día y un reviewer humano no alcanza. Necesitamos que el bot publique anotaciones por línea (archivo, línea, severidad, regla, mensaje) directamente en el PR, pero sin que el pipeline se rompa cada vez que el modelo cambie su redacción.

Restricciones:

- El runner no tiene TTY (modo headless).
- Severidades permitidas: `error`, `warning`, `info`.
- El merge lo sigue aprobando un humano; el bot solo anota.

Pregunta: ¿cómo montamos el step de CI para que sea determinista y robusto?
