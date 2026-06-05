# Code Review Checklist - Body of Knowledge

## Canon

A deterministic checklist is a gate matrix, not a general opinion. Each item is
`pass`, `fail`, `not_applicable`, or `not_verified` based on supplied evidence.
Blocking failures control merge decision.

## Domains

| Domain | Checks | Blocking focus |
|---|---|---|
| Security | `SEC-01` through `SEC-05` | secrets, XSS, rules, CORS, high audit findings |
| Firebase/performance | `FB-01`, `FB-02`, `PERF-03`, `PERF-04`, `FB-05` | unbounded reads and loop reads |
| Quality/types | `QUAL-01` through `QUAL-05` | unsafe `any` and undocumented suppressions |

## Evidence Rules

- Every checklist item cites source file and line when code evidence exists.
- Missing artifacts become `not_verified` or `needs_context`.
- Safe JSX escaping is not an XSS failure.
- Batched, bounded Firestore reads are not loop-read failures.
- Dependency-only PRs may skip unrelated code checks as `not_applicable`.

## Decision Rules

- Blocking failure => `request_changes`.
- Non-blocking failures only => `approve_with_comments`.
- All applicable checks pass plus positive evidence => `approve`.
- Missing minimum inputs => `needs_context`.
