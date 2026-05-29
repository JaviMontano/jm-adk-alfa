---
name: workspace-setup
version: 1.0.0
description: "Safe local workspace profile setup with runtime preferences, command policy, privacy boundaries, and quality checklist."
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

- Dry-run preview of `.jm-adk.local.json`.
- Local profile file only when `--apply` is explicit.
- Setup summary and next task prompt.

## Workflow

1. Discover: read existing local profile state without printing sensitive content.
2. Analyze: reject secret-like inputs and detect overwrite risk.
3. Execute: dry-run by default; write only with `--apply`.
4. Validate: confirm generated profile is local-only and JSON valid.

## Safety Limits

- Never commit `.jm-adk.local.json`.
- Never overwrite without `--force`.
- Never store secrets; use placeholders and policy text.

## Success Criteria

- Dry-run is the default.
- `--apply` creates a valid local profile.
- Existing profile is preserved unless `--force`.
- Secret-like input is rejected.

## Fallback

If setup cannot write safely, return the JSON preview and exact command for a later authorized apply.

## Examples

- `python3 scripts/setup-workspace-profile.py --dry-run`
- `python3 scripts/setup-workspace-profile.py --apply --runtime Codex --autonomy "propose diffs before edits"`
