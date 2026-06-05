# Agent Constitution Creator — Body of Knowledge

## Canon

An agent constitution is a persistent `agent.md` operating identity. It must define mission, mandate, scope, authority, tools, memory, security, orchestration, delegation, escalation, validation, failure handling, KPIs, dependencies, and version control.

## Deterministic Principles

| Principle | Rule | Validation |
|---|---|---|
| Field completeness | Preserve all 22 headings | `agent-constitution-schema.json` |
| Least privilege | Allowed tools come only from the supplied registry | `authority-policy.json` |
| No invention | Missing agents, tools, approvals, or memory policies become `[OPEN]` | Guardian review |
| Explicit authority | Autonomous and approval-required decisions are separated | Validator |
| Evidence tagging | Context claims use `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` | Validator |

## Anti-Patterns

| Anti-Pattern | Risk | Corrective Action |
|---|---|---|
| "All tools" | Grants unsafe authority | List registry-backed tools only |
| Vague escalation | Cannot route failures | Include trigger, target, and context |
| Empty non-goals | Scope creep | Add at least three exclusions with owners |
| Missing version section | Cannot track governance changes | Add semver and change-control rule |

## Quality Metrics

| Metric | Target | How to Measure |
|---|---|---|
| Required fields | 22/22 | Validator section scan |
| Unsupported permissions | 0 | Tool registry check |
| Failure rows | >= 3 | Validator table scan |
| KPI rows | >= 3 | Validator table scan |
