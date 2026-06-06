# Design Agent — Body of Knowledge

## Canon

`design-agent` produces a reviewable plugin subagent specification. It validates role boundary, frontmatter, skill assignments, execution flows, operating principles, and maxTurns rationale before any deployable agent file is written.

## Deterministic Rules

| Rule | Requirement |
|------|-------------|
| Forbidden fields | Reject `hooks`, `mcpServers`, and `permissionMode`. |
| Tool policy | Use `tools` or `disallowedTools`, never both. |
| Agent name | Require kebab-case. |
| Skill assignments | Every assigned skill needs status and invocation mode. |
| Flow coverage | Every handled command needs steps and a quality gate. |
| Operating principles | Require specific, actionable, verifiable statements. |
| maxTurns | Use `(skills * 4) + complexity_bonus + (interaction_points * 2)`, rounded up to nearest 5. |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Forbidden field count | 0 |
| Flow coverage | 100 percent of handled commands |
| Principle quality | 4-7 specific rules |
| maxTurns mismatch | 0 |
| Offline validation | `scripts/check.sh` passes |
