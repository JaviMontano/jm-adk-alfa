---
name: context-optimizer-primary
type: execution
version: 2.0.0
description: "Execute the Context Optimizer workflow."
triad:
  lead: "context-optimizer-lead"
  support: "context-optimizer-support"
  guardian: "context-optimizer-guardian"
---

# Context Optimizer — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{active_task}}` | Current task that must retain full fidelity | Yes | User/session |
| `{{loaded_sources}}` | Files, messages, references, and artifacts in context | Yes | User/workspace |
| `{{token_counts}}` | Current and target token budget facts | Yes | User/tooling |
| `{{risk_flags}}` | Sources that must not be evicted | No | User/Guardian |

## Execution Steps
1. Confirm the request is about context budget, lazy loading, compression, or progressive disclosure.
2. Inventory active and inactive sources before recommending changes.
3. Assign L1/L2/L3 loading levels with at most one L3 source.
4. Compress completed artifacts with retention summaries.
5. Reject eviction for active, unresolved, high-relevance, or risk-flagged sources.
6. Compute reduction/utilization metrics from explicit token counts.
7. Validate JSON reports with `scripts/check.sh` before delivery.
