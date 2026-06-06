# Session End Cleanup Scripts

The scripts directory provides offline validation for machine-checkable session
closeout reports.

## Commands

```bash
bash skills/session-end-cleanup/scripts/check.sh
python3 -B skills/session-end-cleanup/scripts/validate_session_cleanup_report.py \
  skills/session-end-cleanup/scripts/fixtures/valid-closeout-report.json
```

`check.sh` accepts valid fixtures and rejects negative fixtures. It does not use
network, wall-clock, random data, or files outside this skill directory.
