# Skill Review: acta-formal

Date: 2026-05-28
Reviewer: Codex with three parallel review agents
Status: reviewed and improved
Severity: P1

## Intended Purpose

The skill promises formal meeting records with legal/corporate format, numbered sections, signatures, Markdown/HTML output, and optional distribution.
That means it must produce an acta body, not a generic report, and it must avoid inventing formal facts such as quorum, folio, agreements, attendees, deadlines, or signers.

## Parallel Agent Findings

| Agent | Finding |
|---|---|
| Purpose Auditor | `SKILL.md` had strong intent, but quorum and formal validity were not operable enough to prevent unsupported agreements. |
| Artifact Auditor | README, output template, evals, examples, prompts, and knowledge graph were scaffold-level and contradicted the acta I-VIII contract. |
| QA/Regression Auditor | Evals needed adversarial cases for quorum, no-invention, signers, agenda separation, folio uncertainty, Markdown/HTML parity, false positives, and distribution confirmation. |

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | Activated too broadly on "acta de reunion", referenced an unavailable agenda skill, and lacked hard no-invention/distribution gates. |
| `knowledge/body-of-knowledge.md` | Generic update-safety notes instead of acta-specific hard rules. |
| `templates/output.md` | Generic summary/evidence/result output instead of acta sections I-VIII. |
| `templates/acta-formal.md` | Markdown attendee table lacked the signature column present in HTML. |
| `evals/evals.json` | Activation checks, not formal-document behavior checks. |
| `examples/*` | Placeholder input/output without quorum, attendees, agreements, or signatures. |
| `prompts/*` | Generic workflow that did not force acta metadata, quorum, agreement traceability, or distribution confirmation. |
| `agents/*` | Roles were useful but not strict enough about quorum, no-invention, folio, signatures, and external send/upload gates. |

## User Impact

A vibe coder could receive a polished-looking acta that invents missing facts or treats discussions as approved agreements.
That is worse than an obvious gap because the document looks formal enough to be trusted or distributed.

## Agent Risk

The agent could route informal meeting notes into formal minutes, infer quorum, fabricate a next folio, add signers, complete owners/deadlines, or send an acta externally before human review.

## Improvement Applied

| File | Change |
|---|---|
| `skills/acta-formal/SKILL.md` | Narrowed triggers, removed unavailable `agenda-builder` reference, added no-invention, quorum state, folio placeholder, Markdown/HTML, and external distribution gates. |
| `skills/acta-formal/README.md` | Replaced scaffold with purpose, triggers, minimum inputs, routing boundary, and acta output contract. |
| `skills/acta-formal/knowledge/body-of-knowledge.md` | Added hard rules, required inputs, output contract, quorum safety, and distribution gate guidance. |
| `skills/acta-formal/knowledge/acta-sections.md` | Replaced generic quorum assumption with source-required/no-verificable handling and no-invention rules. |
| `skills/acta-formal/templates/output.md` | Replaced generic output with acta sections I-VIII and validation appendix. |
| `skills/acta-formal/templates/acta-formal.md` | Added signature column and quorum source; aligned section labels. |
| `skills/acta-formal/templates/acta-formal.html` | Added quorum source and aligned section labels with Markdown. |
| `skills/acta-formal/evals/evals.json` | Added 12 purpose-specific cases for quorum, no-invention, signatures, numbering, agenda, agreements, pending items, HTML parity, false positives, and distribution confirmation. |
| `skills/acta-formal/examples/*` | Added realistic junta input and expected acta output. |
| `skills/acta-formal/prompts/*` | Aligned prompt variants to formal acta drafting, validation, and distribution safety. |
| `skills/acta-formal/agents/*` | Specialized lead/support/specialist/guardian responsibilities for acta facts, parity, quorum, folio, signatures, and send/upload gates. |
| `skills/acta-formal/knowledge/knowledge-graph.json` | Replaced scaffold graph with acta-specific contracts and gates. |

## No-Regression Check

Run:

```bash
python3 -m json.tool skills/acta-formal/evals/evals.json >/dev/null
python3 -m json.tool skills/acta-formal/knowledge/knowledge-graph.json >/dev/null
python3 scripts/validate-skills.py --strict
python3 scripts/qa/run-adversarial-tests.py
jq -e '.cases as $c | ($c | length >= 12) and all($c[]; has("id") and has("type") and has("input") and has("expected_behavior") and has("must_include") and has("must_not_include") and has("tags")) and ((["quorum","no_invention","signatures","html_brand","numbering","attendees","agenda","agreements","pending","evidence","false_positive"] - ([ $c[] | .tags[] ] | unique)) | length == 0)' skills/acta-formal/evals/evals.json
rg -n 'generated-by|Example output|realistic project request|Add project-specific|Execute `acta-formal`|Markdown with summary|agenda-builder' skills/acta-formal
git diff --check
```

Expected:

- Skill validation passes.
- Acta evals remain valid JSON.
- Targeted eval coverage check returns `true`.
- Scaffold-debt `rg` returns no matches.
- Ledger reports 524 skills, 6 reviewed, 518 pending after marking this skill reviewed.

## Decision

Improved now.
Next skill in default order: `admin-dashboards`.

## Ledger Completion 2026-06-05

- [CODE] `python3 -B scripts/validate-skill-dod.py --skill acta-formal` returned `dod=pass errors=0`.
- [CODE] Added `assets/README.md`, `assets/manifest.json`, and `assets/deliverable-checklist.md` to satisfy the Alfa DoD asset contract.
- [CODE] `skills/acta-formal/evals/evals.json` now uses the `cases` contract and includes `assets`, `deterministic_scripts`, and `quality_criteria` in `expected_checks` coverage.
- [CODE] `python3 -B scripts/validate-skills.py --strict` returned `skills=585 warnings=0 errors=0` after this closure batch.
- [CONFIG] Ledger status updated to `dod-complete` with decision `completed-assets-dod`.
