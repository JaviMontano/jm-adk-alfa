# Brand HTML

Deterministic branded HTML generation for single-file, token-driven,
responsive, accessible web artifacts. [CONFIG]

## Triggers

- "generate branded HTML"
- "create a landing page"
- "build a brand-compliant web page"
- "produce a styled HTML report"
- "design a responsive page"
- "brand tokens"
- "CSS variables"

## Assets

- `assets/activation-policy.json`: activation and routing rules.
- `assets/brand-html-contract.json`: HTML output contract and validator checks.
- `assets/favicon-policy.json`: SVG favicon rules for browser icon links.
- `assets/favicon.svg`: deterministic fallback favicon asset.
- `assets/fallback-brand-config.json`: deterministic fallback brand tokens.
- `assets/evidence-policy.json`: evidence tag and validation report policy.

## Scripts

Run deterministic fixtures:

```bash
bash skills/brand-html/scripts/check.sh
```

The check validates accepted HTML with SVG favicons and rejects hardcoded
off-token colors, low-contrast fixtures, external/base64 dependencies,
non-SVG favicons, and unresolved placeholders. [CÓDIGO]

## Output

Return a single HTML artifact or exactly one fenced `html` block with semantic
landmarks, CSS variables, responsive CSS, a browser SVG favicon link, and no
unapproved remote dependencies.
