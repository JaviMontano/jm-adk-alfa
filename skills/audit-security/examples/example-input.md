# Example Input

Run a static plugin security audit for `evals/fixtures/security-sample-plugin`.

Observed files:

- `plugin.json` line 6 contains a live-looking `sk-proj-*` value.
- `.claude-plugin/plugin.json` line 9 calls a parent directory with `../`.
- `hooks/hooks.json` line 5 has `/Users/deonto/plugin-hook.sh`.
- `hooks/hooks.json` line 7 uses `eval $USER_INPUT`.
- `credentials.json` exists at the plugin root.
- `scripts/install.sh` line 3 uses `curl` without checksum verification.
- `README.md` line 4 contains documentation placeholder `<YOUR_TOKEN>`.

Return a read-only report with all six scan categories, severity counts,
findings, false-positive notes, remediation plan, and coverage.
