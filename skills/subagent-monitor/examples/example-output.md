# Example Output

## Summary

Deterministic monitor report for `skill-hardening-session`; all three agents produced typed results and aggregation is `pass`.

## Evidence

- Timeout policy is bounded to 300 seconds per agent. `[CONFIG]`
- All agent results are present. `[CÓDIGO]`
- Aggregation status is derived from typed results, not inferred from silence. `[DOC]`

## Result

```json
{
  "schema": "jm-labs.subagent-monitor.report.v1",
  "skill": "subagent-monitor",
  "swarm_id": "skill-hardening-session",
  "task": "Audit one active skill and aggregate spoke reports",
  "agents": [
    {"id": "coordinator", "role": "coordinator", "required": true},
    {"id": "determinism-auditor", "role": "auditor", "required": true},
    {"id": "guardian", "role": "guardian", "required": true}
  ],
  "timeout_policy": {
    "per_agent_seconds": 300,
    "action": "cancel-and-record",
    "uses_wall_clock_evidence": false,
    "sequence_based": true
  },
  "results": [
    {"agent_id": "coordinator", "status": "pass", "result_type": "spoke_report", "sequence": 1, "evidence_tag": "[CÓDIGO]"},
    {"agent_id": "determinism-auditor", "status": "pass", "result_type": "spoke_report", "sequence": 2, "evidence_tag": "[CÓDIGO]"},
    {"agent_id": "guardian", "status": "pass", "result_type": "guardian_decision", "sequence": 3, "evidence_tag": "[CONFIG]"}
  ],
  "aggregation": {
    "status": "pass",
    "partial_failure_policy": "block-on-required-agent-failure",
    "blockers": [],
    "coverage_gaps": [],
    "result_count": 3
  },
  "evidence": [
    {"claim": "Every required agent produced exactly one typed result.", "evidence_tag": "[CÓDIGO]", "source": "results"}
  ],
  "validation": {
    "status": "pass",
    "offline": true,
    "network_required": false,
    "deterministic": true,
    "checks": [
      "assets",
      "deterministic_scripts",
      "quality_criteria",
      "timeout_policy",
      "typed_results",
      "aggregation_policy",
      "partial_failure_handling",
      "evidence_required"
    ]
  }
}
```

## Validation

- `bash skills/subagent-monitor/scripts/check.sh` must pass before reporting the monitor summary.

## Risks and Limits

- This report validates the monitor contract, not the quality of each subagent's domain analysis.
- Wall-clock timestamps may be logged elsewhere, but they are not accepted as the only evidence.
