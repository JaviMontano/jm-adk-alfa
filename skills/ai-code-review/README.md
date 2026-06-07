# AI Code Review

AI Code Review produces deterministic, source-backed review reports for diffs,
files, or codebases. It is optimized for exact evidence, false-positive control,
and clear reviewer-ready findings.

## Triggers
- ai-code-review
- ai code review
- AI-assisted review
- review this diff
- automated code review

## Inputs
- Files, directories, patch, PR diff, or review packet target.
- Optional review mode: `quick`, `standard`, `deep`, or `adversarial`.
- Optional constraints: security focus, test focus, migration focus, or generated-file policy.

## Output
Markdown review by default, with an optional JSON packet that follows
`assets/review-report-contract.json`.

Required report sections:
- scope and exclusions
- findings sorted by priority
- file-line evidence
- impact and recommendation
- false-positive notes
- validation commands and remaining risks

## Determinism Rules
- Findings require exact file and line evidence.
- Priorities must follow `assets/severity-policy.json`.
- Runtime claims require `validation.commands_run`.
- Low-confidence issues must be marked `needs-verification`.
- Clean reviews must still record scope, evidence, and validation status.

## Local Validation
Run:

```bash
bash skills/ai-code-review/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ai-code-review
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-code-review
```
