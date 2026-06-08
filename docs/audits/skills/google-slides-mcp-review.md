# Google Slides MCP Review

## Status

- [CODE] DoD status: passed local validation on 2026-06-01.
- [CODE] Ownership scope: `skills/google-slides-mcp/**` and this review file only.
- [CONFIG] Ledger update intentionally skipped because this task forbids editing `docs/audits/skill-review-ledger.csv`.

## Evidence Sources

- [DOC] Google Slides API REST reference and method pages for `presentations.create`, `presentations.get`, `presentations.batchUpdate`, `presentations.pages.get`, and `presentations.pages.getThumbnail`.
- [DOC] Google Slides OAuth scopes reference.
- [DOC] Google Workspace MCP developer server guide.
- [DOC] MCP tools specification draft.
- [DOC] Local setup docs: `docs/google-workspace-mcp-setup.md` and `docs/mcp-integration.md`.
- [CODE] Shape references only: `skills/gmail-mcp`, `skills/google-calendar-mcp`, and `skills/google-drive-mcp`.

## Changes Reviewed

- [CODE] Added `assets/` with schema, MCP tool mapping, scope policy, confirmation policy, batchUpdate policy, thumbnail policy, source map, and report template.
- [CODE] Added `scripts/compile-google-slides-mcp.py`, `scripts/check.sh`, script README, and deterministic fixtures.
- [CODE] Replaced scaffold text in examples, evals, prompts, agents, templates, and knowledge files with Slides-specific content.
- [CODE] Added `templates/output.html` for HTML report output.

## Safety Decisions

- [DOC] `drive.file` is the default recommended profile for app-created/opened presentations.
- [DOC] `presentations.readonly` is the read-only Slides-specific alternative when `drive.file` cannot reach the target file.
- [DOC] `presentations` is the Slides-specific mutation alternative when `drive.file` is insufficient.
- [CODE] `presentations.create` and `presentations.batchUpdate` require `human_confirmation.status=confirmed`.
- [CODE] Broad Drive scopes require `scope_exception.reason` in the offline contract.
- [CODE] Thumbnail `contentUrl` is handled as temporary and non-persistent.

## Validation Closed

- [CODE] `python3 -B scripts/validate-skill-dod.py --skill google-slides-mcp` passed with `skill=google-slides-mcp dod=pass errors=0`.
- [CODE] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-slides-mcp` passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CODE] `bash skills/google-slides-mcp/scripts/check.sh` passed with `OK: google-slides-mcp scripts are deterministic and offline`.
- [CODE] `python3 -B -m py_compile skills/google-slides-mcp/scripts/*.py` passed with no output.
- [CODE] `git diff --check` passed with no output.
