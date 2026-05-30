<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Se configuró el agente en Plan Mode read-only para explorar el repo de microservicios sin riesgo de escritura. Se mapeó el servicio de pagos y se redactó `plan.md` con la propuesta de autenticación JWT, congelado a la espera de firma humana antes de transicionar a escritura.

## GOOD (patrón aplicado)

```python
options = ClaudeAgentOptions(
    permission_mode="plan",
    allowed_tools=["Read", "Glob", "Grep"],
    system_prompt="En Plan Mode: explora, mapea, redacta plan.md. NO escribas código.",
)

write_tools = {"Write", "Edit", "NotebookEdit", "Bash"}
def pre_tool_use(tool_name, mode):
    if tool_name in write_tools and mode == "plan":
        return {"permissionDecision": "deny"}
    return {"permissionDecision": "allow"}
```

### plan.md propuesto (extracto)

- Hallazgos: el servicio de pagos usa FastAPI; los middlewares viven en `services/payments/app/middleware/`; no hay capa de auth previa.
- Arquitectura propuesta: middleware `JWTAuthMiddleware` + dependencia `verify_token`; secreto vía variable de entorno.
- Cambios (tras aprobación): nuevos archivos de middleware y dependencia; sin tocar lógica de cobro.

### Aprobación

- Estado: pendiente de firma humana.
- Transición a escritura: solo tras firma; si el plan cambia, se vuelve a Plan Mode y se re-pide aprobación.

## ANTI (rechazado)

```python
# NO: escritura habilitada sobre repo desconocido desde el inicio
options = ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    allowed_tools=["Read", "Write", "Edit", "Bash"],
)
```

Esto entrega el disco al primer error de razonamiento: el agente podría sobrescribir la lógica de cobro antes de que un humano revise nada.

## Validation

- La skill se activó intencionalmente sobre un repo desconocido y crítico.
- En Plan Mode las herramientas de escritura quedaron deshabilitadas por el hook, no solo desaconsejadas.
- El artefacto de aprobación es `plan.md` firmado, no un "ok" verbal.
- Cambios al plan re-piden aprobación; los hooks aplican el modo.
