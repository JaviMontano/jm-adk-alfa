<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-pretooluse-guardrails
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Pretooluse Guardrails Body of Knowledge

## Canon

Conceptos clave de la Kata 02:

- **Hook `PreToolUse`**: se registra en `ClaudeAgentOptions.hooks` y se ejecuta ANTES de cada invocación de tool, recibiendo `tool_name` y `tool_input`.
- **`permissionDecision`**: enum estructurado `allow` / `deny` / `ask`. No es texto libre; el SDK lo interpreta y aplica.
- **`permissionDecisionReason`**: mensaje legible que el modelo recibe cuando hay `deny`, para replanear.
- **Política en código**: un `dict` (`POLICY = {"max_amount": 1000.0}`) o un JSON en disco. Recargable en caliente sin reiniciar el agente.
- **`HookMatcher`**: filtra a qué tools aplica el hook; `matcher="*"` cubre todas.
- **Garantía del SDK**: si el hook retorna `deny`, la tool NO corre. Cero side-effects.
- **Relación con Kata 01**: `permissionDecision` controla cada tool; `stop_reason` controla el bucle agéntico.

## Quality Signals

| Signal | Target |
|---|---|
| Política fuera del prompt | Los límites críticos viven en hook/`dict`/JSON, no en `system_prompt` |
| Decisión estructurada | Se usa `permissionDecision: allow/deny/ask`, no texto libre |
| Bloqueo pre-ejecución | El `deny` corre ANTES de la tool, garantizando cero side-effects |
| Razón accionable | `permissionDecisionReason` permite al modelo replanear |

## Anti-patrón canónico

Política solo en `system_prompt` ("no apruebes reembolsos mayores a $1000") sin hooks `PreToolUse`. Un prompt injection o un usuario insistente la rompe y la tool ejecuta el reembolso de todas formas. La intención no es determinista hasta que el SDK puede aplicarla.

## Quiz de referencia

Respuestas B · C · B. P2: la política se actualiza mutando el `dict` `POLICY` o releyendo el JSON (hot-reload, sin reiniciar). P3: `deny` corre ANTES de ejecutar la tool (cero side-effects), mientras que un `raise` correría DESPUÉS, ya con efectos.

## Open Knowledge

- Añadir patrones de política compuesta (montos + dominios + paths) conforme se estabilicen.
