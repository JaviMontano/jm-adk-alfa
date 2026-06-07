# AI Safety Body of Knowledge

## Canon

AI safety work is not a vibe check. It is a traceable map from harm scenarios to
controls, tests, metrics, escalation, and residual risk.

## Required Coverage

- risk taxonomy: harm domain and severity
- controls: mapped to every risk id
- jailbreak tests: attack type, expected action, oracle
- evaluation metrics: unsafe recall, over-refusal, jailbreak block rate
- escalation: owner, channels, criteria

## Anti-Patterns

- critical risk with allow-only action
- guardrail without test oracle
- safety plan without over-refusal metric
- no escalation for high-stakes or private-data cases
