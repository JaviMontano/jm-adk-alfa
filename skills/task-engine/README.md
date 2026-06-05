# Task Engine

`task-engine` applies deterministic DSVSR reasoning: Decompose, Solve, Verify, Synthesize, and Reflect with calibrated confidence.

## Activation

Use for complex, ambiguous, multi-domain, high-stakes, or explicitly confidence-calibrated reasoning tasks. Do not use full DSVSR for simple factual lookups.

## Deterministic Resources

- `assets/activation-policy.json`: routing between fast path, full DSVSR, and clarification.
- `assets/confidence-scale.json`: confidence bands and evidence requirements.
- `assets/reflection-policy.json`: retry and below-target handling.
- `assets/dsvsr-packet-contract.json`: required output sections.
- `scripts/validate_dsvsr_packet.py`: offline packet validator.

## Local Checks

```bash
bash skills/task-engine/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill task-engine
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill task-engine
```
