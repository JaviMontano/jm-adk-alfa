# Workspace Setup

Designs deterministic local workspace profile setup plans for `.jm-adk.local.json`.

## Use When

- The user approved local profile setup or requested a dry-run preview.
- Runtime, autonomy, command policy, privacy, and output preferences need reusable local defaults.
- Existing local state must be preserved unless explicit overwrite authority exists.

## Do Not Use When

- The request asks to store secrets, credentials, tokens, or raw personal data.
- The user only needs a one-shot answer and no reusable local profile.
- The plan would require network access, live account state, wall-clock time, or random values to validate.

## Required Output

Return a setup plan that can be validated offline:

- target file: `.jm-adk.local.json`
- mode: `dry-run` or `apply`
- profile preferences: goal, runtime, autonomy, workspace area, output format
- command policy: allowed commands, prohibited commands, escalation-required commands
- privacy policy: local-only, no secrets, secret scan performed, redaction categories
- write policy: dry-run default, explicit apply, overwrite requires force, gitignored target
- evidence and validation checks

## Validation

```bash
bash skills/workspace-setup/scripts/check.sh
python3 skills/workspace-setup/scripts/validate_workspace_setup_plan.py skills/workspace-setup/scripts/fixtures/valid-dry-run-profile.json
```
