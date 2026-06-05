# Doc Factory

Deterministic document-generation engine recovered from `origin/claude/doc-factory-engine`.

## Scope

This PR-level recovery includes the standalone core under `scripts/doc-factory/`:

- `analyze.py`: deterministic intent and field extraction from natural language.
- `validate.py`: pre-generation schema/data/template gate.
- `generate.py`: schema/data/template to output files with provenance state.
- `verify.py`: post-generation output verification.
- `engines/*`: output engines for markdown, HTML, CSV, and optional office formats.
- `fixtures/*`: local smoke fixtures for deterministic checks.

The broader branch also included skill template/schema changes. Those are intentionally not copied here; schema-enabling individual skills should happen in separate skill-scoped PRs.

## Determinism

Set `DOC_FACTORY_TIMESTAMP` or `SOURCE_DATE_EPOCH` to make generated metadata stable.

```bash
DOC_FACTORY_TIMESTAMP=2026-06-05T00:00:00+00:00 \
  python3 scripts/doc-factory/generate.py \
  --schema scripts/doc-factory/fixtures/invoice-schema.json \
  --data scripts/doc-factory/fixtures/invoice-sample.json \
  --formats html,md,csv \
  --output /tmp/doc-factory-output
```

## Validation

Run the local smoke check:

```bash
bash scripts/doc-factory/check.sh
```

The smoke check always validates CSV generation with the standard library. When `jinja2` is installed, it also validates HTML and Markdown generation.
