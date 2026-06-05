# Code Review Checklist

Deterministic, read-only checklist for code review and merge readiness across
security, Firebase/performance, and TypeScript/code-quality gates. [CONFIG]

## Triggers

- "code review checklist"
- "PR checklist"
- "pull request checklist"
- "review checklist"
- "OWASP checklist"
- "Firebase review checklist"

## Assets

- `assets/activation-policy.json`: activation and missing-input routing.
- `assets/checklist-taxonomy.json`: checklist IDs, domains, statuses, and
  blocking behavior.
- `assets/evidence-policy.json`: evidence tag and source citation rules.
- `assets/report-contract.json`: machine-checkable report structure.
- `assets/source-boundary-policy.json`: read-only boundaries and hotfix policy.

## Scripts

Run deterministic fixtures:

```bash
bash skills/code-review-checklist/scripts/check.sh
```

The script validates clean, blocking, and invalid report fixtures. [CÓDIGO]

## Output

Reports use:

- `# Code Review Checklist Report`
- `## Scope`
- `## Scores`
- `## Checklist Results`
- `## Findings`
- `## Missing Evidence`
- `## Validation`
- `## Decision`
- `## Risks and Limits`
