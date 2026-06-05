# Agent Constitution Checklist

Use this checklist before delivering or writing `agents/{id}/agent.md`.

- [ ] The agent id is kebab-case and the frontmatter has `id`, `name`, `role`, and semver `version`.
- [ ] The 22 required headings from `agent-constitution-schema.json` are present once and non-empty.
- [ ] Context-derived claims use `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- [ ] Missing context is marked `[OPEN]` or handled through interview mode.
- [ ] `Allowed Tools` contains only tools from the supplied registry.
- [ ] Wildcards, "all tools", and invented permissions are absent.
- [ ] `Decision Rights` separates autonomous actions from approval-required actions.
- [ ] `Security Policy` covers CP1 input, CP2 prompt/instruction, and CP3 output.
- [ ] `Escalation Rules` has trigger, target, and context.
- [ ] `Failure Handling` has at least three detection-response-fallback rows.
- [ ] `KPIs` has at least three metrics with target and unit.
- [ ] `scripts/validate_agent_constitution.py` passes.
