# AI Content Detection Assets

These assets define the deterministic contract for AI content detection reports.

## Files
- `detection-report-contract.json`: required JSON shape for detection reports.
- `signal-taxonomy-policy.json`: allowed signal types and required signal fields.
- `threshold-policy.json`: likelihood-to-classification mapping.
- `evidence-policy.json`: evidence and no-unsupported-claim rules.
- `watermark-policy.json`: watermark/provenance status policy.
- `decision-policy.json`: safe final actions and non-accusatory language.

The offline validator in `scripts/validate_ai_content_detection_report.py`
enforces the same contract against deterministic fixtures.
