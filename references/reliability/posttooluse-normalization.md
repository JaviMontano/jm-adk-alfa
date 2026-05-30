# Normalización con PostToolUse (Kata 03)

> Reescribe outputs heterogéneos de tools (XML legacy, códigos arcanos) a JSON canónico **antes** de que entren al historial del modelo. Es responsabilidad del runtime, no del autor de cada tool.

## Por qué runtime, no convención

Sin normalización central, cada token de XML legacy quema budget (Kata 10) y dispersa atención (Kata 11). Normalizar por-tool es frágil: cualquier handler nuevo que olvide la regla envenena el contexto. PostToolUse es runtime **garantizado**.

## Patrón (Agent SDK)

```python
STATUS_MAP = {"0xA1": "paid", "0xA7": "timeout", "0xB3": "rejected"}

async def normalize_legacy(input_data, tool_use_id, context):
    if not input_data.get("tool_name", "").endswith("legacy_lookup"):
        return {}
    raw = _extract_text_payload(input_data.get("tool_response"))
    if not raw:
        return {}
    clean = {
        "id": raw.get("@id"),
        "status": STATUS_MAP.get(raw.get("s", ""), "unknown"),
        "amount": float(raw.get("amt", 0)),
    }
    return {"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "updatedMCPToolOutput": {"content": [{"type": "text", "text": json.dumps(clean)}]},
    }}

options = ClaudeAgentOptions(hooks={"PostToolUse": [HookMatcher(matcher="*", hooks=[normalize_legacy])]})
```

`updatedMCPToolOutput` reemplaza el output crudo; el modelo nunca ve el XML. `additionalContext` anexa metadatos auditables sin contaminar el payload limpio.

## Anti-patrón

Cada tool decide si normaliza vía su propio `@tool` decorator → un handler nuevo olvida y reintroduce XML crudo al contexto.

## Relación con Claude Code

El hook PostToolUse de Claude Code (`scripts/post-tool-check.sh`) opera a nivel de logging del workspace; la normalización de payload descrita aquí es a nivel de Agent SDK (`ClaudeAgentOptions.hooks`). Ambos son PostToolUse, distinto surface.

Relacionado: `katas-posttooluse-normalization`, `katas-pretooluse-guardrails`, `katas-prefix-caching`.
