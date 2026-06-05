# Example Output

# Repo Sync Audit

[CODE] Root: `/work/jm-adk-alfa`
[CODE] Branch: `codex/skill-example`
[CODE] HEAD: `abc123`
[CODE] origin/main: `def456`
[CODE] Dirty entries: `0`

## Ledger

[CODE] Ledger rows: `585`
[CODE] Skill directories: `585`
[CODE] Untracked skills: `0`
[CODE] Review docs pending in ledger: `13`
[CODE] Script-backed skills pending in ledger: `13`

## Blockers

- [CODE] `medium` `review_docs_pending`: review docs map to non-complete ledger rows.
- [CODE] `medium` `script_skills_pending`: script-backed skills are not `dod-complete` in the ledger.

## Recommendations

- [INFERENCE] Prefer a dedicated ledger reconciliation PR before trusting cursor counts.
- [INFERENCE] Keep the next skill PR scoped to one skill plus generated indexes.
