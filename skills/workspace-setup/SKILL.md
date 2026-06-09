---
name: workspace-setup
version: 1.1.0
description: "Design deterministic local workspace profile setup plans with runtime preferences, command policy, privacy boundaries, write safety, evidence, and offline validation."
owner: "JM Labs"
triggers:
  - workspace-setup
  - setup-workspace
  - local-profile
  - workspace-profile
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Workspace Setup

## Purpose

Design a safe local workspace profile setup plan for `.jm-adk.local.json`. The skill produces a deterministic dry-run plan by default, validates runtime preferences, command policy, privacy boundaries, write safety, and evidence, and only permits writes when an explicit apply mode is present.

## Deterministic Contract

Use `assets/workspace-setup-plan-contract.json` and validate plans with `scripts/validate_workspace_setup_plan.py`. A valid plan must include:

- `target_file` exactly `.jm-adk.local.json`.
- `mode` of `dry-run` or `apply`, with dry-run as the default policy.
- Runtime preferences for goal, runtime, autonomy, workspace area, and output format.
- Command policy with allowed, prohibited, and escalation-required command classes.
- Privacy policy proving local-only storage, no secret storage, redaction categories, and a completed secret scan.
- Write policy requiring explicit apply, `.gitignore` coverage, and `--force` for overwrite.
- Evidence entries with approved evidence tags.
- Validation checks for assets, deterministic scripts, quality criteria, runtime preferences, command policy, privacy policy, write policy, and evidence.

## When To Use

- User approves creation of local Alfa profile configuration.
- First-use onboarding has collected goal, runtime, autonomy, command policy, privacy, and output preferences.
- A developer wants reusable local defaults without committing personal state.

## When Not To Use

- User has not approved writing local configuration.
- The request includes secrets or credentials.
- The needed work is a one-shot answer that does not require local profile state.

## Inputs

- Primary goal with Alfa.
- Project/product type and known stack.
- Preferred runtime.
- Autonomy level.
- Commands allowed/prohibited.
- Privacy constraints.
- Workspace area and output format.

## Outputs

- Dry-run preview of `.jm-adk.local.json` unless `mode=apply` is explicit.
- Validated workspace setup plan matching the contract.
- Local profile file only when `--apply` is explicit and overwrite policy passes.
- Setup summary with evidence, validation, and residual risks.

## Workflow

1. Discover: read existing local profile state without printing sensitive content.
2. Analyze: reject secret-like inputs and detect overwrite risk.
3. Plan: build the deterministic setup plan with target file, runtime preferences, command policy, privacy policy, write policy, evidence, and validation checks.
4. Execute: dry-run by default; write only with explicit `--apply`.
5. Validate: run the offline validator before any apply decision.

## Safety Limits

- Never commit `.jm-adk.local.json`.
- Never overwrite without `--force`.
- Never store secrets; use placeholders and policy text.
- Never require network, wall-clock time, random values, or live credentials for validation.
- Never widen command permissions silently.

## Success Criteria

- Dry-run is the default.
- `--apply` creates a valid local profile.
- Existing profile is preserved unless `--force`.
- Secret-like input is rejected.
- Offline validator accepts valid fixtures and rejects unsafe fixtures.

## Fallback

If setup cannot write safely, return the JSON preview and exact command for a later authorized apply.

## Scripts

Run:

```bash
python3 skills/workspace-setup/scripts/validate_workspace_setup_plan.py skills/workspace-setup/scripts/fixtures/valid-dry-run-profile.json
bash skills/workspace-setup/scripts/check.sh
```

## Examples

- Dry-run setup plan for a Codex runtime that requires evidence tags and local-only state.
- Apply setup plan for an existing approved profile only when `force=false` and overwrite is not requested.
