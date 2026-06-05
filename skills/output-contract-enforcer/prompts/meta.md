---
name: output-contract-enforcer-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Output Contract Enforcer skill routing."
---

# Output Contract Enforcer - Meta Prompt

Activate when the user asks to validate an existing artifact against an explicit or discoverable contract.

Do not activate when:

- The user asks to design a schema from scratch.
- The user asks to format a fresh answer.
- The user asks a conceptual question about contracts.
- There is no artifact or contract evidence; return blocked or route to the owning creation skill.

## Routing

1. Confirm the contract and artifact exist.
2. Activate `output-contract-enforcer-lead` for validation.
3. Route broader release decisions to `quality-gatekeeper`.
