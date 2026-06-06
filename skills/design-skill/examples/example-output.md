# Example Output

```json
{
  "skill": "design-skill",
  "reference_date": "2026-06-06",
  "designed_skill": "validate-config",
  "summary": "The design is valid because the skill name is kebab-case, the procedure has six structured steps, and the read-only tool profile excludes Write. [CONFIG]",
  "frontmatter": {
    "name": "validate-config",
    "description": "Validates plugin configuration files for syntax, required keys, and consistency. Trigger: validate config, check config, config audit.",
    "argument-hint": "<plugin-path>",
    "allowed-tools": ["Read", "Glob", "Grep"]
  },
  "guiding_principle": "Configuration is code that fails quietly until validation makes it visible. [DOC]",
  "procedure": [
    {"step": 1, "action": "Scan", "input": "plugin path", "output": "config file inventory", "evidence_tag": "[CODE]"},
    {"step": 2, "action": "Read", "input": "config file inventory", "output": "raw config contents", "evidence_tag": "[CODE]"},
    {"step": 3, "action": "Validate", "input": "raw config contents", "output": "syntax findings", "evidence_tag": "[CODE]"},
    {"step": 4, "action": "Compare", "input": "syntax findings", "output": "required-key findings", "evidence_tag": "[CONFIG]"},
    {"step": 5, "action": "Report", "input": "all findings", "output": "config validation report", "evidence_tag": "[DOC]"},
    {"step": 6, "action": "Summarize", "input": "config validation report", "output": "pass/fail decision", "evidence_tag": "[DOC]"}
  ],
  "quality_criteria": [
    "Every config file discovered by Glob is represented in the report. [CODE]",
    "Malformed config files are marked FAIL with the file path. [CODE]",
    "Missing required keys are listed with the expected key name. [CONFIG]",
    "The report includes a single pass/fail decision. [DOC]",
    "No file modification commands are included. [CONFIG]"
  ],
  "anti_patterns": [
    "Treating parser warnings as successful validation.",
    "Including Write in a read-only validation skill.",
    "Skipping empty config files without reporting them.",
    "Mixing remediation edits into the validation report."
  ],
  "edge_cases": [
    {"case": "No config files exist", "expected": "Return INFO with zero files validated. [CONFIG]"},
    {"case": "Config file is empty", "expected": "Report FAIL with exact path. [CODE]"},
    {"case": "Mixed JSON and YAML configs", "expected": "Validate each format separately. [CONFIG]"}
  ],
  "tool_rationale": [
    {"tool": "Read", "reason": "Read config file contents. [CONFIG]"},
    {"tool": "Glob", "reason": "Locate config files. [CONFIG]"},
    {"tool": "Grep", "reason": "Find key references without writing files. [CONFIG]"}
  ],
  "moat_score": {"completeness": 22, "accuracy": 22, "actionability": 22, "maintainability": 22, "total": 88},
  "validation": ["The design meets frontmatter, body, tool, and MOAT thresholds. [CONFIG]"],
  "risks": ["The exact required keys must come from the target plugin contract before implementation. [ASSUMPTION]"]
}
```
