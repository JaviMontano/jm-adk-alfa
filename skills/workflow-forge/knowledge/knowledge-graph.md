# Workflow Forge - Knowledge Graph

## Core Concepts

- workflow-forge: creates slash-command workflow definitions
- workflow-spec: structured input consumed by the offline compiler
- command-frontmatter: description, command, skills, and agents
- phase-map: ordered workflow phases with agents, inputs, outputs, checkpoints
- verification-phase: final phase that proves the workflow deliverable is ready
- workflow-policy: local rules for phases, quality gates, and prohibited stack
- deterministic-compiler: local script that validates and renders workflow specs

## Relationships

- workflow-forge requires workflow-spec
- workflow-spec produces command-frontmatter
- workflow-spec produces phase-map
- phase-map requires checkpoints
- phase-map ends with verification-phase
- workflow-policy validates workflow-spec
- deterministic-compiler applies workflow-policy
