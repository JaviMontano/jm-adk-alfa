# Preservation Report JSON Template

```json
{
  "schema": 1,
  "skill": "local-state-preservation",
  "mode": "inventory-only",
  "scope": {
    "repository": "",
    "branch": "",
    "head": "",
    "upstream": ""
  },
  "mutation_policy": {
    "default_mutates_files": false,
    "requires_explicit_apply": true,
    "allowed_write_roots": [],
    "private_path_patterns": ["user-context/jarvis-os"]
  },
  "surfaces": {
    "tracked_changes": [],
    "untracked_files": [],
    "ignored_files": [],
    "stashes": [],
    "worktrees": [],
    "clones": [],
    "private_path_exclusions": [
      {
        "path": "user-context/jarvis-os",
        "handling": "excluded",
        "reason": ""
      }
    ]
  },
  "artifacts": [],
  "non_touch_decisions": [
    {
      "surface": "stashes",
      "decision": "inventory-only",
      "reason": ""
    },
    {
      "surface": "private_paths",
      "decision": "do-not-move-or-publish",
      "reason": ""
    }
  ],
  "validation": {
    "status": "pass",
    "commands": []
  },
  "next_action": "pause"
}
```
