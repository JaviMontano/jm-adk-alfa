# AI Content Detection

AI Content Detection evaluates whether content is likely AI-generated using
evidence-weighted signals, watermark/provenance checks, threshold policy, and
false-positive controls. It reports likelihood, not definitive authorship.

## Triggers
- ai-content-detection
- ai content detection
- detect AI-generated content
- watermark check
- human AI hybrid content review

## Inputs
- Content excerpt or artifact metadata.
- Review purpose and decision context.
- Optional detector outputs, watermark evidence, provenance, or edit history.
- Optional policy constraints for publishing, moderation, education, or compliance.

## Output
Markdown by default, plus optional JSON packet following
`assets/detection-report-contract.json`.

Required report sections:
- content and scope
- evidence register
- scored detection signals
- likelihood assessment and limitations
- watermark/provenance status
- human-AI hybrid strategy
- decision policy and risks

## Determinism Rules
- Do not claim authorship; use likelihood classes.
- Every signal requires evidence.
- Classification must match thresholds.
- Watermark status must be evidence-backed or `not-checked`.
- High-stakes action requires human review.

## Local Validation
Run:

```bash
bash skills/ai-content-detection/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ai-content-detection
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-content-detection
```
