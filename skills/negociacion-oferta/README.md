# Negociacion Oferta

`negociacion-oferta` compares professional offers with fixed acceptance filters, six-part PIVOTE scoring, supplied evidence, and safe counterproposal boundaries.

## Triggers

- `negociacion-oferta`
- `evaluar-oferta`
- `offer-eval`

## Deterministic Contract

- Score only user-supplied offer facts.
- Require `floor_usd`, at least one offer, six PIVOTE dimensions, and evidence for non-obvious claims.
- Block fabricated competing offers, market-rate claims without a source, pressure language, and hustle glorification.
- Do not fetch exchange rates, salary benchmarks, tax data, or live hiring information.
- Rank only offers that pass every hard acceptance filter.

## Local Validation

```bash
bash skills/negociacion-oferta/scripts/check.sh
python3 skills/negociacion-oferta/scripts/score_oferta.py --input skills/negociacion-oferta/scripts/fixtures/valid-balanced-counteroffer.json
```

## Assets

- `assets/acceptance-filters.json`
- `assets/pivote-rubric.json`
- `assets/evidence-policy.json`
- `assets/counteroffer-policy.json`
- `assets/output-contract.json`
