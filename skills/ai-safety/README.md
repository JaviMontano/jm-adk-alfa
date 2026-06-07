# AI Safety

Designs deterministic AI safety reports for content filters, output guardrails,
jailbreak prevention, safety evaluation, escalation, and residual risk tracking.

## Triggers

- "AI safety"
- "output guardrails"
- "content filters"
- "jailbreak prevention"
- "safety evaluation"
- "unsafe output mitigation"

## Offline Validation

Run:

```bash
bash skills/ai-safety/scripts/check.sh
```

The validator rejects reports with unknown harm domains, uncovered risks,
critical risks set to allow, missing jailbreak tests, missing metrics, missing
evidence, or incomplete validation checks.
