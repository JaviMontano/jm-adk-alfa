# Notebook Curator Seleccion

`notebook-curator-seleccion` validates and curates the offline source inventory for a `SEL-EMPRESA` selection-process notebook.

## Triggers

- `notebook-curator`
- `sel-empresa`
- `curar-notebook`

## Deterministic Contract

- Require canonical `SEL-EMPRESA` slots.
- Require evidence details for each present source.
- Block duplicate canonical slots, missing required slots, URL-only live fetch dependencies, and unsupported curation actions.
- Do not call NotebookLM, browse, sync, or infer source content from titles.

## Local Validation

```bash
bash skills/notebook-curator-seleccion/scripts/check.sh
python3 skills/notebook-curator-seleccion/scripts/validate_archetype.py --input skills/notebook-curator-seleccion/scripts/fixtures/valid-complete-notebook.json
```

## Assets

- `assets/source-slot-contract.json`
- `assets/evidence-policy.json`
- `assets/curation-policy.json`
- `assets/offline-boundary-policy.json`
- `assets/output-contract.json`
