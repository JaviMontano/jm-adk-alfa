---
name: environment-detection-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the Environment Detection skill."
---

# Environment Detection — Self-Improvement

## Evaluate

1. Do assets still match supported hosts and triad modes?
2. Do fixtures cover new IDE/tool combinations without network dependency?
3. Do unknown/conflict cases degrade to `warn` instead of false `pass`?
4. Do templates include signals, decisions, loading plan, and validation evidence?
5. Do agents block private account/cookie/history evidence?
6. Are related startup/context skills still referenced accurately?

## Improve

1. Add or update policies before changing prose.
2. Add a fixture for every new host, conflict, or degradation path.
3. Update `evals/evals.json` with deterministic expected checks.
4. Re-run `scripts/check.sh` and repository validators.

## Trigger

Run this meta-prompt when:
- A new assistant host, IDE, or tool capability appears.
- Runtime detection produced a wrong mode or tier.
- A report needed network/time/random evidence to pass.
- Startup or context-window policies changed.
