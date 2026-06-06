# AI Assisted Testing Scripts

`check.sh` validates deterministic AI Assisted Testing plan fixtures offline.

The validator accepts JSON packets that follow
`jm-labs.ai-assisted-testing.plan.v1` and rejects packets that lack evidence,
oracles, bounded fuzzing, mutation baselines, or measurable coverage targets.

Run from the repository root:

```bash
bash skills/ai-assisted-testing/scripts/check.sh
```
