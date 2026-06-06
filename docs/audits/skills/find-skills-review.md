# find-skills Review

Status: dod-complete; local validation passed.

## SpokeReport: Coordinator
- status: pass
- findings: Branch `codex/harden-find-skills-dod-20260606` is active and was created from `origin/main`. [CÓDIGO][CONFIG]
- coverage_gaps: None at branch creation. [CÓDIGO]
- recommended_changes: Keep scope limited to this skill, review doc, and ledger row. [CONFIG]
- risk: Cross-skill edits would block Guardian. [CONFIG]

## SpokeReport: Ledger Auditor
- status: warn
- findings: Ledger row exists as `pending`; review doc was absent before this hardening. [CÓDIGO]
- coverage_gaps: Ledger cannot be closed until local validations pass. [CONFIG]
- recommended_changes: Update only the `find-skills` row after evidence is complete. [CONFIG]
- risk: Premature `dod-complete` would violate the process. [CONFIG]

## SpokeReport: Determinism Auditor
- status: warn
- findings: Initial DoD failed for missing `assets/`, generic examples, and evals without `cases`. [CÓDIGO]
- coverage_gaps: Needed offline-safe source, scoring, install, and report contracts. [INFERENCIA]
- recommended_changes: Add assets and offline recommendation-report validation. [CONFIG]
- risk: Live marketplaces, install counts, and package installs can make outputs non-reproducible. [INFERENCIA]

## SpokeReport: Eval Designer
- status: warn
- findings: Initial evals were generic and lacked no-match, false-negative, Tier F, auto-install, offline, and bounded-output coverage. [CÓDIGO]
- coverage_gaps: Needed at least 8 deterministic cases covering local-first, remote snapshot, no-match, install safety, security, and boundaries. [CONFIG]
- recommended_changes: Replace evals with DoD-format `cases` and expected checks. [CONFIG]
- risk: Weak evals allow plausible recommendations without evidence or install safety. [INFERENCIA]

## SpokeReport: Script Engineer
- status: warn
- findings: No skill script existed before hardening. [CÓDIGO]
- coverage_gaps: Needed offline validator and fixtures for recommendation reports. [CONFIG]
- recommended_changes: Add `scripts/check.sh`, validator, and fixtures. [CONFIG]
- risk: Without scripts, unsafe auto-install and live remote claims are manually reviewed only. [INFERENCIA]

## SpokeReport: Integrator
- status: pass
- findings: Changes are planned only inside allowed scope. [CONFIG]
- coverage_gaps: Ledger remains pending until validation evidence is recorded. [CONFIG]
- recommended_changes: Run full skill and repo checks before PR. [CONFIG]
- risk: None if scope remains confined. [CONFIG]

## HardeningBrief
- skill: find-skills
- scope_allowed: `skills/find-skills/**`, `docs/audits/skills/find-skills-review.md`, and the `find-skills` ledger row. [CONFIG]
- required_changes: deterministic assets, specialized examples, DoD-format evals, offline validation scripts, fixtures, evidence doc, and ledger closure after validation. [CONFIG]
- forbidden_changes: other skills, global validators, shared repo behavior, adapters, unrelated ledger rows, or automatic skill installation. [CONFIG]
- validation_plan: skill checks, script check, repo checks, doc-factory, adapter freshness, and `git diff --check`. [CONFIG]
- merge_criteria: local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, `main` updated. [CONFIG]

## Evidence
- `bash skills/find-skills/scripts/check.sh` passed with 2 valid fixtures accepted and 6 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill find-skills` passed with `errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill find-skills` passed with `warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/count-components.py --check-docs` passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`. [CÓDIGO]
- `bash scripts/check-repo-boundaries.sh` passed with `Repo boundaries OK`. [CÓDIGO]
- `python3 -B scripts/qa/run-adversarial-tests.py` passed with `passed=11 failed=0 total=11`. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=77 warnings=0 errors=0`. [CÓDIGO]
- `bash scripts/doc-factory/check.sh` passed. [CÓDIGO]
- `bash scripts/adapt.sh all` plus adapter diff check passed with `adapter_diff_status=0`. [CÓDIGO]
- `git diff --check` passed. [CÓDIGO]

## Guardian Decision
- authorized for PR after final diff scope check. [CONFIG]
