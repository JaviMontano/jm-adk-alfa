# Workflow Forge - Body of Knowledge

## Canon

Workflow Forge turns a process into a slash-command workflow contract. The
contract must be executable by agents and auditable by humans.

## Minimum Workflow Contract

| Contract item | Required behavior |
|---|---|
| Command | Begins with `/` and maps to one workflow |
| Deliverable | Names the artifact or outcome produced |
| Skills | Lists skill IDs used during execution |
| Agents | Lists accountable agents, not generic roles |
| Phases | Starts with clarification/planning and ends with verification |
| Checkpoints | Blocks the next phase when required evidence is missing |
| Quality gates | Defines observable completion criteria |
| Example | Shows how the workflow activates in conversation |

## Phase Design Rules

- Prefer 3-7 phases for maintainability.
- Keep phases sequential unless a workflow explicitly declares safe parallelism.
- Give every phase `inputs`, `outputs`, `agents`, and `checkpoint` fields.
- A checkpoint is not a vibe check; it must be observable.
- The final phase verifies the workflow's own deliverable, not just task effort.

## Failure Modes

| Failure | Signal | Recovery |
|---|---|---|
| Missing command | No slash command in request or spec | Ask for command name before writing |
| Missing deliverable | Outcome is "process" or "help" | Ask for concrete artifact/output |
| Single phase | Only one phase or no checkpoint boundary | Split into clarify, execute, verify |
| Unknown agent | Agent not in available catalog | Mark `[OPEN]` and ask/verify |
| Prohibited stack | AWS, Azure, or Docker appears without scope | Fail closed or flag policy exception |
| Weak gate | Gate cannot be observed | Rewrite as a pass/fail criterion |

## Deterministic Assets

`assets/workflow-forge-schema.json` defines the required spec shape.
`assets/workflow-policy.json` defines phase, stack, and quality rules.
`assets/workflow-output-template.md` defines the stable Markdown sections.
`scripts/compile-workflow-forge.py` validates a JSON spec and renders Markdown
or JSON without external dependencies.

## Quality Metrics

| Metric | Target |
|---|---:|
| Required fields present | 100% |
| Phases with agents, inputs, outputs, checkpoint | 100% |
| Final verification phase present | 100% |
| Unknown references flagged | 100% |
| Prohibited stack references | 0 unless explicitly allowed |
