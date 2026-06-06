# Example Input

Design a plugin subagent named `plugin-qa-engineer`.

Context:

- The plugin has three skills: `validate-structure`, `validate-manifest`, and `generate-qa-report`. [CONFIG]
- The agent handles `/pqa:validate` and `/pqa:report`. [CONFIG]
- The agent should be read-only except for writing the final report draft. [CONFIG]
- Do not include `hooks`, `mcpServers`, or `permissionMode` in frontmatter. [CONFIG]
- Document maxTurns with the standard formula. [CONFIG]
