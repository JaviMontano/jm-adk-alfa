---
name: ai-content-detection
author: JM Labs (Javier Montaño)
version: 1.0.1
description: >
  Deterministic AI-generated content detection workflow for probabilistic
  signal analysis, watermark verification, human-AI hybrid strategy, threshold
  policy, false-positive controls, and non-accusatory reporting. [EXPLICIT]
  Trigger: "ai content detection", "detect AI-generated content",
  "watermark check", "human AI hybrid content review"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# AI Content Detection
> Evidence-weighted probabilities, never unsupported accusations.

## TL;DR
Use this skill when the user asks to evaluate whether content may be AI-generated,
to inspect watermark/provenance signals, or to design human-AI hybrid content
review policies. Outputs must describe likelihood, evidence, limitations, and
decision policy without asserting authorship as fact.

## Deterministic Assets
- `assets/detection-report-contract.json` defines the machine-checkable report packet.
- `assets/signal-taxonomy-policy.json` defines allowed signal types and required signal fields.
- `assets/threshold-policy.json` defines classification thresholds and confidence rules.
- `assets/evidence-policy.json` defines evidence requirements and no-unsupported-claim rules.
- `assets/watermark-policy.json` defines watermark/provenance status handling.
- `assets/decision-policy.json` defines allowed actions and non-accusatory language.
- `scripts/validate_ai_content_detection_report.py` validates reports offline.

## Procedure
### Step 1: Activate Intentionally
- Activate for AI-generated content detection, watermark checks, provenance review, or human-AI hybrid content policy.
- Do not activate for general writing, editing, plagiarism detection, SEO, or weather-style unrelated requests.

### Step 2: Establish Scope
- Record content id, content type, reviewed excerpt/source, and review purpose.
- Note whether the user needs policy advice, artifact inspection, or a validated report packet.

### Step 3: Collect Signals
- Use only available offline signals unless the user explicitly authorizes external detectors.
- Allowed signals include stylometry, metadata, watermark/provenance, model-detector output, citation/source integrity, edit history, and disclosure statements.
- Every signal requires evidence and a score from 0 to 1.

### Step 4: Classify Probabilistically
- Apply `assets/threshold-policy.json`.
- Emit `likely-ai`, `mixed`, `likely-human`, or `inconclusive`.
- Keep `authorship_claim` as `not-determined`; the skill reports likelihood, not identity or intent.

### Step 5: Control False Positives
- Prefer `inconclusive` when evidence is weak or contradictory.
- Require human review for any enforcement, moderation, academic, hiring, or compliance action.
- Include limitations and false-positive notes.

### Step 6: Validate
- JSON packets must follow `assets/detection-report-contract.json`.
- Run `bash skills/ai-content-detection/scripts/check.sh` before marking local DoD evidence.

## Quality Criteria
- [ ] Every signal has evidence ids.
- [ ] Classification matches threshold policy.
- [ ] Watermark claims include evidence or are marked `not-checked`.
- [ ] Report does not accuse a person or assert authorship as fact.
- [ ] Decision policy avoids punitive automated action without human review.
- [ ] Machine-readable packets pass `scripts/validate_ai_content_detection_report.py`.

## Output Contract
Required top-level JSON fields:
- `schema`: `jm-labs.ai-content-detection.report.v1`
- `content`, `scope`, `evidence`, `signals`, `assessment`, `watermark`, `decision_policy`, `human_ai_strategy`, `validation`, `risks`

## Usage
Example invocations:
- "/ai-content-detection review this article"
- "Check whether this text is likely AI-generated and explain the limits"
- "Design a watermark and disclosure policy for hybrid human-AI content"
- "Validate this AI-content detection report packet"

## Assumptions & Limits
- Detection is probabilistic and may be wrong. [EXPLICIT]
- The skill does not identify who authored content. [EXPLICIT]
- External detector claims require captured tool output as evidence. [EXPLICIT]
- High-stakes decisions require human review and documented policy. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Short sample | Mark as `inconclusive` unless strong provenance exists. |
| Human edited AI draft | Classify as `mixed` and recommend disclosure strategy. |
| Watermark unavailable | Set watermark status to `not-checked` with reason. |
| Detector score conflicts with metadata | Lower confidence and document contradictory signals. |
| User asks to punish a writer | Require human review and non-accusatory language. |
