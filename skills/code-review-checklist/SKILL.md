---
name: code-review-checklist
description: >
  Apply a deterministic, read-only code review checklist for supplied pull
  request diffs, changed files, dependency updates, Firestore rules, Firebase
  code, TypeScript code, and frontend changes. The checklist covers OWASP-style
  security, Firebase/performance, TypeScript/code-quality gates, exact evidence,
  merge decision rules, and offline report validation. [EXPLICIT]
  Trigger: "code review checklist", "PR checklist", "pull request checklist",
  "review checklist", "OWASP checklist", "Firebase review checklist"
version: 1.1.0
status: production
owner: Javier Montaño
tags: [testing, code-review, checklist, owasp, performance, firebase, typescript, best-practices]
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Code Review Checklist

## Purpose

Use this skill to run a repeatable checklist over supplied code-review evidence.
The skill is read-only: it may inspect code, diffs, rules, package manifests,
test output, CI output, and audit reports, but it does not edit target code.
[CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares every deterministic asset. [CÓDIGO]
- `assets/activation-policy.json` defines activation and missing-input routing.
  [CÓDIGO]
- `assets/checklist-taxonomy.json` defines fixed checklist IDs, domains,
  blocking behavior, statuses, and decision rules. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and required source
  fields. [CÓDIGO]
- `assets/report-contract.json` defines the JSON report shape. [CÓDIGO]
- `assets/source-boundary-policy.json` defines read-only scope, hotfix handling,
  and forbidden behaviors. [CÓDIGO]
- `scripts/check.sh` runs deterministic validator fixtures. [CÓDIGO]

## When To Activate

Activate when the user asks for a code review checklist, PR checklist, OWASP
review, Firebase review, TypeScript review checklist, performance review
checklist, or merge-readiness checklist for code artifacts. [CONFIG]

Do not activate for generic product reviews, book reviews, service reviews, or
non-code checklists unless the user supplies code artifacts. If no code, diff,
PR, branch, rules file, package manifest, test output, or audit report is
available, return `needs_context` with minimum inputs instead of inventing
checklist results. [CONFIG]

## Checklist Domains

### Security

- `SEC-01`: No secrets in code; use environment variables or Secret Manager.
- `SEC-02`: User-controlled HTML is sanitized before `dangerouslySetInnerHTML`.
- `SEC-03`: Firestore rules enforce authentication and least privilege.
- `SEC-04`: CORS does not allow wildcard origins for production endpoints.
- `SEC-05`: Dependency audit has no high or critical vulnerabilities.

### Performance And Firebase

- `FB-01`: Firestore reads use `limit()`, pagination, or a bounded query plan.
- `FB-02`: Firestore reads are not executed inside unbounded loops.
- `PERF-03`: Images use optimized formats, lazy loading, or responsive sizing
  when image changes are in scope.
- `PERF-04`: New dependencies above 50KB are justified or split.
- `FB-05`: Cloud Functions minimize cold-start cost through scoped imports or
  lazy initialization.

### Quality And Types

- `QUAL-01`: No new `any` types without a documented boundary and type guard.
- `QUAL-02`: No `@ts-ignore`, `eslint-disable`, or suppression without ticket
  or policy evidence.
- `QUAL-03`: Changed functions/files remain within stated size policy unless
  generated code or documented exception applies.
- `QUAL-04`: Naming is intention-revealing for changed public code.
- `QUAL-05`: Error handling is explicit; catches are not silently swallowed.

## Output Contract

Preferred output is JSON matching `assets/report-contract.json`. Markdown
reports must preserve these sections:

1. `# Code Review Checklist Report`
2. `## Scope`
3. `## Scores`
4. `## Checklist Results`
5. `## Findings`
6. `## Missing Evidence`
7. `## Validation`
8. `## Decision`
9. `## Risks and Limits`

Every checklist result must include `id`, `domain`, `status`, `evidence_tag`,
`source.file`, `source.line`, and `why`. Status values are `pass`, `fail`,
`not_applicable`, and `not_verified`. [CONFIG]

## Validation Gate

- Any failing security item (`SEC-*`) blocks merge. [CONFIG]
- Failing `FB-01`, `FB-02`, `QUAL-01`, or `QUAL-02` blocks merge. [CONFIG]
- Missing minimum input produces `needs_context`, not a guessed checklist.
  [CONFIG]
- Clean PRs must include positive evidence and must not fabricate findings.
  [CONFIG]
- Hotfix reviews may run only security plus critical Firebase/performance gates,
  but must record a full-review follow-up within 48 hours. [CONFIG]
- Reports must pass `bash skills/code-review-checklist/scripts/check.sh` before
  this skill can be marked complete. [CÓDIGO]

## Decision Rules

- `request_changes`: one or more blocking checklist failures.
- `approve_with_comments`: non-blocking failures only.
- `approve`: no failures, no missing required evidence, and positive evidence
  exists.
- `needs_context`: minimum inputs are missing.

## Anti-Patterns

- Treating style preferences as blockers without policy evidence.
- Approving despite a failed security, unbounded Firestore, `any`, or
  unapproved suppression gate.
- Treating safe React JSX escaping as an XSS finding.
- Flagging batched Firestore reads as loop reads.
- Loading remote assets or using implicit current dates in report templates.
- Using `Write` or `Edit` tools while performing checklist review.

## Assumptions & Limits

- The checklist validates supplied artifacts only. [CONFIG]
- It cannot prove runtime safety outside inspected code, tests, CI, rules, audit
  output, or user-supplied evidence. [CONFIG]
- It complements `code-review`; it does not replace deeper implementation
  review or `audit-security` for specialized security audits. [CONFIG]
