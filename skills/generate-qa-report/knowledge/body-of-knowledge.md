# Generate QA Report - Body of Knowledge

## Canon

A QA report is a reconciliation artifact. It should not invent audit results or silently drop missing dimensions. Counts, severities, source coverage, and recommendations must be traceable to source runs.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Source coverage | 100% | complete, partial, or blocked per QA dimension |
| Count reconciliation | 100% | summary totals equal findings list |
| TL;DR length | exactly 3 | three distinct lines |
| Finding schema | 100% | severity, category, component, description, recommendation, evidence |
| Recommendation ranking | 100% | ranks are sequential and reference findings |
| Evidence coverage | 100% | source, finding, validation, and risk claims tagged |

## References
- `references/report-format-spec.md`
- `assets/report-contract.json`
- `assets/severity-policy.json`
- `assets/source-policy.json`
