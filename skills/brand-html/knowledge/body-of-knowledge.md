# Brand HTML - Body of Knowledge

## Canon

Brand HTML is deterministic when every visible style decision traces to a brand
token, fallback token, or explicit user instruction. A valid artifact is
single-file HTML with inline CSS, semantic landmarks, responsive CSS, and no
unapproved remote dependencies. Browser favicons are SVG-only and must be
declared in the document head.

## Required Invariants

- CSS variables define brand colors and fonts.
- Color use after `:root` references variables.
- HTML has semantic landmarks and a viewport meta tag.
- HTML includes `<link rel="icon" type="image/svg+xml" href="...">`.
- Responsive CSS includes at least one media query.
- Unresolved template placeholders are not allowed.
- Base64 images and external JavaScript are not allowed.
- Bitmap, remote, or base64 favicons are not allowed.
- Current date/time is not inferred.

## False Positives

- DOCX, XLSX, PDF, slide, or image requests should route away.
- Token extraction without an HTML artifact should route away.
- Missing brand config is not a failure when fallback tokens are allowed.

## Validation

Use `scripts/validate_brand_html.py` and fixture HTML to verify contract
behavior before marking DoD complete.
