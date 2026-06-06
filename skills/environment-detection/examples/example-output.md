# Example Output — Environment Detection

## Environment Detected

- IDE: `codex` [CÓDIGO]
- Model tier: `heavy` from `128000` token budget [CONFIG]
- Triad mode: `sequential` because subagent and hook/MCP capabilities are absent [CÓDIGO]
- Confidence: `0.94` with no conflicting local signals [INFERENCIA]

## Signals

| id | source | value | evidence |
|----|--------|-------|----------|
| `s1` | `workspace/AGENTS.md` | AGENTS instructions are present | [CÓDIGO] |
| `s2` | `active_tools` | read/write/shell/git available | [CONFIG] |
| `s3` | `active_tools` | subagents and hooks/MCP unavailable | [CONFIG] |
| `s4` | `user_runtime_context` | context budget `128000` tokens | [CONFIG] |

## Loading Plan

| resource | level | reason |
|----------|-------|--------|
| `AGENTS.md` | L2 | Active workspace instructions are required for routing |
| `active skill` | L3 | The active task needs full skill instructions |
| `all skill registry` | L1 | Metadata is enough for routing |
| `session transcript` | SKIP | Full transcript persistence is not authorized |

## Validation

- `signals_have_evidence`: pass [CÓDIGO]
- `mode_matches_capabilities`: pass [CÓDIGO]
- `tier_matches_budget`: pass [CÓDIGO]
- `loading_plan_bounded`: pass [CÓDIGO]

## JSON Report

```json
{
  "schema": "jm-labs.environment-detection.report.v1",
  "environment": {
    "ide": "codex",
    "model": "user-supplied-heavy-context-model",
    "model_tier": "heavy",
    "triad_mode": "sequential",
    "context_budget_tokens": 128000,
    "confidence": 0.94
  },
  "signals": [
    {"id": "s1", "kind": "instruction_file", "source": "workspace/AGENTS.md", "value": "AGENTS instructions present", "evidence_tag": "[CÓDIGO]"},
    {"id": "s2", "kind": "tooling", "source": "active_tools", "value": "read/write/shell/git available", "evidence_tag": "[CONFIG]"},
    {"id": "s3", "kind": "tooling", "source": "active_tools", "value": "subagents false; hooks_or_mcp false", "evidence_tag": "[CONFIG]"},
    {"id": "s4", "kind": "model_context", "source": "user_runtime_context", "value": "context_budget_tokens=128000", "evidence_tag": "[CONFIG]"}
  ],
  "capabilities": {"read": true, "write": true, "shell": true, "subagents": false, "hooks_or_mcp": false, "network": true},
  "decisions": [
    {"id": "d1", "decision": "triad_mode=sequential", "evidence_ids": ["s2", "s3"], "evidence_tag": "[INFERENCIA]"},
    {"id": "d2", "decision": "model_tier=heavy", "evidence_ids": ["s4"], "evidence_tag": "[INFERENCIA]"}
  ],
  "conflicts": [],
  "loading_plan": [
    {"resource": "AGENTS.md", "level": "L2", "reason": "workspace instructions are required", "evidence_ids": ["s1"]},
    {"resource": "active skill", "level": "L3", "reason": "active task requires full instructions", "evidence_ids": ["s2"]},
    {"resource": "all skill registry", "level": "L1", "reason": "metadata is enough", "evidence_ids": ["s2"]},
    {"resource": "session transcript", "level": "SKIP", "reason": "full transcript persistence is not authorized", "evidence_ids": ["s3"]}
  ],
  "validation": {
    "status": "pass",
    "checks": ["signals_have_evidence", "mode_matches_capabilities", "tier_matches_budget", "loading_plan_bounded"]
  },
  "recommendations": ["Use sequential orchestration and keep only the active skill at L3."]
}
```
