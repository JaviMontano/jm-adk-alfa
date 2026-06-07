# Example Output

## System Context

- system: `Payments API`
- scope: production alerting strategy
- risk_level: high

## Evidence

| id | tag | source | summary |
|---|---|---|---|
| E1 | [EXPLICIT] | user input | Duplicate pages and noisy CPU alerts create fatigue. |
| E2 | [EXPLICIT] | user input | Missed authorization failures are critical customer-impacting events. |
| E3 | [EXPLICIT] | user input | Critical failures must page within 5 minutes. |

## Severity Model

| severity | page | target_response | example |
|---|---|---|---|
| critical | true | 5 minutes | authorization failure rate breach |
| high | true | 15 minutes | sustained checkout probe failure |
| medium | false | next business hour | queue depth rising without user impact |
| low | false | weekly review | noisy CPU trend |

## Alert Rules

- payment_authorization_failure_rate: critical, threshold `>2% for 5m`, owner `payments`, oracle `synthetic checkout and payment metrics agree`.
- checkout_probe_failure: high, threshold `3 failed probes in 10m`, owner `SRE`, oracle `probe fails from two regions`.
- queue_depth_growth: medium, threshold `p95 queue depth > baseline x2 for 30m`, owner `platform`, oracle `no critical symptom already paging`.

## Fatigue Controls

- Deduplicate correlated latency, queue, and timeout symptoms behind the highest-severity customer-impacting alert.
- Suppress CPU-only paging unless customer impact or capacity exhaustion is present.
- Review alert volume weekly and retire rules with no action taken in 30 days.

## Validation

- assets
- deterministic_scripts
- quality_criteria
- severity_model
- alert_rules
- escalation_paths
- fatigue_controls
