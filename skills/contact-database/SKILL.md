---
name: contact-database
description: >
  Triggers on "contact database", "contact list", "CRM list", "base de contactos",
  "lista de contactos". Structured contact/CRM list builder with records for name,
  company, role, email, phone, LinkedIn, notes, last contact date, and status.
  Output: CSV template + optional branded HTML contact cards. [EXPLICIT]
argument-hint: "contact records or fields to include, optional: export format, grouping criteria"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# contact-database

## TL;DR

Builds structured contact databases from user-provided data or blank templates. Produces a clean CSV file with standardized fields (name, company, role, email, phone, LinkedIn, notes, last contact date, status) and optionally generates branded HTML contact cards for visual review. Supports bulk import structuring, deduplication guidance, and segmentation by status or category.

## When to Activate

- User asks to create, organize, or template a contact list or CRM database.
- User provides unstructured contact information needing standardization.
- User requests a CSV template for tracking business contacts.
- User mentions "contact database", "contact list", "CRM list", "base de contactos", or "lista de contactos".
- Do NOT activate for client dossier deep-dives (use `client-dossier`), lead generation research (use `lead-generation`), or stakeholder mapping exercises (use `stakeholder-mapping`).

## Contact Record Schema

### Core Fields

Every contact record contains these standardized fields:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | Auto-increment integer | Yes | Unique, sequential |
| `first_name` | Text | Yes | Trimmed, title-case |
| `last_name` | Text | Yes | Trimmed, title-case |
| `company` | Text | Yes | Standardized company name |
| `role` | Text | No | Job title or function |
| `email` | Email | No | RFC 5322 format validation |
| `phone` | Text | No | E.164 format preferred (+CC NNNN) |
| `linkedin` | URL | No | Must start with linkedin.com/in/ |
| `category` | Enum | Yes | CLIENT, PROSPECT, PARTNER, VENDOR, INTERNAL, OTHER |
| `status` | Enum | Yes | ACTIVE, INACTIVE, NURTURING, CLOSED, DO_NOT_CONTACT |
| `notes` | Text | No | Free-form, max 500 chars in CSV |
| `last_contact_date` | Date | No | ISO 8601 (YYYY-MM-DD) |
| `next_action` | Text | No | Brief description of follow-up |
| `next_action_date` | Date | No | ISO 8601 (YYYY-MM-DD) |
| `source` | Text | No | How contact was acquired |
| `created_at` | Datetime | Yes | ISO 8601, auto-populated |

### Extended Fields (Optional)

Users may request additional columns:

- `secondary_email`: backup email address.
- `company_size`: S/M/L/Enterprise enum.
- `industry`: free-text or NAICS code.
- `timezone`: IANA timezone identifier.
- `preferred_language`: ISO 639-1 code (es, en, pt).
- `deal_value`: numeric, currency amount of associated opportunity.
- `tags`: comma-separated labels for flexible grouping.

## CSV Output Specification

The primary output is a UTF-8 CSV file with BOM marker for Excel compatibility:

- **Encoding**: UTF-8 with BOM (`\xEF\xBB\xBF` prefix).
- **Delimiter**: comma (`,`), with proper escaping for fields containing commas.
- **Header row**: always present, using snake_case field names.
- **Quoting**: all text fields double-quoted to handle special characters.
- **Date format**: ISO 8601 (`YYYY-MM-DD`) for universal parsing.
- **Empty fields**: represented as empty quoted strings (`""`), never NULL.
- **Line endings**: CRLF (`\r\n`) for cross-platform compatibility.
- **Filename convention**: `contacts-{context}-{YYYY-MM-DD}.csv`.

## Branded HTML Contact Cards

When the user requests visual output, generate HTML contact cards:

- **Card layout**: CSS Grid, 2-3 cards per row, responsive to viewport width.
- **Brand colors**: JM Labs dark theme (`#0a0a0a` background, `#e94560` accents, `#eaeaea` text).
- **Card structure**: avatar placeholder (initials circle), name, role, company, contact icons with links (email mailto:, phone tel:, LinkedIn href).
- **Status badge**: color-coded pill (green=ACTIVE, amber=NURTURING, gray=INACTIVE, red=DO_NOT_CONTACT).
- **Category tag**: small label in top-right corner of card.
- **Print stylesheet**: grid collapses to single column, cards get borders for clarity.
- **Interactivity**: no JavaScript; pure CSS hover effects for card elevation.

## Data Quality & Deduplication

When processing existing contact data:

1. **Normalize names**: trim whitespace, apply title-case, split first/last correctly.
2. **Normalize companies**: strip legal suffixes for matching (S.A.S., LLC, Inc.) but preserve in output.
3. **Detect duplicates**: flag records sharing (a) same email, (b) same first+last+company, or (c) same phone number. Present duplicates to user for resolution, never auto-merge.
4. **Validate emails**: check format against RFC 5322 pattern (not deliverability).
5. **Validate phones**: strip non-numeric characters, check length plausibility.
6. **Flag incomplete**: mark records missing both email and phone as `INCOMPLETE`.

