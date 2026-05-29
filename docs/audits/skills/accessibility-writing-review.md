# Skill Review: accessibility-writing

Date: 2026-05-28
Reviewer: Codex with three parallel review agents
Status: reviewed and improved
Severity: P1

## Intended Purpose

The skill promises alt text guidelines, plain language, reading level, and inclusive language.
That means it should produce accessible reader-facing copy plus validation notes, not a generic summary or an unbounded accessibility audit.

## Parallel Agent Findings

| Agent | Finding |
|---|---|
| Purpose Auditor | The purpose was clear, but `SKILL.md` was scaffold-level and did not operationalize alt text, plain language, reading level, or inclusive language. |
| Artifact Auditor | Knowledge, templates, examples, prompts, agents, and evals were generic and did not define a useful accessibility-writing deliverable. |
| QA/Regression Auditor | Current evals proved activation only; adversarial evals were needed for hallucinated alt text, unmeasured reading-level claims, link text, error copy, localization, and false positives. |

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | Generic procedure, broad assumptions, and no content-specific validation rules. |
| `knowledge/body-of-knowledge.md` | Placeholder standards language instead of concrete writing patterns and claim-safety rules. |
| `templates/output.md` | Generic summary/evidence/result format rather than reader-facing copy and review tables. |
| `evals/evals.json` | Activation checks, not semantic quality checks. |
| `examples/*` | No realistic input or good output pattern. |
| `prompts/*` | Generic orchestration that could leak evidence tags into final copy. |
| `agents/*` | Generic roles with no responsibility for alt text, language clarity, inclusion, localization, or claim safety. |

## User Impact

A vibe coder could ask for accessible copy and receive broad advice without usable alt text, clearer links, better error messages, localization notes, or explicit limits.
The biggest failure mode is false confidence: invented chart/image details or exact reading-level claims that were never measured.

## Agent Risk

The agent could hallucinate visual details, over-simplify legal or technical meaning, silently rename code/API terms, optimize for SEO instead of accessibility, or mix internal evidence tags into publishable copy.

## Improvement Applied

| File | Change |
|---|---|
| `skills/accessibility-writing/SKILL.md` | Reframed as accessible content review/rewrite skill with alt text decision tree, plain-language rules, inclusive-language boundaries, non-sensory instructions, and mutation limits. |
| `skills/accessibility-writing/README.md` | Added natural triggers, inputs, non-goals, and output contract. |
| `skills/accessibility-writing/knowledge/body-of-knowledge.md` | Added content types, alt text decision tree, plain-language rules, inclusive-language rules, reading-level claim safety, and quality metrics. |
| `skills/accessibility-writing/templates/output.md` | Replaced generic output with scope, content inventory, reader-facing rewrite, alt text, writing changes, validation notes, and risks. |
| `skills/accessibility-writing/templates/output.docx.md` | Aligned DOCX outline with accessible writing report sections. |
| `skills/accessibility-writing/templates/output.html` | Added branded report sections for copy, inventory, alt text, changes, validation, and risks. |
| `skills/accessibility-writing/evals/evals.json` | Added adversarial and purpose-specific evals for alt text, chart no-context, plain language, reading-level claims, inclusive language, structure, links, errors, localization, SEO conflict, evidence separation, and false positives. |
| `skills/accessibility-writing/examples/*` | Added realistic onboarding-page input and expected accessible-writing output. |
| `skills/accessibility-writing/prompts/*` | Aligned quick, deep, primary, and meta prompts to reader-facing copy plus validation boundaries. |
| `skills/accessibility-writing/agents/*` | Specialized lead/support/specialist/guardian responsibilities around copy, alt text, source fidelity, localization, and claim safety. |
| `skills/accessibility-writing/knowledge/knowledge-graph.*` | Replaced scaffold graph with accessible writing concepts and gates. |

## No-Regression Check

Run:

```bash
python3 -m json.tool skills/accessibility-writing/evals/evals.json >/dev/null
python3 -m json.tool skills/accessibility-writing/knowledge/knowledge-graph.json >/dev/null
python3 scripts/validate-skills.py --strict
python3 scripts/qa/run-adversarial-tests.py
jq -e 'length >= 12 and ([.[] | select(.type=="false_positive")] | length >= 2) and all(.[]; has("id") and has("type") and has("input") and has("expected_behavior") and has("tags"))' skills/accessibility-writing/evals/evals.json
jq -e '(["alt-text","plain-language","reading-level","inclusive-language","structure","links","errors","instructions","localization","false_positive"] - ([.[] | (.tags[]?, .type)] | unique) | length) == 0' skills/accessibility-writing/evals/evals.json
git diff --check
```

Expected:

- Skill validation passes.
- Accessibility writing evals remain valid JSON.
- Targeted eval coverage checks return `true`.
- Ledger reports 524 skills, 5 reviewed, 519 pending after marking this skill reviewed.

## Decision

Improved now.
Next skill in default order: `acta-formal`.
