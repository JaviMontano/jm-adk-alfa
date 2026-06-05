---
name: quality-gatekeeper-quick
type: variation
variant: quick
---
# Quality Gatekeeper Quick Mode

Use when the gate scope is explicit and evidence is already provided.
[EXPLICIT]

Return:

- Decision: `allow`, `block`, or `needs_evidence`.
- Gate and criterion summary.
- Missing evidence and remediation.
- Proposed score-history entry.

Do not skip evidence tags. A quick gate report still fails closed.
