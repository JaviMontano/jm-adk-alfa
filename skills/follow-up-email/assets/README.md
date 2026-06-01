# Follow Up Email Assets

These assets support deterministic follow-up email generation without re-creating tone, subject, and rendering rules from memory.

## Files

- `email-style.css`: lightweight HTML email styling for preview/rendered output.
- `email-copy-tokens.json`: subject prefixes, default sign-off, and tone constraints.
- `manifest.json`: machine-readable asset inventory and usage map.

## Contract

- Keep assets free of real attendee data and secrets.
- Treat drafts as review-first outputs; never encode auto-send behavior in assets.
- Update `manifest.json` whenever an asset changes purpose or usage.
