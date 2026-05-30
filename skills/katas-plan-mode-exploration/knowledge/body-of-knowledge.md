<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Plan Mode Exploration Body of Knowledge

## Canon

Plan Mode es la fase solo-lectura de un contrato de dos modos. El agente explora un repo desconocido sin poder escribir, redacta `plan.md` y solo transiciona a escritura tras firma humana.

### Conceptos clave

- **Dos modos discretos:** read-only (Plan) y write (Direct). La transición es explícita y registrada, no implícita.
- **Deshabilitado, no desaconsejado:** en Plan Mode las herramientas de escritura están bloqueadas por un hook, no apenas desincentivadas por el system_prompt.
- **`plan.md` firmado:** el artefacto de aprobación es texto auditable. La aprobación es una firma sobre un plan congelado, no un "ok" verbal.
- **Re-aprobación ante cambios:** si el plan cambia, se vuelve a Plan Mode, se actualiza `plan.md` y se re-pide aprobación.
- **Los hooks aplican el modo:** la barrera de seguridad es el hook `PreToolUse`, que enumera tools de escritura (`Write`, `Edit`, `NotebookEdit`, `Bash` con redirecciones) y deniega mientras `mode=="plan"`.

## Quality Signals

| Signal | Target |
|---|---|
| Modo solo-lectura | `permission_mode="plan"` con `allowed_tools=["Read","Glob","Grep"]` |
| Hook de bloqueo | `PreToolUse` deniega escritura mientras el modo sea plan |
| Artefacto de aprobación | `plan.md` firmado por humano, auditable |
| Transición controlada | Escritura solo tras firma; cambios al plan re-piden aprobación |
| Cobertura del borde Bash | El hook inspecciona el comando, no solo el nombre de la tool |

## Anti-patrón canónico

`permission_mode="bypassPermissions"` con `allowed_tools=["Read","Write","Edit","Bash"]` desde el inicio sobre un repo desconocido: elimina la fase de exploración segura y entrega el disco al primer error de razonamiento.

## Quiz canónico

- Respuestas: B · B · B.
- P2: ante un cambio en el alcance, volver a Plan Mode, actualizar `plan.md` y re-pedir aprobación.
- P3: un hook `PreToolUse` que enumera las tools de escritura (`Write`, `Edit`, `NotebookEdit`, `Bash` con redirecciones) y las deniega.
