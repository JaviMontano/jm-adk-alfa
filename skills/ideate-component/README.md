# Ideate Component

`ideate-component` produces a read-only concept card for one proposed plugin component: skill, agent, command, or hook. It is used before design/build work to test whether the component has a distinct responsibility, valid relationships, acceptable tool needs, and a justified MOAT depth.

## Deterministic Inputs

- Component type or enough context to ask one clarifying question.
- Existing plugin path, plugin brief, or architecture plan.
- Optional constraints such as movement, hook event, command prefix, or sandboxed tools.

## Deterministic Output

The required output is a component concept card with:

- component type and recommended kebab-case name;
- 2-3 name candidates;
- single-sentence responsibility;
- source inventory and evidence tags;
- relationships, conflicts, missing dependencies, and resolution;
- MOAT depth with required assets;
- tools needed and rationale;
- estimated line range;
- validation notes and residual risks.

## Offline Contract

The skill includes `scripts/check.sh`, which validates deterministic JSON concept-card fixtures against the policy assets in `assets/`.

Run:

```bash
bash skills/ideate-component/scripts/check.sh
```
