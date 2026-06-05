# Skill Review: repo-sync-auditor

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/repo-sync-auditor`.
- [CONFIG] Review date: 2026-06-04.
- [CONFIG] Remote ledger row is intentionally deferred; this PR does not modify
  `docs/audits/skill-review-ledger.csv`.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates consumer
  paths.
- [CODE] `assets/git-safety-policy.json` forbids destructive Git operations and
  keeps network refresh explicit.
- [CODE] `assets/ledger-risk-policy.json` defines ledger, review-doc, script,
  and generated-file drift risks.
- [CODE] `assets/sync-audit-schema.json` documents the JSON output contract.
- [CODE] `scripts/audit-repo-sync.py` emits JSON or Markdown without fetch,
  reset, rebase, push, or file writes.
- [CODE] `scripts/check.sh` verifies JSON shape, Markdown evidence tags,
  non-git failure behavior, and read-only working-tree preservation.
- [CODE] `evals/evals.json` includes concrete branch, ledger, dirty-tree,
  staging-PR, generated-file, and unsafe-request cases.
- [CODE] Examples, knowledge, prompts, and templates now describe repository
  truth auditing instead of scaffold output.

## Validation Commands

```text
bash skills/repo-sync-auditor/scripts/check.sh
OK: repo-sync-auditor reports repo drift read-only

python3 -B scripts/validate-skill-dod.py --skill repo-sync-auditor
PASS repo-sync-auditor: OK: repo-sync-auditor reports repo drift read-only
skills_with_scripts=1 warnings=0 errors=0
skill=repo-sync-auditor dod=pass errors=0

python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill repo-sync-auditor
PASS repo-sync-auditor: OK: repo-sync-auditor reports repo drift read-only
skills_with_scripts=1 warnings=0 errors=0
```

## Residual Limits

- [INFERENCE] The script uses local refs only. Run an explicit fetch first when
  a fresh remote network baseline is required.
- [INFERENCE] The script diagnoses ledger drift but does not update the ledger.
- [INFERENCE] Exact GitHub PR merge state still requires `gh pr view` or API
  evidence when local refs are not enough.
