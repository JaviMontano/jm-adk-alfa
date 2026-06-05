# Agent Constitution Creator

`agent-constitution-creator` produces deterministic `agents/{id}/agent.md` constitutions for multi-agent ecosystems.

## Activation

Use this skill when the request asks for persistent agent identity, governance, authority boundaries, tool permissions, escalation rules, or a constitution-grade `agent.md`.

Do not use it for lightweight subagent metadata only; route that to `agent-creator`.

## Required Inputs

- Agent id in kebab-case.
- Role or mission.
- Existing agents or explicit confirmation that none exist.
- Tool registry.
- Security, memory, escalation, and approval constraints.

Missing required inputs trigger interview mode rather than generation.

## Deterministic Resources

- `assets/agent-constitution-template.md`: canonical output skeleton.
- `assets/agent-constitution-schema.json`: required fields, minimum row counts, and blocked phrases.
- `assets/authority-policy.json`: no-invention and least-privilege authority policy.
- `assets/constitution-checklist.md`: human-readable delivery gate.
- `scripts/validate_agent_constitution.py`: offline validator for generated constitutions.

## Local Gates

```bash
bash skills/agent-constitution-creator/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill agent-constitution-creator
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill agent-constitution-creator
```

## Output

The final output is Markdown suitable for `agents/{id}/agent.md`, with 22 top-level field sections, valid frontmatter, explicit permissions, and source-tagged assumptions.