## Trade-off Matrix

| Decision | Option A | Option B | Default |
|----------|----------|----------|---------|
| Output format | CSV only | CSV + HTML cards | CSV only (HTML on request) |
| Encoding | UTF-8 no BOM | UTF-8 with BOM | UTF-8 with BOM (Excel compat) |
| Dedup behavior | Auto-merge duplicates | Flag for user review | Flag for review (safer) |
| Phone format | Local format | E.164 international | E.164 international |
| Status vocabulary | Custom user-defined | Fixed enum | Fixed enum (consistency) |
| Extended fields | Always include all | Only on request | Only on request (lean CSV) |

## Assumptions & Limits

- **Assumption**: contacts are business/professional, not personal address book entries. [INFERRED]
- **Assumption**: user has legal basis to store contact data (GDPR, HABEAS DATA compliance is user's responsibility). [EXPLICIT]
- **Assumption**: CSV is the universal interchange format; user imports into their own CRM. [EXPLICIT]
- **Limit**: no live CRM integration (Salesforce, HubSpot); output is file-based.
- **Limit**: no email verification or enrichment API calls.
- **Limit**: no automated follow-up scheduling; `next_action_date` is informational only.
- **Limit**: maximum 500 records per generated file for performance.

## Edge Cases

1. **Empty database request**: user asks for a blank template with no contacts. Generate CSV with header row only plus 3 example rows marked `[EXAMPLE]` in notes field, then instruct user to delete examples.
2. **Unstructured input**: user pastes a paragraph of text containing names and emails mixed together. Parse systematically, present extracted records for confirmation before finalizing CSV.
3. **Duplicate resolution conflict**: two records have same email but different names (e.g., name change or shared alias). Flag both, present side-by-side, ask user which to keep or whether to create separate records.
4. **Non-Latin characters**: contact names in Cyrillic, Arabic, or CJK scripts. Preserve original encoding in UTF-8, do not transliterate unless user requests it.
5. **GDPR deletion request**: user asks to mark contact as "do not contact". Set status to `DO_NOT_CONTACT`, clear optional fields (phone, notes), preserve minimum identification data.

## Good vs Bad Example

### Good

```
Input: "Create a contact database for my 5 key clients:
        - Maria Lopez, CTO at TechCo, maria@techco.com, +57 310 555 1234
        - James Park, CEO at InnovateLabs, james@innovate.co
        - Sofia Restrepo, PM at DataFlow, sofia.r@dataflow.io, last spoke March 10"

Output:
1. CSV file (contacts-clients-2026-03-27.csv) with:
   - 3 complete records, properly normalized
   - Missing fields marked as empty (not fabricated)
   - last_contact_date: 2026-03-10 for Sofia
   - status: ACTIVE for all (default for key clients)
   - category: CLIENT for all
2. Note: "You mentioned 5 clients but provided 3. Ready to add the remaining 2."
```

### Bad

```
Output that:
- Invents email addresses for contacts where none was provided
- Uses inconsistent date formats (03/10/2026 mixed with 2026-03-10)
- Creates a markdown table instead of proper CSV
- Omits the header row in the CSV
- Stores phone numbers with parentheses and dashes inconsistently
- Ignores the "5 key clients" count discrepancy
```

## Validation Gate

Before delivering the contact database, verify:

- [ ] CSV file is UTF-8 encoded with BOM marker for Excel compatibility.
- [ ] Header row present with all core fields in snake_case.
- [ ] All text fields properly double-quoted in CSV output.
- [ ] Dates in ISO 8601 format (`YYYY-MM-DD`) throughout.
- [ ] No fabricated data: missing fields are empty, never invented.
- [ ] Duplicate detection performed if more than 10 records provided.
- [ ] Status and category fields use defined enum values only.
- [ ] Email fields pass RFC 5322 format validation (if provided).
- [ ] Phone numbers normalized to consistent format.
- [ ] Record count matches user expectation (or discrepancy flagged).
- [ ] HTML cards (if generated) use JM Labs brand colors and are self-contained.
- [ ] No sensitive data (passwords, financial info) stored in notes fields.

## Reference Files

| File | Purpose |
|------|---------|
| `references/csv-spec.md` | CSV formatting rules, encoding, delimiter standards |
| `references/field-validation.md` | Regex patterns for email, phone, URL validation |
| `references/brand-tokens.md` | JM Labs color palette and typography for HTML cards |
| `references/data-privacy.md` | GDPR and Habeas Data compliance notes for contact storage |
