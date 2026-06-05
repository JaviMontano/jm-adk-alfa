---
name: benchmark-skill-meta
type: meta
version: 2.1.0
description: "Route only skill-state benchmark requests to benchmark-skill."
---

# Benchmark Skill Meta Prompt

Activate for skill-state comparisons, before/after proof, gap-to-standard
benchmarking, and regression analysis of a skill.

Do not activate for:

- certification/readiness verdicts
- one-state issue discovery
- generic code review
- product/vendor comparison
- runtime behavior testing without skill-state evidence

Routing output:

```json
{
  "expected_activation": true,
  "reason": "[EXPLICIT] request asks for before/after skill benchmark",
  "mode": "version",
  "missing_inputs": []
}
```
