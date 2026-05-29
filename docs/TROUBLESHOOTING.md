# Troubleshooting

## Repo Not Confirmed

Run:

```bash
git remote -v
python3 scripts/diagnose-first-use.py --dry-run
```

If the repo is not Alfa, stop and ask for the correct path or remote.

## Onboarding Does Not Trigger

Run:

```bash
python3 scripts/diagnose-first-use.py --input hola --json
python3 scripts/validate-onboarding.py
```

Check that `first-use-onboarding-agent`, `first-use-onboarding` skill, and `/jm-adk:first-use` exist.

## Local Profile Already Exists

Run dry-run and review the diff manually before any overwrite:

```bash
python3 scripts/setup-workspace-profile.py --dry-run
```

Use `--force` only after explicit review.

## Runtime Capability Unclear

Use `runtime-routing-agent`. Mark the capability as validation pending and fall back to Markdown-first local workflow.
