# Context Optimizer Scripts

`check.sh` validates deterministic Context Optimizer report fixtures offline.

Run from the repository root:

```bash
bash skills/context-optimizer/scripts/check.sh
```

The validator accepts `jm-labs.context-optimizer.report.v1` packets and rejects
unsafe L3 loading, unsafe eviction, missing retention summaries, and fake token
reduction metrics.
