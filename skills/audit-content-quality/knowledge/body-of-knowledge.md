# Audit Content Quality Body of Knowledge

## Canon

Content quality for JM-ADK skills is the observable quality of the `SKILL.md`
contract: activation clarity, procedure specificity, quality gates,
anti-pattern coverage, edge-case handling, and traceable evidence.

## Evidence Tags

| Tag | Meaning |
|---|---|
| `[CODE]` | Local file content, command output, or parser result |
| `[CONFIG]` | Asset, manifest, policy, threshold, or declared contract |
| `[DOC]` | Human-readable rubric, documented rule, or source note |
| `[INFERENCE]` | Reviewer conclusion derived from observed evidence |

## Scoring Invariants

- Six dimensions are always scored from `0` to `10`.
- Total score is always out of `60`.
- Grade is formula-derived from percentage.
- Bottom skills are sorted by score, then skill name.
- Systematic gaps require a dimension average below `6.0`.
- Every score needs a rationale tied to observable evidence.

## Anti-Patterns

- Rewarding a section count without checking whether the section is testable.
- Skipping malformed `SKILL.md` files instead of scoring them with evidence.
- Reporting a plugin average while hiding weak individual skills.
- Giving generic remediation such as "improve quality" without naming the weak section.
- Mixing code review, security review, factuality review, or copy review into this rubric.
