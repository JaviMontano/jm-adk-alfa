---
name: ai-conops-meta
type: meta
version: 2.1.0
description: "Meta-prompt for maintaining deterministic AI CONOPS quality."
---

# AI CONOPS - Meta Prompt

## Evaluate
1. Do evals cover stakeholder gaps, autonomy errors, metric pillar gaps, value quadrant conflicts, and missing degraded modes?
2. Do assets match the offline validator?
3. Do examples include open assumptions and operational modes?
4. Do prompts prevent CONOPS from becoming architecture design too early?
5. Are the three references still aligned with assets?

## Improve
1. Add fixtures for any recurring invalid CONOPS packet.
2. Update assets only when the deterministic policy changes.
3. Keep `scripts/check.sh` offline and reproducible.
4. Update review doc and ledger only after validation evidence exists.
