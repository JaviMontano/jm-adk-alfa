---
name: code-review
author: JM Labs (Javier Montaño)
version: 1.1.0
description: >
  Perform deterministic, evidence-bound code review on supplied diffs, pull
  requests, patches, or file excerpts. Classify findings with a fixed severity
  and category taxonomy, cite exact file/line evidence, separate blocking from
  non-blocking feedback, and validate the review report with local assets and
  scripts. [EXPLICIT]
  Trigger: "code review", "PR review", "pull request review", "review this diff",
  "review this patch", "review these changed files"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Code Review

## TL;DR

Use this skill to review code changes with deterministic scope, evidence,
severity, category, decision, and remediation rules. The skill is read-only:
it may inspect files, diffs, tests, logs, and CI output, but it does not edit the
review target. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares the assets required by this skill. [CÓDIGO]
- `assets/activation-policy.json` defines activation and refusal routing. [CÓDIGO]
- `assets/review-taxonomy.json` defines fixed severities, categories, and
  release decisions. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and source requirements. [CÓDIGO]
- `assets/report-contract.json` defines the JSON report shape. [CÓDIGO]
- `assets/source-boundary-policy.json` defines allowed inputs and no-write
  boundaries. [CÓDIGO]
- `scripts/check.sh` runs the deterministic report validator against valid and
  invalid fixtures. [CÓDIGO]

## Activation

Activate only when the user asks to inspect code, a pull request, a patch, a
diff, changed files, implementation quality, or review comments for code. Do
not activate for generic product reviews, book reviews, course reviews, or
non-code critique unless the user supplies code artifacts. [CONFIG]

If no code, diff, PR, file path, or repository context is available, produce a
minimum-input request instead of inventing findings. [CONFIG]

## Inputs

Accept one or more of the following:

- PR URL, branch name, commit range, staged diff, patch, or code excerpt.
- Relevant issue, requirement, acceptance criteria, test output, or CI result.
- Explicit review depth: `quick`, `standard`, or `deep`.
- Caller-supplied review date if a dated report is required.

## Review Procedure

1. Establish scope:
   - Identify files, line ranges, diff hunks, tests, and stated intent.
   - Record unavailable artifacts in `minimum_inputs_missing`.
   - Do not rely on unstated intent or invisible files.
2. Classify findings with the fixed taxonomy:
   - Severities: `BLOCKER`, `MAJOR`, `MINOR`, `NIT`.
   - Categories: `correctness`, `security`, `tests`, `performance`,
     `maintainability`, `accessibility`, `api_contract`, `observability`,
     `style`, `positive`.
3. Gather evidence:
   - Every code finding must cite `file`, `line`, `claim`, and `evidence_tag`.
   - Use `[CÓDIGO]` for inspected code/diff/test/CI evidence.
   - Use `[CONFIG]` for repository policy, review standard, or acceptance
     criteria supplied by the user.
   - Use `[INFERENCIA]` only for a reasoned risk that follows from cited code.
4. Apply severity rules:
   - `BLOCKER`: likely correctness/security/data-loss failure, broken contract,
     or required test/CI failure that should block merge.
   - `MAJOR`: material quality or risk issue that should be addressed before or
     near merge but is not an immediate release blocker.
   - `MINOR`: useful improvement with limited risk.
   - `NIT`: style or readability preference that must not block merge unless it
     violates a cited policy.
5. Produce a decision:
   - `request_changes` when at least one `BLOCKER` exists.
   - `approve_with_comments` when only `MAJOR`, `MINOR`, or `NIT` findings exist.
   - `approve` when no blocking or material findings remain and positive
     patterns are recorded.
   - `needs_context` when minimum input is missing.
6. Validate:
   - Run `bash skills/code-review/scripts/check.sh` for the skill fixtures.
   - Run `python3 -B scripts/validate-skill-dod.py --skill code-review` before
     marking the skill complete.

## Output Contract

Preferred machine-checkable output is JSON following
`assets/report-contract.json`. Markdown reports must preserve the same sections:

1. `# Code Review Report`
2. `## Scope`
3. `## Findings`
4. `## Positive Patterns`
5. `## Validation`
6. `## Decision`
7. `## Risks and Limits`

Findings must be ordered by severity (`BLOCKER`, `MAJOR`, `MINOR`, `NIT`), then
file path, then line number. Finding IDs must be gapless as `CR-NNN`. [CONFIG]

## Quality Criteria

- [ ] Scope is explicit and source-bound.
- [ ] No finding lacks file/line evidence unless it is a documented
      context/input gap.
- [ ] Blocking decision matches the severity taxonomy.
- [ ] Style-only concerns are never treated as blockers without a cited policy.
- [ ] Clean-code reports include positive patterns and do not fabricate
      findings.
- [ ] All claims use `[CÓDIGO]`, `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, or
      `[SUPUESTO]` as appropriate.
- [ ] Local deterministic checks pass.

## Anti-Patterns

- Rubber-stamping PRs without reading the diff.
- Blocking a PR for a style preference owned by lint/format tooling.
- Saying "looks good" when required artifacts are missing.
- Fabricating files, tests, CI status, or hidden behavior.
- Echoing real secrets or sensitive values in review output.
- Using current time, web research, randomness, or remote assets unless the user
  explicitly supplies that source and it is cited.

## Related Skills

- `code-review-checklist` for reusable checklist generation.
- `audit-security` for deeper security-specific static audit.
- `quality-gatekeeper` for release gate decision enforcement.
- `assumption-log` for unresolved review assumptions.

## Assumptions & Limits

- This skill reviews supplied evidence; it cannot prove behavior outside the
  inspected code, diff, tests, or CI artifacts. [CONFIG]
- It may recommend tests, but it does not modify target code. [CONFIG]
- It must ask for missing minimum inputs rather than inventing review findings.
  [CONFIG]
