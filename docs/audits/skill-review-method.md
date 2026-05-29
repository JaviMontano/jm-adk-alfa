# Skill Review Method

Date: 2026-05-28
Scope: `skills/*/SKILL.md`
Mode: one skill at a time, three parallel review agents per skill

## Objective

Review every JM-ADK skill against its intended purpose, then improve one skill at a time with a small, auditable, validation-backed change.

## Review Order

Default order is alphabetical by skill slug from `skills/*/SKILL.md`.
Priority may override order only for P0/P1 safety issues, broken validation, high-use workflows, or explicit maintainer direction.

## Per-Skill Review Contract

For each skill, record:

| Field | Meaning |
|---|---|
| Intended purpose | What the frontmatter and body promise the skill does. |
| Current contract | Inputs, outputs, tools, procedure, templates, examples, evals, and quality gates. |
| Gap | Where the skill is generic, unsafe, unclear, unverifiable, or misaligned. |
| User impact | What a vibe coder or agent user experiences because of the gap. |
| Agent risk | How the gap causes false activation, false confidence, bad tool use, or unreviewable output. |
| Improvement | The smallest useful change that makes the skill more faithful to its purpose. |
| No-regression check | Validator, adversarial test, JSON parse, or targeted command that proves the change. |

## Three-Agent Parallel Review

Use three parallel agents for each skill, but keep write integration centralized.
Only one skill is active at a time.

| Agent | Scope | Output |
|---|---|---|
| Purpose Auditor | `SKILL.md` vs stated finality | Purpose fidelity, missing/weak requirements, severity, recommended improvement. |
| Artifact Auditor | README, templates, evals, examples, prompts, agents, knowledge | Generic vs purpose-specific artifacts, artifact gaps, recommended edits. |
| Regression Auditor | Validators, eval strategy, failure modes | No-regression plan, purpose-specific eval cases, false positives, edge cases. |

The parent agent integrates results and edits files.
Sub-agents should not edit shared files unless a future task assigns disjoint write scopes explicitly.
This avoids merge conflicts and preserves a single review narrative per skill.

## Done Criteria For One Skill

1. The intended purpose is explicit and domain-specific.
2. The procedure tells the agent what to gather, decide, produce, and validate.
3. Outputs have a concrete shape, not only a generic summary.
4. Evals include at least one purpose-specific happy path and one failure/edge case.
5. Examples show the expected deliverable style.
6. Validation passes with `python3 scripts/validate-skills.py --strict`.
7. The review ledger marks exactly that skill as reviewed.

## Ledger

Use:

```bash
python3 scripts/qa/generate-skill-review-ledger.py
```

To mark a completed review:

```bash
python3 scripts/qa/generate-skill-review-ledger.py \
  --mark-reviewed ab-testing \
  --review-doc docs/audits/skills/ab-testing-review.md \
  --severity P2 \
  --decision "improved" \
  --notes "Aligned A/B testing outputs, evals, examples, and quality gates with experiment-design purpose."
```

The ledger lives at `docs/audits/skill-review-ledger.csv`.

## Batch Discipline

Do not mass-edit generated skill text across all skills unless the change is purely mechanical and validated separately.
Domain quality improvements happen one skill at a time.
