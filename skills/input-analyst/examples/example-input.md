# Example Input

Analyze this raw input offline and produce a stable Markdown report:

```json
{
  "schema_version": "input-analysis.v1",
  "raw_input": "i need somthing for teh meeting tmrw about that thing we talked about",
  "context": {
    "audience": "general assistant",
    "constraints": [
      "Preserve intent while correcting surface errors.",
      "Do not call external APIs."
    ]
  },
  "requested_passes": [
    "surface",
    "five_whys",
    "seven_so_whats",
    "intent",
    "reformulation"
  ],
  "routing_policy": {
    "offline_only": true,
    "allow_external_apis": false
  }
}
```

Command:

```bash
python3 skills/input-analyst/scripts/compile-input-analysis.py \
  --input skills/input-analyst/scripts/fixtures/input-analysis-input.json
```
