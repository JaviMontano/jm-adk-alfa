# Generate Qa Report

`generate-qa-report` aggregates validation and audit outputs into a deterministic Markdown QA report. It does not invent findings; it reconciles source runs, counts severities, writes an exact 3-line TL;DR, and prioritizes recommendations from evidence-backed findings.

## Deterministic Inputs

- Validation/audit outputs from structure, manifest, components, hooks, cross-reference, security, and content-quality checks.
- Plugin metadata such as name, version, path, and component counts.
- Optional partial-source acknowledgement when not all QA dimensions were run.

## Deterministic Output

The report must include:

- report metadata and source coverage;
- summary statistics whose counts match the findings list;
- exactly three TL;DR lines;
- categorized findings with severity, component, description, recommendation, and evidence tag;
- category status table;
- top recommendations ranked by severity and impact;
- validation notes and residual risks.

## Offline Contract

Run the deterministic fixture validator:

```bash
bash skills/generate-qa-report/scripts/check.sh
```
