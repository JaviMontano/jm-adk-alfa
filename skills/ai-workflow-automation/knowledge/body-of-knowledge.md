# AI Workflow Automation — Body of Knowledge

## Canon
- AI workflow automation is a controlled plan: a step graph, actor map, input
  contracts, output contracts, approval gates, handoffs, retries, fallbacks, and
  validation evidence. [DOC]
- AI steps must never be black boxes; they need prompt/input contracts,
  expected output schema, deterministic checks, and escalation criteria. [DOC]
- Human approval gates precede irreversible, external-effect, policy-sensitive,
  or high-risk steps. [DOC]
- Handoffs require owner, artifact, acceptance criteria, and completion signal.
  [DOC]
- Retry policies are bounded; "keep trying" is not a deterministic workflow.
  [DOC]

## Canonical Step Fields

| Field | Purpose |
|-------|---------|
| `id` | Stable step ID |
| `actor` | `human`, `ai`, or `system` |
| `action` | Concrete action |
| `input_refs` | Inputs or artifacts consumed |
| `output` | Artifact produced |
| `owner` | Accountable person/team |
| `risk_level` | `low`, `medium`, `high`, or `critical` |
| `requires_approval` | Boolean gate requirement |
| `deterministic_check` | Offline validation check |
| `retry_limit` | Integer between 0 and 3 |
| `fallback` | Action when retry/validation fails |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Step contract coverage | 100% | Every step has actor, input, output, owner, check |
| Approval coverage | 100% | High/critical and external-effect steps have gates |
| Handoff completeness | 100% | Handoffs have artifact and acceptance criteria |
| Retry determinism | 100% | Retry limits are bounded and fallback exists |
| Evidence coverage | 100% | Claims include allowed evidence tags |

## Anti-Patterns

- "AI decides and sends" without human approval for external effects. [DOC]
- A handoff that names a team but no acceptance artifact. [DOC]
- Retry loops without a stop condition. [DOC]
- Validation that depends on the current time, network, or unverifiable model
  confidence. [DOC]

## References
- `assets/workflow-schema.json`
- `assets/actor-taxonomy.json`
- `assets/approval-gate-policy.json`
- `assets/handoff-policy.json`
- `assets/failure-policy.json`
- `assets/report-contract.json`
