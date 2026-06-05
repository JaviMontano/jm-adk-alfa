# User Representative

Deterministic review skill for evaluating whether a stakeholder deliverable is understandable, scannable, actionable, and fair to its intended users.

## Activation

Use this skill when the request asks for a user perspective, voice-of-user review, clarity review, cognitive load check, adoption risk assessment, or bias scan of an existing deliverable.

Do not use it as the primary skill for technical correctness, UX copywriting, UI design, requirements writing, or weather/general Q&A.

## Required Input

- Deliverable text or path.
- Target audience, or permission to apply the default personas in `SKILL.md`.
- Any known constraints, success criteria, or stakeholder context.

If the user omits those facts, ask for the missing minimum context or mark the gaps as `[SUPUESTO]`; do not invent a persona, metric, owner, date, or adoption probability.

## Output Contract

Every Markdown review packet must include:

- `# User Representative Review`
- `## Audience`
- `## Evidence Map`
- `## 5-Dimension Scorecard`
- `## Top 5 Micro-Adjustments`
- `## Adoption Risks`
- `## Bias Flags`
- `## Verdict`
- `## Validation`

The verdict is deterministic: `PASS` when all five scores are at least 7, `CONDITIONAL` when one or two scores are 5-6 and none are below 5, and `FAIL` when any score is below 5 or three or more scores are 5-6.

## Assets And Scripts

- `assets/user-representative-checklist.md` defines the review checklist.
- `assets/review-rubric.json` defines dimensions, evidence tags, forbidden inventions, and verdict rules.
- `scripts/validate_user_representative_review.py` validates Markdown review packets against the deterministic contract.

## Local Gates

```bash
bash skills/user-representative/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill user-representative
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill user-representative
```
