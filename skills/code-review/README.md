# Code Review

Deterministic code review for supplied diffs, pull requests, patches, or file
excerpts. The skill is read-only, evidence-bound, and validates its report
contract with local fixtures. [CONFIG]

## Triggers

- "code review"
- "PR review"
- "pull request review"
- "review this diff"
- "review this patch"
- "review these changed files"

## Assets

- `assets/activation-policy.json`: activation and non-code refusal rules.
- `assets/review-taxonomy.json`: severities, categories, and decisions.
- `assets/evidence-policy.json`: allowed evidence tags and citation rules.
- `assets/report-contract.json`: required report sections and fields.
- `assets/source-boundary-policy.json`: read-only review boundaries.

## Scripts

Run the deterministic fixture check:

```bash
bash skills/code-review/scripts/check.sh
```

The check validates report JSON fixtures, rejects false approvals with blockers,
and rejects untagged or unevidenced findings. [CÓDIGO]

## Output

Reports use:

- `# Code Review Report`
- `## Scope`
- `## Findings`
- `## Positive Patterns`
- `## Validation`
- `## Decision`
- `## Risks and Limits`

For machine validation, use the JSON shape in
`assets/report-contract.json`. [CONFIG]
