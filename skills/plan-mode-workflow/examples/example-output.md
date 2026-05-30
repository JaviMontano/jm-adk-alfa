<!--
generated-by: scripts/scaffold-skill.py
generated-for: plan-mode-workflow
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Gate de dos modos construido sobre el servicio de pagos: exploración read-only, `plan.md` firmado por hash, y escritura habilitada solo tras la firma.

## Patrón correcto (GOOD)

```python
STATE = {"mode": "plan", "signed_plan_hash": None}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

def pre_tool_use(tool_name, plan_hash_now):
    if STATE["mode"] == "plan" and tool_name in WRITE_TOOLS:
        return {"decision": "deny", "reason": "Plan Mode read-only; sign plan.md."}
    if STATE["signed_plan_hash"] and plan_hash_now != STATE["signed_plan_hash"]:
        STATE["mode"] = "plan"
        return {"decision": "deny", "reason": "plan.md changed; re-approval required."}
    return {"decision": "allow"}

# plan.md firmado: hash a1b2c3, aprobado por lead-pagos, 2026-05-30T10:00-05:00
approve_plan("a1b2c3", "lead-pagos")   # -> mode = execute
```

## Anti-patrón (ANTI)

```python
# bypassPermissions + escritura desde el primer turno: sin plan, sin firma, sin hook.
settings = {"permissionMode": "bypassPermissions"}
edit_file("db/schema.sql", rename_patch)   # pisa cambios sin commitear de otro dev
```

## Validation

- [x] Escritura bloqueada por hook mientras `mode == "plan"`.
- [x] Aprobación auditable: hash `a1b2c3` + aprobador + timestamp.
- [x] Cambiar `plan.md` tras firmar revierte a `plan`.
- [x] Write-tools enumeradas explícitamente.
