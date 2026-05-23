# Adding a Domain Bundle

A **domain bundle** is a plugin whose only purpose is to declare dependencies on a group of other plugins. Users install one bundle, and Claude Code auto-installs every member.

Examples shipped by this marketplace: `skills-communication`, `skills-devops`, `rules-quality`, `rules-workflow`, `rules-all`.

## How they work

Domain bundles are **never edited directly**. They are generated from tagging in `catalog.toml`. To add a new bundle, you add a new `[skill_domain.<name>]` or `[rule_domain.<name>]` section to `catalog.toml`. The generator produces the corresponding `_generated/skills-<name>/` or `_generated/rules-<name>/` plugin with a `dependencies` array.

Verified empirically (see [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md)): when a user runs `/plugin install skills-<domain>@dgxsparklabs-marketplace`, Claude Code auto-installs every plugin listed in the `dependencies` array.

## Workflow — adding a new domain

1. **Decide** which existing skills or rules belong in the new domain. They must already exist in `skills/<name>/` or `rules/<name>/`. (To add a new skill or rule into an existing domain, see [`ADDING_A_SKILL.md`](./ADDING_A_SKILL.md) or [`ADDING_A_RULE.md`](./ADDING_A_RULE.md).)

2. **Remove the chosen members from their existing domain(s)** in `catalog.toml` — each skill/rule must belong to exactly one domain (the test suite enforces this).

3. **Add a new domain section**:
   ```toml
   [skill_domain.my-new-domain]
   display_name = "My New Domain"
   description = "One-line description shown in the bundle's plugin.json"
   members = ["skill-name-1", "skill-name-2", "skill-name-3"]
   ```
   Or `[rule_domain.my-new-domain]` for rules. Domain names must be kebab-case (they become part of the plugin name as `skills-my-new-domain`).

4. **Regenerate**:
   ```bash
   uv run scripts/generate_manifest.py
   ```
   This creates `_generated/skills-my-new-domain/.claude-plugin/plugin.json` with the dependency list and adds the bundle to `marketplace.json`.

5. **Validate**:
   ```bash
   uv run tests/test_marketplace.py
   ```
   The test suite confirms every member maps to an existing source directory and that no skill/rule appears in multiple domains.

6. **Commit** with a message describing the new domain.

## Workflow — moving an existing item between domains

1. Remove the item from its current domain's `members` list in `catalog.toml`.
2. Add it to the new domain's `members` list.
3. Regenerate and commit.

## Naming convention

| Source type | Domain plugin name |
|-------------|-------------------|
| `[skill_domain.foo]` | `skills-foo` |
| `[rule_domain.bar]` | `rules-bar` |

Note the plural. Singular prefixes (`skill-`, `rule-`) are reserved for individual plugins.

## Why dep-only bundles?

The alternative would be to physically copy member content into each bundle's directory. We chose dep-only bundles because:

- Single source of truth (member content lives in one place)
- Bundle updates are trivial (one-line catalog edit + regenerate)
- Installing a bundle gives users exactly the same content as installing the members individually — no version skew
- Smaller repo footprint

The tradeoff: we depend on Claude Code's `dependencies` auto-install behavior. This was verified empirically; see [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md).

## Cross-construct bundles?

The generator supports bundles for all 10 construct types. Each construct type already has a `[<construct>_domain.examples]` entry in `catalog.toml` that produces a `<construct>s-examples` bundle pointing at the reference example plugin. When a future PR adds multiple commands, agents, hooks, etc., add `[command_domain.my-domain]`, `[agent_domain.my-domain]`, etc. sections to `catalog.toml` — the generator will automatically produce `commands-my-domain`, `agents-my-domain`, etc. bundles.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md)
- [`PLAN_PLUGIN_COMPLIANCE.md`](./PLAN_PLUGIN_COMPLIANCE.md) — full architecture
