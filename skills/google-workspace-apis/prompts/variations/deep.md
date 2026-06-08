---
name: google-workspace-apis-deep
type: variation
version: 2.1.0
description: "Deep Google Workspace API integration architecture mode."
---

# Google Workspace APIs — Deep Mode

## Use When

Use deep mode for production automation, compliance-sensitive workflows, or
cross-service plans that can send messages, create events, change files, or
write document/spreadsheet/presentation content.

## Execution

1. Build the complete service matrix from official methods.
2. Separate REST/client-library and MCP execution surfaces.
3. Prove least-privilege scope choice per operation.
4. Require read-only-first evidence for every mutation.
5. Define idempotency, retry, rollback, and partial-response strategy.
6. Define secret storage and token handling.
7. Run the offline compiler against structured fixtures.
8. Produce a sandbox/live validation plan.

## Output

- Cross-service architecture plan.
- Operation-by-operation scope and MCP mapping.
- Mutation and consent register.
- Test matrix with static, fixture, sandbox, and live-read-only phases.
- Residual risks that require Google-side verification.
