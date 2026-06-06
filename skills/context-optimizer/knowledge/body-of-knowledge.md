# Context Optimizer — Body of Knowledge

## Canon

Context optimization is a fidelity-preserving budget discipline. It reduces
loaded context by using indexes, summaries, and deferred loading while keeping
the active task and active skill complete.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Active fidelity | 100% | Active task and active skill stay L3 |
| L3 count | <= 1 | Full-load sources in loading plan |
| Reduction | >= 20% when optimizing | Rounded token reduction |
| Utilization | <= target | Optimized tokens / max tokens |
| Safe eviction | 100% | No active, risk-flagged, or high-relevance source evicted |

## Required Concepts

- L1: index-only source for discovery.
- L2: summary source with decisions, evidence, blockers, and next actions.
- L3: full source loaded for active execution.
- Compression: replacing full content with a retention summary.
- Defer: not loading a source until relevance is proven.
- Eviction: removing low-relevance, non-risk context from the active window.
