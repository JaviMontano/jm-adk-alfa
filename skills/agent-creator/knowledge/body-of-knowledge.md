# Agent Creator - Body of Knowledge

## Canon

Custom agents are best used for repeatable delegated work where the parent
agent benefits from isolated context, a bounded role, and a narrower tool
surface. The generated definition must be self-sufficient because the spawned
agent does not receive the parent conversation by default.

## Agent Versus Alternatives

| Need | Prefer | Reason |
|---|---|---|
| One-off instruction | Inline response | No persistent artifact needed |
| Stable project rule | CLAUDE.md or AGENTS.md source | Applies continuously without spawning |
| Reusable workflow with assets | Skill | Skills package references, scripts, and assets |
| Always-on event reaction | Hook | Runs from events instead of user routing |
| Delegated analysis or production | Agent | Isolated context and explicit tool contract |

## Required Agent Qualities

- The description must say when to spawn the agent, not only what it can do.
- The role must be bounded enough that another agent can identify overlap.
- Tools must follow least privilege and avoid wildcard access.
- The system prompt must include process, output format, constraints, and
  escalation triggers.
- The prompt must not refer to the parent chat, hidden context, or unspecified
  files.
- The generated file path must match the user-approved scope: project-local or
  global.

## Tooling Policy

Read-only agents normally use `Read`, `Glob`, and `Grep`. Add `Bash` only when
the agent must run deterministic inspections. Add `Write` or `Edit` only when
the user explicitly wants the agent to create or modify files.

## Model Selection

| Model | Use For | Avoid When |
|---|---|---|
| `haiku` | Formatting, extraction, checklist verification | Architecture, security, ambiguous trade-offs |
| `sonnet` | Balanced review, generation, refactoring plans | Mission-critical governance or deep architecture |
| `opus` | Complex reasoning, security, multi-system architecture | Simple mechanical checks |

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Trigger specificity | 100% | Description includes WHEN conditions and negative triggers when needed |
| Least privilege | 100% | No wildcard tools; write tools justified by responsibility |
| Self-sufficiency | 100% | Prompt can run without parent chat context |
| Validation Gate pass | 100% | DoD and script validators pass |

## References

- `assets/agent-spec-schema.json`
- `assets/tool-policy.json`
- `assets/model-selection-policy.json`
- `assets/description-trigger-policy.json`
- `references/domain-knowledge.md`
