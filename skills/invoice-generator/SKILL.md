---
name: invoice-generator
description: >
  Triggers on "create invoice", "invoice template", "factura", "generar factura".
  Branded invoice template builder with client info, line items, subtotal/tax/total,
  payment terms, and bank details placeholder. JM Labs dark brand HTML, bilingual
  ES/EN, print-optimized. Output: self-contained HTML invoice. [EXPLICIT]
argument-hint: "client name, line items (description + qty + unit price), currency, payment terms"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# invoice-generator

## TL;DR

Generates professional, print-ready invoices as self-contained HTML files using the JM Labs dark brand identity. Accepts client details, line items, tax configuration, and payment terms. Produces bilingual (ES/EN) output with automatic subtotal/tax/total calculation, structured bank details placeholder, and CSS print stylesheet for pixel-perfect PDF export.

## When to Activate

- User requests an invoice, factura, or billing document for a client engagement.
- User asks for a reusable invoice template with JM Labs branding.
- User provides line items, amounts, or service descriptions expecting a formatted financial document.
- User mentions "create invoice", "invoice template", "factura", or "generar factura".
- Do NOT activate for general pricing discussions, cost estimations, or budget planning (use `cost-estimation` or `pricing-strategy` instead).

## Invoice Structure & Layout

### Header Block

The invoice header contains:

- **JM Labs logo placeholder** (`[LOGO]` div with brand colors, replaceable with base64 image).
- **Invoice number**: auto-generated format `JML-YYYY-NNN` based on current date.
- **Issue date** and **due date** (calculated from payment terms).
- **Issuer block**: JM Labs legal name, NIT/tax ID placeholder, address, contact email.
- **Client block**: company name, contact person, tax ID, billing address, purchase order reference (optional).

### Line Items Table

Each row contains:

| Column | Type | Notes |
|--------|------|-------|
| # | Auto-increment | Row number |
| Description | Text | Service or product description, bilingual if requested |
| Quantity | Number | Decimal-safe (e.g., 1.5 hours) |
| Unit Price | Currency | Formatted with thousands separator |
| Subtotal | Calculated | qty x unit_price, auto-computed |

### Totals Block

- **Subtotal**: sum of all line item subtotals.
- **Tax line(s)**: configurable tax name and rate (default: IVA 19% for Colombia).
- **Discount line**: optional, percentage or flat amount.
- **Total**: final amount in bold, large font.
- **Currency indicator**: ISO 4217 code (COP, USD, EUR) displayed next to amounts.

### Payment Terms Section

- Payment deadline (Net 15, Net 30, Net 60, or custom).
- Accepted payment methods.
- Bank details placeholder with fields for: bank name, account type, account number, SWIFT/BIC, beneficiary name.
- Late payment policy note (optional).

### Footer

- Legal disclaimer text (bilingual).
- Document generation timestamp.
- Page number for multi-page print.

## Brand & Visual Design

The invoice follows the JM Labs dark brand system:

- **Background**: `#0a0a0a` (near-black) with `#1a1a2e` card surfaces.
- **Primary accent**: `#e94560` (coral red) for headings, totals, and highlights.
- **Text**: `#eaeaea` (light gray) for body, `#ffffff` for totals.
- **Font stack**: `'Inter', 'Segoe UI', system-ui, sans-serif`.
- **Table styling**: alternating row backgrounds (`#1a1a2e` / `#16213e`), no outer borders, subtle bottom borders on rows.
- **Print override**: `@media print` stylesheet flips to white background, dark text, hides non-essential elements, forces `break-inside: avoid` on tables.

## Bilingual Support (ES/EN)

Every text element includes both languages:

- Labels are rendered as `Factura / Invoice`, `Subtotal / Subtotal`, `Total / Total`.
- The `lang` parameter controls primary language (displayed prominently) vs secondary (displayed in smaller text or parentheses).
- Date format adapts: `DD/MM/YYYY` for ES, `MM/DD/YYYY` for EN.
- Currency formatting adapts: `$1.500.000` for COP, `$1,500.00` for USD.

## Trade-off Matrix

