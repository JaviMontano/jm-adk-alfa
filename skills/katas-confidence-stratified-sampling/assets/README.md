# katas-confidence-stratified-sampling Assets

These assets define deterministic acceptance rules for confidence calibration
and stratified sampling reports.

- `confidence-calibration-report-contract.json` defines required report fields.
- `calibration-policy.json` requires labeled validation and empirical buckets.
- `stratified-sampling-policy.json` requires document type and score strata.
- `accuracy-reporting-policy.json` rejects aggregate-only accuracy.
- `routing-policy.json` requires routing by calibrated confidence.
- `evidence-policy.json` defines local evidence requirements.

The offline validator in `scripts/validate_confidence_report.py` uses these
assets as the local contract.
