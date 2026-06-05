# Domain Knowledge - Agent Creator

## Overview

This reference defines the local rules for generating Claude Code custom agent
definitions. It is intentionally offline and deterministic; live installation
or permission mutation is outside the compiler's scope. [EXPLICIT]

## Key Concepts

| Concept | Definition | Relevance |
|---------|-----------|-----------|
| Trigger description | Frontmatter text that tells the parent WHEN to spawn the agent | Prevents over-invocation [EXPLICIT] |
| Isolated context | Spawned agents do not inherit the full parent conversation | Requires self-contained prompts [EXPLICIT] |
| Least privilege | Explicit minimal tool list for the delegated task | Reduces unintended mutation risk [EXPLICIT] |
| Negative trigger | Condition where the parent should not spawn this agent | Prevents noisy routing [EXPLICIT] |
| Scope | Project-local or global destination for the agent file | Separates reusable and repo-specific behavior [EXPLICIT] |

## Best Practices

1. Start by deciding whether an agent is the right artifact. [EXPLICIT]
2. Use a kebab-case name that does not collide with built-ins. [EXPLICIT]
3. Write descriptions as trigger conditions, not capability slogans. [EXPLICIT]
4. Default to read-only tools and add write access only when necessary. [EXPLICIT]
5. Include a constraints section with explicit negative boundaries. [EXPLICIT]
6. Include escalation triggers for uncertainty, destructive actions, or scope
   overlap. [EXPLICIT]
7. Validate with local fixtures before proposing runtime installation. [EXPLICIT]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|-------------|-------------|-------------------|
| `tools: ["*"]` | Grants broad access without intent | Enumerate tools from the policy catalog |
| "Use this agent for anything related to X" | Routes too often | Name concrete trigger phrases and negative triggers |
| Parent-chat references | Spawned agent lacks that context | Make the prompt self-contained |
| Missing output format | Hard to consume downstream | Add a table, checklist, or fenced schema |
| Agent for formatting preference | Over-engineers a simple rule | Use output style or project instructions |

## Integration Points

- This skill may be invoked by orchestrator skills in the pipeline. [EXPLICIT]
- Output format follows deterministic Markdown conventions. [EXPLICIT]
- Runtime installation into `.claude/agents/` requires a separate write action. [EXPLICIT]