| Decision | Option A | Option B | Default |
|----------|----------|----------|---------|
| Output format | Single HTML file | HTML + separate CSS | Single HTML (portable) |
| Tax calculation | Auto-compute in HTML | Static values only | Auto-compute (JS-free CSS calc display) |
| Logo embedding | Base64 inline | External URL reference | Base64 placeholder |
| Multi-page support | CSS page-break rules | Single continuous page | CSS page-break |
| Currency | Single currency | Multi-currency per line | Single currency |
| Number formatting | Locale-aware JS | Pre-formatted strings | Pre-formatted strings (no JS dependency) |

## Assumptions & Limits

- **Assumption**: invoices are for professional services, not physical goods with shipping. [INFERRED]
- **Assumption**: Colombian tax regime (IVA 19%) is the default; user can override. [EXPLICIT]
- **Assumption**: bank details are placeholders; user fills in sensitive data manually. [EXPLICIT]
- **Limit**: no PDF generation natively; user prints to PDF from browser.
- **Limit**: no recurring invoice scheduling; this produces one-off documents.
- **Limit**: no integration with accounting software; output is standalone HTML.
- **Limit**: line items capped at 50 rows for print layout stability.

## Edge Cases

1. **Zero-amount invoice**: proforma or courtesy invoices with $0 total. Render normally with "PROFORMA" watermark and skip payment terms section.
2. **Multi-tax jurisdiction**: client requests both IVA and withholding tax (retefuente). Add multiple tax lines with separate rates and labels.
3. **Extremely long descriptions**: line item descriptions exceeding 200 characters. Truncate at 200 chars in table, add full description as footnote.
4. **Currency mismatch**: user provides amounts in USD but requests COP invoice. Flag the mismatch, ask for exchange rate or confirmation, never silently convert.
5. **Missing client info**: user provides incomplete client data. Generate invoice with `[PENDING]` placeholders for missing fields, add warning banner.

## Good vs Bad Example

### Good

```
Input: "Create an invoice for Acme Corp, 3 items: Discovery phase 40hrs at $150/hr,
        Architecture design 20hrs at $200/hr, Documentation 10hrs at $100/hr.
        Net 30, USD."

Output: Complete HTML invoice with:
- Invoice number JML-2026-001
- All 3 line items with calculated subtotals ($6000, $4000, $1000)
- Subtotal: $11,000.00
- Tax: configurable (0% for international, or IVA if Colombian)
- Total: $11,000.00
- Due date: 30 days from issue date
- Bank details placeholder section
- Print-ready CSS
```

### Bad

```
Output that:
- Uses generic white template with no JM Labs branding
- Hardcodes tax rate without asking jurisdiction
- Embeds real bank account numbers in the template
- Requires external CSS file or CDN links (not self-contained)
- Outputs a markdown table instead of proper HTML
- Omits payment terms or due date calculation
```

## Validation Gate

Before delivering the invoice, verify:

- [ ] Output is a single self-contained HTML file (no external dependencies).
- [ ] JM Labs dark brand colors applied: `#0a0a0a`, `#e94560`, `#1a1a2e`.
- [ ] All line item subtotals are mathematically correct (qty x unit_price).
- [ ] Grand total equals subtotal + tax - discount (verified manually).
- [ ] `@media print` stylesheet included with light-background override.
- [ ] Bilingual labels present for all section headers and field names.
- [ ] Bank details section contains ONLY placeholders, never real account data.
- [ ] Invoice number follows `JML-YYYY-NNN` format.
- [ ] Due date correctly calculated from issue date + payment terms.
- [ ] Currency symbol and formatting consistent throughout document.
- [ ] No JavaScript dependencies; all calculations pre-rendered in HTML.
- [ ] File size under 50KB for email attachment compatibility.

## Reference Files

| File | Purpose |
|------|---------|
| `references/brand-tokens.md` | JM Labs color palette, typography, spacing system |
| `references/tax-config.md` | Tax rates by jurisdiction (CO, US, EU defaults) |
| `references/invoice-templates.md` | HTML skeleton and CSS patterns for invoice layout |
| `references/payment-terms.md` | Standard payment term definitions and legal text |
