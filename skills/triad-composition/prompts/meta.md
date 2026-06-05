---
name: triad-composition-meta
type: meta
version: 2.0.0
description: "Routes Pristino triad composition requests and rejects unrelated triad meanings."
---

# Triad Composition Meta Prompt

Activate only when the request needs Pristino Lead/Support/Guardian selection, agent orchestration, domain-to-agent mapping, committee escalation, or degraded-mode triad handling.

Do not activate for music triads, chemistry triads, generic three-part lists, or unrelated uses of "composition".

Routing checks:

1. Read `SKILL.md` `## When to Activate`.
2. If activated, load `assets/classification-policy.json`.
3. If false-positive, return no orchestration triad.
4. If missing required inputs, request Goal, Context, Constraints, and Definition of done.
