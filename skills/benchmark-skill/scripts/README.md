# Benchmark Skill Scripts

Deterministic report checks for benchmark-skill.

- `validate_benchmark_report.py`: validates a JSON benchmark report against the
  local rubric, gate policy, net-assessment policy, and report contract.
- `check.sh`: parses all assets and fixtures, then verifies positive and
  negative report scenarios.

The scripts are offline and read only explicit JSON paths supplied to them.
