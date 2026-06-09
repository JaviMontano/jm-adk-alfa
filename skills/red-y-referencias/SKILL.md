---
name: red-y-referencias
version: 0.2.0
description: "This skill should be used when the user asks to manage a professional reference network, request or audit explicit consent, plan referral follow-ups, map relationship context, decide whether a reference can be contacted, or create an evidence-backed networking handoff."
owner: "JM Labs"
triggers:
  - red-y-referencias
  - referencias
  - networking
  - reference consent
  - referral follow-up
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Red Y Referencias

## Purpose

Manage professional references and networking follow-ups without guessing consent or exposing direct contact details. Convert supplied notes into a deterministic reference packet with evidence IDs, consent status, allowed actions, follow-up cadence, network edges, blockers, and next actions.

Use this skill for relationship tracking and consent-safe referral planning. Do not use it to scrape social networks, enrich contacts, bypass consent, or send messages through live services unless the user separately supplies explicit data and approval.

## Deterministic Contract

Follow `assets/output-contract.json` and validate packets with `scripts/reference_network_validator.py`. The packet must include:

- `as_of` ISO date supplied by the user or report author.
- Evidence records for every consent, relationship, follow-up, and action claim.
- Contacts with `consent_status` from `assets/consent-policy.json`.
- Allowed actions derived only from explicit consent and evidence.
- Follow-up decisions computed from `as_of`, not from the current clock.
- Privacy-safe labels instead of direct email, phone, payment, or private channel details.

## Workflow

1. Inventory supplied evidence and assign stable IDs such as `E-001`.
2. Create contact records with stable IDs such as `C-001`. Use `contact_label`, `relationship`, `consent_status`, `consent_evidence_ref`, `last_contact_date`, and `allowed_actions`.
3. Reject or block any contact action when consent is not `explicit_granted`.
4. Compute stale follow-up from `as_of` and `last_contact_date` using `assets/followup-policy.json`.
5. Build network edges only when both contacts exist and the edge has evidence.
6. Create actions with IDs such as `A-001`, due dates in ISO format, action type from policy, and one evidence reference.
7. Validate JSON with `scripts/reference_network_validator.py` before producing the markdown handoff from `templates/output.md`.

## Output Rules

- Tag claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- Mark the packet `blocked` when consent is missing, relative dates appear, direct contact details are exposed, or follow-up is stale without an action.
- Do not include raw email bodies, phone numbers, private email addresses, or payment identifiers.
- Do not infer willingness to provide a reference from prior friendship, job title, seniority, or social media connection.
- Do not contact or draft as if contact is authorized unless `consent_status` is `explicit_granted`.

## Assets

- `assets/manifest.json` lists deterministic assets.
- `assets/output-contract.json` defines packet structure.
- `assets/consent-policy.json` defines consent statuses and allowed actions.
- `assets/followup-policy.json` defines stale follow-up calculation.
- `assets/privacy-policy.json` defines redaction and contact-detail blockers.
- `assets/network-map-policy.json` defines node and edge requirements.

## Scripts

Run:

```bash
python3 skills/red-y-referencias/scripts/reference_network_validator.py --input <packet.json>
bash skills/red-y-referencias/scripts/check.sh
```

The validator is offline and deterministic. It rejects missing evidence, non-consented contact actions, stale follow-ups without actions, relative dates, duplicate IDs, unresolved network edges, and direct contact details.

## Related Skills

- `onboarding-90-dias`
- `proceso-seleccion-orchestrator`
- `gratitud-post-proceso`

## Stop Conditions

Stop when the user asks to contact a person without explicit consent, enrich contacts from external sources, infer private contact details, or rely on a live mailbox/calendar/social network not already provided as evidence.
