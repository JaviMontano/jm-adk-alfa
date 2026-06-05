---
name: assumption-log-quick
type: variation
variant: quick
---

# Assumption Log Quick Mode

Produce the smallest complete assumption log that still satisfies the local
contract. Keep evidence tags, IDs, statuses, validation queue, and warnings.

Do not skip evidence tagging. If evidence is missing, mark the entry
`unvalidated` with `[ASSUMPTION]` and a concrete validation action.
