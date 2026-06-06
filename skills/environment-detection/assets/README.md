# Environment Detection Assets

These assets define deterministic environment detection behavior for the skill.

- `signal-policy.json`: accepted and rejected evidence sources.
- `capability-profile-policy.json`: IDE to triad-mode mapping.
- `model-tier-policy.json`: context budget thresholds.
- `loading-policy.json`: tier-safe bootstrap loading limits.
- `environment-report-contract.json`: required machine-readable report fields.

All policies are offline and static. Do not use network, current time, random values, browser cookies, or account state as detection evidence.
