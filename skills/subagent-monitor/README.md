# Subagent Monitor

Produces deterministic monitoring reports for subagent execution, timeouts, typed results, and aggregation.

## Use When

- A task dispatches multiple subagents or spoke agents.
- The coordinator needs one report covering status, timeouts, blockers, and partial failures.
- The result must prove that every agent either completed, warned, blocked, failed, or timed out.

## Do Not Use When

- There is only one direct task and no subagent lifecycle to monitor.
- The desired output depends on live wall-clock timing as evidence.
- The caller wants to hide failed or timed-out agents and still report success.

## Required Output

Return a JSON-compatible monitor report with:

- `swarm_id`
- task summary
- agent registry
- timeout policy
- typed results
- aggregation summary
- evidence entries
- validation checks

## Validation

```bash
bash skills/subagent-monitor/scripts/check.sh
python3 skills/subagent-monitor/scripts/validate_subagent_monitor_report.py skills/subagent-monitor/scripts/fixtures/valid-complete-swarm.json
```
