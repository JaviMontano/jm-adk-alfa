---
name: katas-plan-mode-exploration
version: 1.0.0
description: "Exploracion segura en Plan Mode read-only con plan.md firmado por humano antes de transicionar a escritura."
owner: "JM Labs"
triggers:
  - plan mode
  - read-only exploration
  - plan approval
  - safe exploration
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Plan Mode Exploration

## Qué es

Antes de modificar un repositorio desconocido, el agente entra en Plan Mode (solo-lectura). Explora el código, mapea convenciones y escribe un `plan.md` con hallazgos y arquitectura propuesta. Obtiene aprobación humana directa sobre ese plan antes de transicionar a un modo de escritura (Direct). El artefacto de aprobación es texto auditable, no un "ok" verbal.

## Por qué importa (falla que evita)

Lanzar un agente con permisos de escritura sobre un repo desconocido es destrucción probabilística. El primer error borra archivos clave o reescribe convenciones del proyecto, y recuperar es caro. Plan Mode separa exploración de mutación: el agente puede equivocarse al razonar sin tocar el disco, y el humano revisa el plan antes de que cualquier herramienta destructiva se habilite.

## Modelo mental

- Dos modos discretos: read-only (Plan) y write (Direct). La transición es explícita y registrada.
- En Plan Mode las herramientas de escritura están deshabilitadas, no desaconsejadas. Es un hook que niega, no una instrucción de cortesía.
- El artefacto de aprobación es un `plan.md` firmado por humano, texto auditable.
- Aprobación = firma + plan congelado. Cualquier cambio al plan re-pide aprobación.
- Los hooks aplican el modo; el system_prompt orienta el comportamiento pero no es la barrera de seguridad.

## Patrón correcto

```python
options = ClaudeAgentOptions(
    permission_mode="plan",
    allowed_tools=["Read", "Glob", "Grep"],
    system_prompt=(
        "En Plan Mode: explora, mapea, redacta plan.md. NO escribas código."
    ),
)

# hook PreToolUse niega escritura mientras el modo sea plan:
write_tools = {"Write", "Edit", "NotebookEdit", "Bash"}
def pre_tool_use(tool_name, mode):
    if tool_name in write_tools and mode == "plan":
        return {"permissionDecision": "deny"}
    return {"permissionDecision": "allow"}
```

La transición a `permission_mode` de escritura ocurre solo después de que un humano firma `plan.md`. Si el plan cambia, se vuelve a Plan Mode, se actualiza `plan.md` y se re-pide aprobación.

## Anti-patrón

```python
options = ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    allowed_tools=["Read", "Write", "Edit", "Bash"],  # escritura desde el inicio
)
```

Arrancar en `bypassPermissions` con herramientas de escritura habilitadas sobre un repo desconocido elimina la fase de exploración segura y entrega el disco al primer error de razonamiento.

## Argumento de certificación

Plan Mode es un contrato de dos modos read-only/write con transición firmada por humano, no un "modo de cortesía". Los hooks aplican el modo: enumeran las tools de escritura (`Write`, `Edit`, `NotebookEdit`, y `Bash` con redirecciones) y las deniegan mientras el modo sea plan. El artefacto de aprobación es `plan.md` firmado; cambios al plan re-piden aprobación.

## Cuándo activar

- Vas a operar sobre un repositorio o base de código desconocida o crítica.
- Necesitas explorar y proponer arquitectura antes de mutar nada.
- El flujo exige aprobación humana explícita antes de escribir.
- Quieres una barrera dura (hook) contra escritura accidental durante exploración.

## Skills relacionadas

- `katas-hierarchical-claude-memory`
- `katas-custom-commands-skills`
- `katas-session-resume-fork`
