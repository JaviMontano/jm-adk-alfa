# Agent Creator

Create Claude Code custom agent definitions from a structured contract.

## Triggers

- User asks to create an agent, add a subagent, or build an autonomous
  subprocess.
- User needs a reusable role with isolated context and explicit tools.
- User wants a project-local or global `.claude/agents/{name}.md` definition.

## Allowed Tools

- Read
- Write
- Edit
- Bash
- Glob
- Grep

## Quick Use

1. Decide whether an agent is the correct artifact.
2. Normalize the request into `assets/agent-spec-schema.json`.
3. Compile with `scripts/compile-agent.py`.
4. Validate with `scripts/check.sh` and the repository DoD validators.

## Output Format

Markdown agent definition with frontmatter, self-contained task, process,
output format, constraints, reasoning discipline, quality bar, and escalation
rules.

## Deterministic Assets

- `assets/agent-spec-schema.json` defines the required input shape.
- `assets/tool-policy.json` constrains tool access.
- `assets/model-selection-policy.json` maps complexity to model choice.
- `assets/description-trigger-policy.json` keeps routing descriptions precise.
- `assets/agent-template.md` supplies the canonical section order.
