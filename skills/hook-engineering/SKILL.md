---
name: hook-engineering
version: 1.0.0
description: "Disenar hooks deterministas (PreToolUse permissionDecision deny, PostToolUse updatedMCPToolOutput) que el runtime garantiza, con politica recargable en codigo."
owner: "JM Labs"
triggers:
  - hook engineering
  - pretooluse hook
  - posttooluse hook
  - deterministic hooks
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Hook Engineering

## Capacidad

Registrar hooks en `ClaudeAgentOptions.hooks` que el runtime del Agent SDK garantiza,
para hacer cumplir politicas y normalizar I/O sin depender del modelo. Un hook bien
construido convierte una regla "que el modelo deberia respetar" en un control que el
runtime ejecuta siempre: el PreToolUse decide `allow|deny|ask` antes de cualquier
side-effect, y el PostToolUse reescribe la respuesta de la tool antes de que entre al
historial. La politica vive en codigo recargable, no en el system prompt, de modo que
una inyeccion de prompt no puede desactivarla.

## Cuando usarla

- Limites criticos no negociables: topes monetarios, rutas protegidas, dominios permitidos.
- Normalizacion de outputs heterogeneos hacia un contrato unico antes de que el modelo los lea.
- Enforcement de modo de operacion (plan read-only vs write) independiente del prompt.
- Cualquier regla cuyo incumplimiento sea costoso o irreversible y no se pueda dejar a criterio del modelo.

## Como construir

1. Define la politica en codigo recargable (`dict`/JSON hot-reload), nunca en el prompt.
2. Implementa el PreToolUse: inspecciona `tool_name` + `tool_input` y devuelve
   `permissionDecision: allow|deny|ask` ANTES de ejecutar, con cero side-effects.
3. Implementa el PostToolUse: reescribe `tool_response` hacia `updatedMCPToolOutput`
   ANTES de que la respuesta entre al historial del modelo.
4. Registra los hooks con `HookMatcher(matcher="*")` para cobertura global, o por-tool
   cuando la politica sea especifica.
5. Deja traza auditable de cada decision deny (regla disparada, payload evaluado).

## Patron correcto

```python
import json
from pathlib import Path
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

POLICY_PATH = Path("references/guardrails/tool-policy.json")

def load_policy() -> dict:
    # Hot-reload en cada invocacion: la politica vive en codigo/JSON, no en el prompt.
    return json.loads(POLICY_PATH.read_text())

async def pre_tool_guard(input_data, tool_use_id, context):
    policy = load_policy()
    tool_name = input_data["tool_name"]
    tool_input = input_data.get("tool_input", {})

    rule = policy.get(tool_name)
    if rule and rule.get("max_amount") is not None:
        amount = tool_input.get("amount", 0)
        if amount > rule["max_amount"]:
            # Deny estructurado ANTES de cualquier side-effect.
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"amount {amount} exceeds limit {rule['max_amount']}"
                    ),
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[pre_tool_guard])]},
)
```

## Anti-patron

```python
# ANTI 1: politica solo en el system prompt. Una inyeccion de prompt la rompe.
SYSTEM_PROMPT = "Never approve a transfer above 10000 USD."  # el modelo puede ignorarla

# ANTI 2: normalizacion ad-hoc por-tool en cada handler.
# Un handler nuevo olvida normalizar y el modelo ve payloads crudos inconsistentes.
def handle_search(resp):
    return resp["raw"]  # sin contrato unico; el siguiente tool tendra otro shape
```

## Checklist de validacion

- La politica vive en codigo recargable, no en el system prompt.
- El `deny` ocurre antes de cualquier side-effect (el PreToolUse no muta nada).
- El modelo nunca ve el payload crudo: el PostToolUse normaliza antes del historial.
- Cada decision es auditable (regla disparada + payload evaluado quedan trazados).
- La cobertura usa `matcher="*"` o por-tool de forma deliberada, sin huecos.

## Katas y skills relacionadas

- Katas: `02`, `03`, `07`.
- Skills relacionadas: `katas-pretooluse-guardrails`, `katas-posttooluse-normalization`,
  `plan-mode-workflow`, `mcp-engineering`.
