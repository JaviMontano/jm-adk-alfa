# Official Source Verifier Body of Knowledge

## Canon

Official-source verification is a decision gate: a change is authorized only when a primary official source supports the claim that justifies it. Secondary sources can help discovery, but they cannot be the authority for a claim.

## Source Priority

| Source type | Role |
|---|---|
| `official_docs` | Primary authority for product behavior |
| `official_spec` | Primary authority for normative contracts |
| `official_repo` | Authority for source code and release metadata |
| `vendor_blog` | Supporting context only unless explicitly official for the product |
| `secondary` | Discovery only |
| `community` | Discovery only |

## Contract Sections

| Section | Purpose |
|---|---|
| `question` | Decision that needs authority |
| `source_registry` | Source metadata, URL, date, official flag and role |
| `claims` | Claim-level evidence and decision impact |
| `decision` | Whether a change is authorized and what scope it touches |
| `validation` | Machine-checkable proof that official sources govern |
| `guardian` | Final pass/warn/block decision |

## Anti-Patterns

- Citing a blog, forum answer, generated summary or issue comment as the only authority.
- Omitting `accessed_date` for sources whose content may change.
- Authorizing a code or docs change from an unverified claim.
- Mixing official and secondary sources without declaring which one controls the decision.

## Quality Signals

| Signal | Target |
|---|---|
| Official-first | Official sources are checked before secondary sources become evidence |
| Claim coverage | Every verified claim has an official source id |
| Citation hygiene | Every source has URL, publisher and accessed date |
| Decision traceability | Authorized changes map to verified claims |
| Blocked gaps | Missing official evidence blocks change authorization |
| Script offline | `scripts/check.sh` accepts valid fixtures and rejects invalid mutations |
