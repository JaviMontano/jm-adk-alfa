# Continuous Learning Scripts

`check.sh` validates deterministic continuous learning report fixtures offline.

Run from the repository root:

```bash
bash skills/continuous-learning/scripts/check.sh
```

The validator accepts `jm-labs.continuous-learning.report.v1` packets and rejects
missing prior insight search, incomplete source extraction, duplicate active
insights, invalid amendment candidates, and unsafe update paths.
