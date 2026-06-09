# Subagent Monitor Body of Knowledge

## Canon

`subagent-monitor` turns subagent execution into a typed report. The monitor must never infer success from silence. Every required agent needs exactly one result, and every timeout or failure must be preserved in aggregation.

## Deterministic Report Fields

| Field | Requirement |
|---|---|
| `swarm_id` | Stable slug for the monitored run |
| `agents[]` | Registry of required and optional agents |
| `timeout_policy.per_agent_seconds` | Integer between 1 and 3600 |
| `timeout_policy.uses_wall_clock_evidence` | Must be `false` |
| `results[]` | One typed result per agent |
| `aggregation.status` | `pass`, `warn`, or `block` based on typed results |

## Safety Invariants

- A required agent with `timeout`, `error`, or `block` forces aggregation `block`.
- Optional failures may produce `warn`, but cannot be hidden.
- `result_count` must equal the number of result objects.
- Duplicate agent results are invalid.
- Missing required agent results are invalid.
- Validation is offline and deterministic.

## Quality Signals

| Signal | Target |
|---|---|
| Coverage | Every registered agent has exactly one result |
| Timeout handling | Timeout action is cancel-and-record |
| Partial failure | Blockers and coverage gaps are preserved |
| Evidence | Results and report claims include approved evidence tags |
| Aggregation | Status follows typed results, not narrative optimism |
