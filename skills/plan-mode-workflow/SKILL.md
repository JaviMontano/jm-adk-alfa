---
name: plan-mode-workflow
version: 1.0.0
description: "Operar repos desconocidos en Plan Mode read-only con plan firmado antes de escribir, aplicado por hooks."
owner: "JM Labs"
triggers:
  - plan mode workflow
  - read-only exploration
  - plan approval gate
  - two-mode operation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Plan Mode Workflow

## Capacidad

Operar un repositorio o dominio desconocido en dos modos explícitos: un **Plan Mode read-only** donde el agente solo lee (Read, Grep, Glob, Bash de inspección) y produce un `plan.md`, y un **Execute Mode** que se habilita únicamente tras la aprobación firmada de ese plan. La transición entre modos no depende de la buena voluntad del modelo: la aplica un **hook** que enumera y bloquea las tools de escritura mientras el modo activo sea `plan`. La capacidad construible es el diseño del gate: estado de modo, contrato del plan, evento de firma y enforcement por hook.

## Cuándo usarla

- Antes de la primera escritura en un repo que el agente no conoce y cuyo blast radius es desconocido.
- Cuando la organización exige una aprobación auditable antes de mutar archivos (cambio gobernado, compliance, producción).
- Cuando varias personas o agentes comparten el workspace y un write prematuro puede pisar trabajo no commiteado.
- Cuando el plan puede cambiar a mitad de camino y necesitas que cada cambio re-dispare la firma, no que se cuele silenciosamente.

## Cómo construir

1. **Define el estado de modo** como dato explícito (`mode: "plan" | "execute"`), no como una intención en prosa. Por defecto arranca en `plan`.
2. **Enumera las write-tools** que el hook debe bloquear en `plan` (`Write`, `Edit`, `MultiEdit`, `Bash` mutante, MCP de mutación). Lo que no esté en la lista de lectura, se bloquea.
3. **Escribe el `plan.md`** como artefacto: objetivo, archivos a tocar, orden de cambios, criterio de aceptación y riesgos. Es el objeto que se firma.
4. **Modela la aprobación como evento auditable** (`plan_signed_at`, `approved_by`, hash del plan), no como un "ok" conversacional. La firma referencia el hash del plan exacto.
5. **Implementa el hook `PreToolUse`** que lee el modo: si `mode == "plan"` y la tool está en la write-list, deniega con motivo. Solo `plan_approved(hash)` cambia `mode` a `execute`.
6. **Re-dispara firma ante cambios**: si el `plan.md` cambia (hash distinto al firmado), el modo vuelve a `plan` y se exige nueva aprobación.
7. **Cierra con evidencia**: el plan firmado más el diff resultante son el rastro auditable de qué se autorizó y qué se ejecutó.

## Patrón correcto

```python
# GOOD: el modo es estado; el hook bloquea writes hasta firma del hash exacto.
STATE = {"mode": "plan", "signed_plan_hash": None}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

def pre_tool_use(tool_name: str, plan_hash_now: str) -> dict:
    if STATE["mode"] == "plan" and tool_name in WRITE_TOOLS:
        return {"decision": "deny",
                "reason": "Plan Mode is read-only. Sign plan.md to enter execute."}
    # any change to the plan after signing reverts to plan mode
    if STATE["signed_plan_hash"] and plan_hash_now != STATE["signed_plan_hash"]:
        STATE["mode"] = "plan"
        return {"decision": "deny", "reason": "plan.md changed; re-approval required."}
    return {"decision": "allow"}

def approve_plan(plan_hash: str, approver: str) -> None:
    STATE["signed_plan_hash"] = plan_hash      # auditable artifact
    STATE["mode"] = "execute"                   # only path into write mode
```

## Anti-patrón

```python
# ANTI: bypassPermissions + escritura desde el primer turno, sin plan ni firma.
settings = {"permissionMode": "bypassPermissions"}   # no read-only gate
def run(repo):
    edit_file(repo / "main.py", patch)   # writes before exploration
    edit_file(repo / "config.yaml", patch)
    # no plan.md, no signed hash, no hook; the model decides alone.
```

## Checklist de validación

- ¿La escritura está deshabilitada mientras el modo es `plan` (no por convención, sino por hook)?
- ¿La aprobación es un artefacto auditable (hash + aprobador + timestamp), no un "ok" en la conversación?
- ¿Un cambio al `plan.md` después de firmado revierte a `plan` y re-pide firma?
- ¿El hook enumera explícitamente las tools de escritura a bloquear?
- ¿El plan firmado y el diff final quedan como rastro de qué se autorizó?

## Katas y skills relacionadas

- Kata 07 cubre el diseño del gate de aprobación read-only.
- Relacionadas: `katas-plan-mode-exploration`, `custom-tooling-extension`, `human-escalation-design`.
