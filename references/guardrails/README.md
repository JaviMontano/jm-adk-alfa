# Guardrails System

User-declared working rules that Pristino loads as internal RAG at every session.

## Files

| File | Type | Description |
|------|------|-------------|
| `guidelines.json` | Guidelines | Working preferences ("always use TypeScript") — followed by default |
| `constraints.json` | Constraints | Hard rules ("never use jQuery") — never violated |
| `guardrails.json` | Guardrails | Soft boundaries ("prefer functional style") — flexible when justified |
| `tool-policy.json` | Enforcement | **Deterministic** tool-use policy enforced in code by `scripts/pre-tool-guard.sh` (Kata 02). Hot-reloaded on every PreToolUse call; emits a deny before a dangerous Bash command or a write to a protected path runs. Distinct from the three user-RAG files above. |

## How It Works

1. User says something like "from now on, always use TypeScript"
2. Pristino detects the intent to set a rule
3. Pristino asks: **"Should I save this as a working guideline? (yes/no)"**
4. If confirmed, writes to the appropriate JSON file
5. At every session start, Pristino loads all 3 files as context
6. The Guardian (triad) checks compliance with these rules

## Entry Format

```json
{
  "id": "GL-001",
  "rule": "Always use TypeScript for new files",
  "type": "guideline",
  "confirmed": "2026-03-22",
  "source": "user-explicit",
  "active": true
}
```

## Management

- **Add**: `/jm-adk:guardrails add="your rule"`
- **List**: `/jm-adk:guardrails`
- **Remove**: `/jm-adk:guardrails remove=GL-001`

## Types

| Type | Enforcement | Override |
|------|------------|---------|
| **Guideline** | Followed by default | Can be overridden with justification |
| **Constraint** | Never violated | Requires explicit removal to change |
| **Guardrail** | Preferred but flexible | Deviated from when evidence supports it |
