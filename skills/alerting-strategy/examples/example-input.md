# Example Input

Design an alerting strategy for `Payments API`.

Context:
- Incidents: duplicate pages for latency spikes, noisy CPU alerts, and missed critical payment authorization failures.
- Signals: p95 latency, error rate, payment authorization failure rate, queue depth, dependency timeout rate, and synthetic checkout probe.
- Teams: platform owns infrastructure, payments owns API behavior, SRE owns paging policy.
- Constraints: critical customer-impacting failures must page within 5 minutes; warning alerts should route to business-hours triage; duplicate pages must be suppressed for correlated symptoms.

Produce severity classification, alert rules, escalation paths, fatigue controls, routing policy, validation checks, and residual risks.
