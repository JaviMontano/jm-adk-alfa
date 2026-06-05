# Domain Knowledge — Agent Constitution Creator

## Purpose

An agent constitution converts a requested role into durable governance. It is stricter than a prompt because it records authority, tool access, memory rules, escalation paths, validation discipline, and version control.

## Evidence Tags

| Tag | Use |
|---|---|
| `[EXPLICIT]` | Directly supplied by the user or observed in repository files |
| `[INFERRED]` | Reasonable conclusion from explicit context |
| `[OPEN]` | Missing, conflicting, or unresolved context |

## Authority Rules

- Never grant a tool absent from the registry.
- Never invent a peer agent to own a non-goal or escalation.
- Financial, production, destructive, network, and memory-write authority require explicit approval.
- A conflict between autonomous authority and approval-required authority blocks generation until clarified.

## Interview Mode

Ask for missing:

1. Primary responsibility.
2. Peer agents or confirmation that none exist.
3. Tool registry.
4. Forbidden actions.
5. Memory, security, and escalation constraints.

## Completion Standard

A constitution is complete only when the validator passes and unresolved context is explicitly marked `[OPEN]`.
