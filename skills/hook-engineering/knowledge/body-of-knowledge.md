<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Hook Engineering Body of Knowledge

## Canon de la capacidad

Los hooks son el unico mecanismo del Agent SDK que el runtime garantiza sin pasar por la
voluntad del modelo. Se registran en `ClaudeAgentOptions.hooks` como `HookMatcher` y operan
en dos momentos clave:

- **PreToolUse**: recibe `tool_name` + `tool_input`, inspecciona y devuelve
  `permissionDecision: allow|deny|ask` ANTES de ejecutar la tool. Es el punto de
  enforcement de politica; debe ser inspeccion pura, sin side-effects.
- **PostToolUse**: recibe `tool_response` y la reescribe hacia `updatedMCPToolOutput`
  ANTES de que entre al historial. Es el punto de normalizacion de I/O.

La regla estructural es que la politica vive en **codigo recargable** (`dict`/JSON
hot-reload), no en el system prompt. Asi una inyeccion de prompt no puede desactivar el
limite, y el control queda fuera del razonamiento del modelo.

## Conceptos clave

- **Politica recargable**: fuente unica de verdad de limites y reglas, leida en cada
  invocacion del hook para soportar hot-reload.
- **permissionDecision**: `allow|deny|ask`; el deny estructurado incluye razon auditable.
- **updatedMCPToolOutput**: contrato unico de salida que el modelo siempre ve normalizado.
- **HookMatcher**: `matcher="*"` para cobertura global o por-tool para reglas especificas.
- **Auditabilidad**: cada decision deny deja traza (regla disparada + payload evaluado).

## Senales de calidad

| Senal | Objetivo |
|---|---|
| Politica en codigo | La regla vive en JSON/dict recargable, nunca en el prompt |
| Deny pre-side-effect | El PreToolUse decide antes de mutar nada |
| Modelo sin crudo | El PostToolUse normaliza antes del historial |
| Cobertura deliberada | `matcher="*"` o por-tool sin huecos |
| Trazabilidad | Cada deny es auditable |

## Decision de diseno

Usa hooks (no prompt) cuando el incumplimiento sea costoso o irreversible: topes
monetarios, paths protegidos, dominios permitidos, modo plan/write. Usa PostToolUse cuando
distintas tools devuelvan shapes heterogeneos que el modelo deba consumir como contrato unico.

## Anti-patron

- Politica solo en el system prompt: una inyeccion de prompt la rompe.
- Normalizacion ad-hoc por-tool: un handler nuevo la olvida y el modelo recibe payloads
  crudos inconsistentes.

## Open Knowledge

- Anadir referencias especificas del proyecto a medida que se estabilizan.
