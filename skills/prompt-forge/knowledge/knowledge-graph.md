# Prompt Forge - Knowledge Graph

## Core Concepts

- [[prompt-forge]] - deterministic prompt artifact workflow
- [[playbook]] - required system prompt section contract
- [[source-boundary]] - allowed evidence and unsupported-source behavior
- [[rubric-scorecard]] - ten criteria with repairs for weak scores
- [[platform-portability]] - runtime feature mapping and losses
- [[forge-packet]] - structured validation artifact

## Relationships

```text
prompt-forge
├── create -> playbook + rubric + tests
├── review -> scorecard + prioritized repairs
├── evolve -> preserved contract + rubric delta
├── repair -> failure pattern + surgical fix
└── port -> platform matrix + unsupported features + losses

forge-packet
├── validates: source-boundary
├── validates: playbook sections
├── validates: rubric criteria
└── validates: test coverage
```

## Routing Boundaries

- `prompt-engineering`: choose patterns and design instruction packages.
- `prompt-creator`: write durable prompt files after the forge packet is approved.
- `agent-constitution-creator`: create persistent agent governance documents.

## Tags

#prompt-forge #playbook #prompt-review #prompt-portability #source-grounding
