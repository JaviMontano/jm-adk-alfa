# Domain Knowledge - Brand HTML

## Overview

`brand-html` creates deterministic single-file HTML artifacts from explicit
brand tokens. The output should feel like a brand system applied to a web page,
not a generic template with arbitrary colors.

## Best Practices

1. Resolve brand tokens before writing layout.
2. Declare tokens in `:root`.
3. Use variables after token declaration.
4. Keep semantic landmarks visible.
5. Use responsive CSS with stable constraints.
6. Avoid remote dependencies unless the brand config explicitly allows them.
7. Include a browser SVG favicon link in `<head>`; use a URL-encoded SVG data
   URI for single-file delivery or a relative `favicon.svg` path for
   asset-package delivery.
8. Treat missing config as a fallback-token path, not a reason to invent a
   brand.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| Off-token colors | Breaks brand determinism | Declare tokens in config or fallback |
| Remote scripts | Breaks single-file safety | Inline static CSS only |
| Base64 images | Bloats output | Use text, CSS, or approved relative assets |
| Bitmap favicon | Breaks the SVG favicon contract | Use `type="image/svg+xml"` |
| Inferred dates | Makes output time-dependent | Require caller-supplied `artifact_date` |
