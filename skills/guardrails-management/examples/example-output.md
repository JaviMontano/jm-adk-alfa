<!--
generated-by: scripts/scaffold-skill.py
generated-for: guardrails-management
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The utterance proposes a durable guideline because it uses "always" and applies
to future JM Labs outputs. [CONFIG][INFERENCIA]

## Rule Proposal

```json
{
  "id": "GL-002",
  "type": "guideline",
  "rule": "Always include evidence tags on every claim in JM Labs outputs.",
  "scope": "JM Labs user-facing outputs",
  "source": "user-explicit",
  "confirmed_date": "2026-06-06",
  "active": true,
  "evidence_tag": "[CONFIG]",
  "verifiable_check": "Every user-facing claim contains one of [CÓDIGO], [DOC], [CONFIG], [INFERENCIA], or [SUPUESTO].",
  "target_file": "references/guardrails/guidelines.json"
}
```

## Conflict Review

- Duplicate check: no active normalized duplicate was found in the three
  guardrail files. [CÓDIGO]
- Conflict check: no existing constraint forbids evidence tags. [CÓDIGO]

## Confirmation

Proposed confirmation prompt: "Confirmo: ¿quieres guardar esto como guideline
`GL-002` en `references/guardrails/guidelines.json`? Responde sí/no." [CONFIG]

## Storage Action

- Until the user answers yes, no JSON file is modified. [CONFIG]
- If confirmed, append exactly one entry to `references/guardrails/guidelines.json`. [CONFIG]

## Validation

- Rule type, ID prefix, and target file match the classification policy. [DOC]
- Rule has scope, source, active flag, evidence tag, and verifiable check. [DOC]
- Remaining risk: if the user intended a hard constraint instead of a guideline,
  the confirmation prompt must clarify enforcement level before persistence.
  [SUPUESTO]
