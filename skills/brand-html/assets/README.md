# Brand HTML Assets

These assets make `brand-html` deterministic. They define activation routing,
the HTML artifact contract, SVG favicon policy, fallback brand tokens, evidence
requirements, and the fixture manifest used by `scripts/check.sh`.

`favicon.svg` is the fallback browser icon. It is square, self-contained, and
has no remote fonts or assets. Generated single-file HTML should reference a
URL-encoded SVG favicon data URI; asset-package outputs may reference a local
`favicon.svg` path.

Run `bash skills/brand-html/scripts/check.sh` after changing assets, fixtures,
templates, or validator logic.
