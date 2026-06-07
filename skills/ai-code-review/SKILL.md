---
name: ai-code-review
author: JM Labs (Javier Montaño)
version: 1.0.1
description: >
  Deterministic AI-assisted code review workflow for source-backed findings,
  file-line evidence, false-positive filtering, review report contracts, and
  safe automated suggestion generation. [EXPLICIT]
  Trigger: "ai code review", "AI-assisted review", "review this diff",
  "automated code review"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# AI Code Review
> Source evidence before suggestion confidence.

## TL;DR
Use this skill when the user asks for AI-assisted code review, automated review suggestions, diff review, or review-report generation. Produce a review that is traceable to exact files and lines, separates confirmed findings from hypotheses, and refuses to claim test results without command evidence.

## Deterministic Assets
- `assets/review-report-contract.json` defines the machine-checkable review report packet.
- `assets/severity-policy.json` defines priority, blocking, and escalation rules.
- `assets/evidence-policy.json` defines allowed evidence tags and source requirements.
- `assets/scope-policy.json` defines in-scope file matching and generated-file handling.
- `assets/false-positive-policy.json` defines suppression, confidence, and degradation rules.
- `scripts/validate_ai_code_review_report.py` validates report packets offline.

## Procedure
### Step 1: Activate Intentionally
- Activate only for code review, diff review, static review, AI-assisted suggestion generation, or review report requests.
- Do not activate for unrelated AI writing, weather, project management, or general coding questions unless the user explicitly requests code review.

### Step 2: Establish Review Scope
- Identify reviewed commit, branch, diff, files, or directories.
- Record `scope.includes` and `scope.excludes` in the output contract.
- Treat generated files, vendored files, lockfiles, and snapshots as excluded unless the user explicitly asks to review them.

### Step 3: Gather Evidence
- Read source files before judging behavior.
- Cite exact `file` and `line_start` for every finding.
- Use evidence tags from `assets/evidence-policy.json`.
- If a finding depends on runtime behavior, include command output in `validation.commands_run` or mark the finding as `needs-verification`.

### Step 4: Review With Stable Categories
- Check correctness, security, data integrity, concurrency, performance, maintainability, observability, tests, accessibility, and AI-specific risks when relevant.
- Assign priorities using `assets/severity-policy.json`.
- Use one finding per root cause; group duplicates under the strongest evidence.

### Step 5: Filter False Positives
- Reject findings based only on style preference, broad suspicion, or missing context.
- Downgrade low-confidence issues to `needs-verification`.
- Include `false_positive_notes` when a tempting issue was suppressed.

### Step 6: Produce The Report
- Prefer Markdown for human review and JSON for machine validation.
- JSON packets must follow `assets/review-report-contract.json`.
- Run `bash skills/ai-code-review/scripts/check.sh` before marking local DoD evidence.

## Quality Criteria
- [ ] Every finding has exact file-line evidence.
- [ ] Priority follows the severity policy.
- [ ] False positives and low-confidence claims are filtered or downgraded.
- [ ] Test-pass or test-fail claims cite executed commands.
- [ ] Output includes validation status, remaining risks, and review limits.
- [ ] Machine-readable packets pass `scripts/validate_ai_code_review_report.py`.

## Output Contract
Required top-level JSON fields:
- `schema`: `jm-labs.ai-code-review.report.v1`
- `target`, `scope`, `review_mode`, `evidence`, `findings`, `summary`, `validation`, `risks`

Each finding requires:
- `id`, `priority`, `category`, `status`, `file`, `line_start`, `evidence_id`, `observation`, `impact`, `recommendation`, `confidence`, `false_positive_notes`

## Usage
Example invocations:
- "/ai-code-review review this PR"
- "Run an AI-assisted code review on the current diff"
- "Review this patch for correctness, security, and test gaps"
- "Generate a machine-checkable review report for these files"

## Assumptions & Limits
- Assumes access to the files, diff, or report inputs under review. [EXPLICIT]
- Does not replace maintainer judgment; it produces source-backed review evidence. [EXPLICIT]
- Does not claim tests passed, failed, or reproduced unless commands were executed and recorded. [EXPLICIT]
- Network research is out of scope unless the user explicitly allows it and source attribution is recorded. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty diff or no files | Produce a clean-review packet with scope evidence and no findings. |
| Missing line numbers | Block machine validation until each finding has a stable line. |
| Generated or vendored files | Exclude by default and record the exclusion. |
| High suspicion but weak evidence | Mark `needs-verification`, reduce confidence, and avoid blocking priority. |
| Test status mentioned without commands | Mark validation as `warn` or `block`; do not claim pass/fail. |
| User asks for broad refactor ideas | Separate advisory notes from review findings. |
