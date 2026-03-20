# revert-on-failure

An always-on rule that enforces a commit-experiment-measure-revert loop for speculative changes -- commit a known-good baseline, try one thing, measure, keep if improved, revert if not.

Inspired by the experiment loop in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/revert-on-failure/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/revert-on-failure/install.sh --global

# Install for a specific tool only
/tmp/marketplace/rules/revert-on-failure/install.sh --format windsurf
/tmp/marketplace/rules/revert-on-failure/install.sh --format cursor
/tmp/marketplace/rules/revert-on-failure/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat revert-on-failure/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp revert-on-failure/formats/windsurf.md .windsurf/rules/revert-on-failure.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp revert-on-failure/formats/cursor.md .cursor/rules/revert-on-failure.md
```

## What it enforces

- Always commit a clean baseline before making speculative changes
- Test each change individually -- no batching untested experiments
- Keep changes that measurably improve, revert everything else
- Use judgment on crashes: fix trivial issues, abandon broken ideas
- Abandon an approach after 3 failed attempts -- try a different angle

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/revert-on-failure.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/revert-on-failure.md` | `alwaysApply: true` |
