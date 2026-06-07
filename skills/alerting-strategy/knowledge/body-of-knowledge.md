# Alerting Strategy - Body of Knowledge

## Canon

Alerting strategy converts telemetry into actionable operational signals. A good alert is owned, thresholded, routed, deduplicated, tied to a runbook, and reviewed for usefulness.

## Quality Metrics

| Metric | Target | How To Measure |
|--------|--------|----------------|
| Actionability | 100% | Every alert has owner, threshold, oracle, and runbook or action |
| Severity coverage | 100% | Critical, high, medium, low, and info are defined or explicitly excluded |
| Escalation coverage | 100% | Every paging alert has primary and backup route |
| Fatigue control | 100% | Deduplication, grouping, suppression, and review cadence exist |
| Offline validation | pass | JSON handoff passes `scripts/validate_alerting_strategy.py` |
