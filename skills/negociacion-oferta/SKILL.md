---
name: negociacion-oferta
version: 0.2.0
description: "Evalua ofertas profesionales con filtros de aceptacion, PIVOTE, evidencia suministrada y contrapropuestas sin presion, numeros inventados ni claims de mercado vivo."
owner: "JM Labs"
triggers:
  - negociacion-oferta
  - evaluar-oferta
  - offer-eval
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Negociacion Oferta

## Purpose

Use this skill when the user needs to compare job, consulting, advisory, or project offers and decide whether to accept, reject, ask questions, or prepare a counterproposal. The skill is deterministic: it scores only the offer facts supplied by the user, applies fixed acceptance filters, and blocks unsupported claims about market rates, competing offers, or guaranteed outcomes.

## Inputs Expected

- Offer facts: name, monthly USD amount or normalized USD amount, work mode, exclusivity, relocation compatibility, and relevant notes.
- User constraints: `floor_usd`, minimum optionality, relocation goal, parallel-stream requirement, and deal breakers.
- PIVOTE dimensions: purpose, income, viability, optionality, traction, and energy, each scored 0 to 10 from supplied facts.
- Evidence list for non-obvious claims: written offer, recruiter statement, contract clause, user preference, documented competing offer, or known constraint.
- Desired output: ranking, decision packet, questions to ask, or counterproposal draft.

## Outputs Expected

- One deterministic offer table with pass/fail filters and PIVOTE score.
- A ranked list of offers that pass every acceptance filter.
- A blocked or partial decision when required evidence is missing.
- A counterproposal plan only when supported by the supplied offer facts.
- Risk notes for pressure language, fabricated leverage, market-data claims, exclusivity, relocation, and hustle culture.

## Procedure

### Discover

Identify the decision target, normalize supplied compensation to monthly USD only when the user provides the conversion, and capture constraints before scoring. If conversion, taxes, equity value, or benefits are needed but not supplied, mark them as open questions instead of inventing them.

### Analyze

Apply `assets/acceptance-filters.json`, `assets/pivote-rubric.json`, `assets/evidence-policy.json`, and `assets/counteroffer-policy.json`. Treat live market benchmarks as out of scope unless the user provides a source.

### Execute

Score every offer with `scripts/score_oferta.py`. Rank only offers that pass all filters. Draft a counterproposal in calm language, anchored to supplied value, scope, constraints, and requested adjustment. Do not create fake competing offers, ultimatums, scarcity pressure, or guaranteed hiring outcomes.

### Validate

Run the deterministic fixture suite:

```bash
bash skills/negociacion-oferta/scripts/check.sh
```

For one decision packet:

```bash
python3 skills/negociacion-oferta/scripts/score_oferta.py --input <packet.json>
```

## Assets

- `assets/acceptance-filters.json`
- `assets/pivote-rubric.json`
- `assets/evidence-policy.json`
- `assets/counteroffer-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- Every offer has required numeric and boolean fields before scoring.
- PIVOTE is computed from six bounded dimensions, not a free-form vibe.
- Each specific claim references supplied evidence or is marked as an open question.
- Counterproposal language is respectful and firm; it avoids FOMO, ultimatums, hustle glorification, and fabricated leverage.
- Offers that fail any hard filter are not ranked as acceptable.
- Missing compensation, exclusivity, relocation, or evidence produces a blocked output instead of a confident recommendation.

## Edge Cases

- No offers: block and request at least one offer packet.
- Salary exactly equals the floor: pass the compensation filter.
- Strong compensation but exclusivity blocks parallel streams: fail unless the user explicitly marks it as an accepted documented exception.
- PIVOTE average above 7 but one dimension below 5: fail the PIVOTE gate.
- User asks to cite market rates without a source: mark as unsupported.
- User asks to pretend there is another offer: block fabricated leverage.
- User asks for aggressive pressure language: rewrite to calm counterproposal language.

## Assumptions and Limits

- This skill is career and negotiation support, not legal, tax, immigration, or financial advice.
- It does not fetch market data, exchange rates, tax tables, or live job-market information.
- It does not decide for the user; it produces a traceable decision packet from supplied constraints.

## Scripts

`scripts/score_oferta.py --input <json>` validates and scores offer packets against acceptance filters, PIVOTE dimensions, evidence policy, pressure language, and counteroffer boundaries. `scripts/check.sh` runs valid, blocked, and invalid fixtures offline.

## Related Skills

- `validar-liquidacion-co`
- `gratitud-post-proceso`
- `proceso-seleccion-orchestrator`

## Evidence Requirements

- Tie compensation, work mode, exclusivity, relocation, benefits, competing-offer leverage, and next-step claims to supplied evidence.
- Mark live market, tax, equity, or immigration assumptions as open questions unless a source is provided.
- Report validation commands and results when a machine-readable packet is used.

## Update-Safety Notes

- Keep scoring deterministic and offline.
- Do not add network calls, wall-clock market data, randomness, or hidden default conversions.
- Preserve user facts and avoid changing other skills during hardening.
