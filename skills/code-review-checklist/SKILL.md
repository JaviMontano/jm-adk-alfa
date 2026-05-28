---
name: code-review-checklist
description: Structured code review covering OWASP security, Core Web Vitals performance, Firebase best practices, and TypeScript types
version: 1.0.0
status: production
owner: Javier Montaño
tags: [testing, code-review, owasp, performance, firebase, typescript, best-practices]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 083 — Code Review Checklist {Testing}

## Purpose
Provide a deterministic, repeatable code review process that catches security vulnerabilities, performance regressions, Firebase anti-patterns, and type safety issues before merge. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Objectivity**: Every review item is a binary pass/fail check — no subjective opinions. The checklist is the standard. [EXPLICIT]
2. **Law of Shift Left**: Catch defects at review time, not in production. A review that misses a security flaw is a review failure. [EXPLICIT]
3. **Law of Knowledge Transfer**: Reviews spread codebase knowledge. Every review must have at least one comment explaining WHY, not just WHAT. [EXPLICIT]

## Protocol

### Phase 1 — Security Review (OWASP)
1. No secrets in code (API keys, tokens, passwords) — use env vars or Secret Manager. [EXPLICIT]
2. User input sanitized — XSS prevention via React's default escaping + DOMPurify for dangerouslySetInnerHTML. [EXPLICIT]
3. Firestore rules enforce auth — no open read/write rules in production. [EXPLICIT]
4. CORS configured restrictively — no `*` origins. [EXPLICIT]
5. Dependencies audited — `npm audit` shows zero high/critical. [EXPLICIT]

### Phase 2 — Performance & Firebase
1. No unbounded Firestore queries — `limit()` on every `getDocs()`. [EXPLICIT]
2. No Firestore reads in loops — batch or use `in` queries. [EXPLICIT]
3. Images optimized — WebP format, lazy loading, responsive srcset. [EXPLICIT]
4. Bundle impact assessed — no new dependency > 50KB without justification. [EXPLICIT]
5. Cloud Functions cold start mitigated — minimal imports, lazy initialization. [EXPLICIT]

### Phase 3 — Code Quality & Types
1. No `any` types — use `unknown` + type guards if type is uncertain. [EXPLICIT]
2. No `eslint-disable` without JIRA ticket comment. [EXPLICIT]
3. Functions < 50 lines, files < 300 lines — extract if exceeding. [EXPLICIT]
4. Naming is intention-revealing — no abbreviations, no single-letter variables (except loops). [EXPLICIT]
5. Error handling explicit — no swallowed catches, user-facing errors use error boundary. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Pull request diff | Completed checklist (pass/fail per item) |
| Changed files list | Security, performance, quality scores |
| Dependency changes | `npm audit` report |
| Firestore rule changes | Rule coverage verification |

## Quality Gates — 5 Checks

1. **Zero OWASP Top 10 violations** — any finding blocks merge. [EXPLICIT]
2. **No unbounded Firestore queries** — every query has `limit()` or pagination. [EXPLICIT]
3. **TypeScript strict mode** — no `any`, no `@ts-ignore` without ticket. [EXPLICIT]
4. **Bundle size delta < 50KB** — justify or code-split if exceeding. [EXPLICIT]
5. **All review items addressed** — no unresolved comments at merge. [EXPLICIT]

## Edge Cases

- **Hotfix PRs**: Run abbreviated checklist (security + critical performance only). Full review within 48h.
- **Dependency-only PRs**: Focus on `npm audit`, license check, bundle size delta.
- **Firestore rule changes**: Require integration test proof (skill 080) in PR.
- **Generated code**: Exclude from line-count rules but include in security review.

## Self-Correction Triggers

- Production incident traced to missed review item → add to checklist permanently.
- Review turnaround > 24h → escalate or split PR into smaller changes.
- Same defect found 3x → add automated lint rule to prevent it.
- Reviewer approves without checklist completion → flag in team retro.

## Usage

Example invocations:

- "/code-review-checklist" — Run the full code review checklist workflow
- "code review checklist on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
