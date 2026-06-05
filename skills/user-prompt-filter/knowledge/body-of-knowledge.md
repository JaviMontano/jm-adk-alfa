# User Prompt Filter - Body of Knowledge

## Canon

Prompt filtering is a pre-execution control. It reduces the chance that unsafe
instructions reach agents, hooks, tools, MCP servers, browser automation, or
shell runners. It does not replace runtime permissions, sandboxing, or human
approval.

## Threat Classes

| Class | Description | Default Action |
|---|---|---|
| Prompt injection | Attempts to override developer, system, or policy instructions | Block |
| Tool override | Attempts to grant tools, bypass approval, or force execution | Block |
| Secret exfiltration | Requests credentials, tokens, private memory, or hidden config | Block |
| Protected-context leakage | Requests hidden prompt, policy, or private workspace data | Block or escalate |
| Destructive action | Requests deletion, irreversible mutation, or bypassed safety checks | Escalate or block |
| Ambiguous authority | Claims authority without verifiable source or asks to impersonate owner | Escalate |
| Benign task | Clear task within allowed actions | Allow |

## Filtering Principles

- Preserve benign user intent where possible.
- Remove control instructions aimed at overriding the agent, tools, or policy.
- Redact secrets from evidence.
- Prefer escalation over guessing when authority or intent is unclear.
- Return downstream constraints, not just a binary decision.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Threat coverage | 100% | Every matched pattern maps to a taxonomy class |
| Secret redaction | 100% | Evidence never prints token-like values verbatim |
| Determinism | 100% | Same input gives same decision and sanitized prompt |
| False positive control | >= 80% | Benign defensive prompts are allowed with constraints |

## References

- `assets/threat-taxonomy.json`
- `assets/risk-scoring-policy.json`
- `assets/sanitization-policy.json`
- `references/domain-knowledge.md`
