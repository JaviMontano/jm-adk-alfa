---
name: agent-constitution-creator
version: 1.0.0
description: >-
  Use when the user asks to create an agent constitution, define persistent
  agent identity, write agent.md, generate an agent governance spec, or add a
  constitution-grade agent to a multi-agent ecosystem. Produces deterministic
  agent.md constitutions with 22 required fields covering identity, authority,
  governance, quality, validation, and version control.
argument-hint: agent-id [role-description]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---
# Agent Constitution Creator

Create deterministic `agents/{id}/agent.md` constitutions for multi-agent ecosystems. A valid constitution has exactly the 22 required field sections, traceable context, explicit authority boundaries, least-privilege tools, and a versioned completion contract.

## When to Activate

Activate for requests such as:

- "create an agent constitution"
- "define agent identity"
- "write agent.md"
- "generate agent spec"
- "design agent governance"
- "add an agent for X" when the user needs persistent operating identity, tools, authority, and governance

Do not activate for lightweight Claude Code subagent metadata only. Route that request to `agent-creator` and explain the routing boundary.

## Deterministic Contract

- Use `assets/agent-constitution-template.md` as the output skeleton.
- Use `assets/agent-constitution-schema.json` as the 22-field contract.
- Use `assets/authority-policy.json` before assigning tools, agents, memory rights, escalation targets, or autonomous decisions.
- Run `scripts/validate_agent_constitution.py` on any generated `agent.md` before marking the work complete.
- Never invent tools, peer agents, registries, memory keys, security checkpoints, APIs, or approval rights. If context is missing, ask for it or mark the field `[OPEN]`.
- Use a caller-provided `{{CONSTITUTION_DATE}}` token for rendered templates; do not derive dates from wall-clock time inside the skill.

## Required Inputs

Minimum context before generation:

1. Agent id in kebab-case.
2. Primary role or responsibility.
3. Known peer agents or confirmation that none exist.
4. Tool registry or explicit statement that no tools are available.
5. Security, memory, and escalation constraints.

If any item is absent, enter interview mode and ask only for the missing fields. Do not produce `agents/{id}/agent.md` prematurely.

## Context Harvest

1. Search existing constitutions with `Glob agents/*/agent.md`.
2. Read matching peer agent files to identify scope overlap and escalation paths.
3. Read tool registry, security policy, memory policy, or project `AGENTS.md` when present.
4. Build a source map with `[EXPLICIT]`, `[INFERRED]`, and `[OPEN]` tags.
5. If another agent's scope overlaps materially, stop generation and propose merge, split, or explicit mutual non-goals.

## The 22 Fields

Identity:

1. Mission
2. Mandate
3. Scope

Authority:

4. Non-Goals
5. Inputs
6. Outputs
7. Decision Rights
8. Allowed Tools
9. Forbidden Tools

Governance:

10. Memory Policy
11. Security Policy
12. Orchestration Policy
13. Delegation Rules
14. Escalation Rules
15. Tone / Output Style

Quality:

16. Validation Discipline
17. Meta-Cognition Protocol
18. Failure Handling
19. Completion Criteria
20. KPIs
21. Dependencies
22. Version

## Generation Rules

- Write to `agents/{id}/agent.md` only when the user asks for a file update. Otherwise return the Markdown body.
- The frontmatter must include `id`, `name`, `role`, and semver `version`.
- Each required field must be a top-level Markdown heading and contain specific, non-placeholder content.
- `Decision Rights` must separate `Autonomous` from `Requires approval`.
- `Allowed Tools` must list only explicit names from the supplied registry. No wildcards, "all tools", or invented tools.
- `Forbidden Tools` must explicitly deny likely overreach such as network, shell, write, payment, deploy, or deletion powers when those are not in scope.
- `Security Policy` must cover CP1 input, CP2 prompt/instruction, and CP3 output validation.
- `Escalation Rules` must include trigger, target, and context.
- `Failure Handling` must include at least three rows with detection, response, and fallback.
- `KPIs` must include at least three metrics with target and unit.
- `Version` must include current semver and change-control rule.

## Output Template

Use `assets/agent-constitution-template.md`. Keep its 22 headings intact. Substitute only from user-provided or repo-observed context and retain `[OPEN]` where context is missing.

## Validation Gate

Before delivery:

- [ ] `scripts/validate_agent_constitution.py --schema assets/agent-constitution-schema.json --constitution <agent.md>` passes.
- [ ] All 22 fields are present and non-empty.
- [ ] Frontmatter is valid and semver is present.
- [ ] No placeholder tokens, `TODO`, `TBD`, wildcards, or "all tools" claims remain.
- [ ] All tools are registry-backed and least privilege.
- [ ] Overlap, missing context, and conflicting authority are handled by clarification, not invention.
- [ ] Evidence tags distinguish `[EXPLICIT]`, `[INFERRED]`, and `[OPEN]` claims.
