<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 25 · Prompt primario

## Objetivo

Decidir cómo reanudar el trabajo del agente aplicando el patrón resume / fork / fresh, y emitir el comando concreto.

## Entradas requeridas

- Nombre o ID de la sesión previa (si existe).
- Qué pasó entre sesiones: ¿hubo refactor, migración, deploy o edición masiva?
- Objetivo de la reanudación: continuar lo mismo, explorar enfoques alternativos, o retomar con estado actualizado.
- Disponibilidad de un scratchpad estructurado (Kata 18) como fuente de summary.

## Proceso

1. **Clasifica.** ¿Contexto previo válido y conversación lógica → resume? ¿Dos caminos independientes desde una baseline → fork? ¿El mundo cambió y los tool results están stale → fresh?
2. **Verifica staleness.** Si hubo refactor/migración/deploy, descarta resume.
3. **Ejecuta el patrón:**
   - resume: `claude --resume <nombre-sesion>`
   - fork: `claude --fork <baseline> --new-name approach-A` (y approach-B)
   - fresh: `SUMMARY=$(cat scratchpad.md); claude -p "Continuamos. Hallazgos previos:\n$SUMMARY"`, recargando fuentes actualizadas.
4. **Valida.** Nunca pegues transcript crudo viejo; confirma que el summary es tipado y curado.

## Salida

Markdown con: decisión (resume/fork/fresh), justificación (validez del contexto vs stale), comando ejecutable y riesgos residuales.
