---
name: alfa-repo-maintenance-orchestrator
version: 1.0.0
description: "Orchestrates JM-ADK Alfa repository maintenance in fixed safety phases: bootstrap, repo sync audit, local state preservation, isolated branch planning, selective import or consolidation planning, cleanup planning, validation gates, and closeout blockers."
owner: "JM Labs"
triggers:
  - alfa repo maintenance
  - repo sync cleanup orchestrator
  - alfa cleanup workflow
  - systematic repo update
  - maintenance branch plan
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Alfa Repo Maintenance Orchestrator

Use this skill for JM-ADK Alfa maintenance when the work includes repo sync, local cleanup, skill import, branch consolidation, generated index refresh, or PR preparation.

## Fixed Phase Order

Always execute and report these phases in order:

1. `bootstrap`
2. `repo-sync-audit`
3. `local-state-preservation`
4. `branch-plan`
5. `import-consolidation-plan`
6. `cleanup-plan`
7. `validation-gates`
8. `closeout`

The report contract lives in `assets/orchestration-report-contract.json`; the offline checker is `scripts/validate_alfa_maintenance_orchestration.py`.

## Write Blockers

Writes are blocked until all of these are true:

- Baseline is known: repo root, `main`, HEAD, upstream, and status.
- Work is on an isolated non-`main` branch for any mutating phase.
- A preservation manifest exists before import, cleanup, or generated-index writes.
- Cleanup has a cleanup manifest when cleanup actions are planned.
- `no_push` and `no_main_merge` remain true unless the user explicitly changes the policy.

Use `assets/write-blocker-policy.json` to classify blockers.

## Required Integrations

Coordinate these skills by contract, even when they are implemented in separate PRs:

- `repo-sync-auditor`: read-only baseline, remote, branch, and drift evidence.
- `local-state-preservation`: mandatory preservation packet before mutation.
- `workspace-governance`: allowed workspace/archive locations and transient file policy.
- `git-workflow`: isolated branches, no direct `main`, no unsafe resets.
- `safe-scripting-and-bash`: defensive shell execution and dry-run bias.
- `quality-gatekeeper`: validation gates and closeout decision.
- `tasklog-management`: work log, branch intent, and progress evidence.
- `session-end-cleanup`: final state, residual risks, and next actions.

See `assets/integration-matrix.json`.

## Validation Gate Set

The validation phase must include at minimum:

```bash
git status --short --branch
bash scripts/check-repo-boundaries.sh
python3 scripts/count-components.py --check-docs
python3 scripts/validate-skills.py --strict
python3 scripts/validate-skill-dod.py --skill <skill>
python3 scripts/validate-skill-scripts.py --strict --run-checks --skill <skill>
python3 scripts/validate-skill-scripts.py --strict --run-checks
python3 scripts/validate-runtime-instructions.py
python3 scripts/check-devkit-readiness.py
git diff --check main...HEAD
```

Use `assets/validation-gates.json` for machine-checkable gate names.

## Required Output

Produce:

- A JSON orchestration report validated by `scripts/validate_alfa_maintenance_orchestration.py`.
- A human summary using `templates/output.md`.
- Branch/PR sequencing notes, including that this skill can reference `local-state-preservation` as a dependency even when implemented in a prior branch.

## Failure Handling

If a required phase cannot pass, set `next_action` to `blocked` or `pause` and record the reason. Do not reinterpret a missing preservation manifest as a warning when a mutating phase is planned.
