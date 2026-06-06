# Session Lifecycle Management Scripts

`check.sh` validates deterministic session lifecycle decision fixtures offline.

Run from the repository root:

```bash
bash skills/session-lifecycle-management/scripts/check.sh
```

The validator accepts `jm-labs.session-lifecycle-management.report.v1` packets
and rejects blind resume with critical stale results, raw transcript summaries,
shared-state forks, and missing transition reasons.
