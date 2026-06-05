---
name: task-engine-meta
type: meta
version: 2.0.0
description: "Routes deterministic DSVSR reasoning requests."
---

# Task Engine — Meta Prompt

Activate for complex, ambiguous, high-stakes, multi-domain, confidence-calibrated, or explicitly step-by-step reasoning tasks.

Do not activate full DSVSR for simple factual lookups, live-data questions, or single-step commands unless the user explicitly requests DSVSR or confidence calibration.

Routing:

1. Load `SKILL.md` `## When to Activate`.
2. Load `assets/activation-policy.json`.
3. If complexity signals are fewer than 2 and no confidence target exists, use fast path or route away.
4. If the core problem is missing, ask one clarification question before DSVSR.
