# simplicity-bar

An always-on rule that enforces a complexity cost/benefit check on every change -- weigh the improvement magnitude against the complexity added, and prefer deletion over addition.

Inspired by the simplicity criterion in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/simplicity-bar/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/simplicity-bar/install.sh --global

# Install for a specific tool only
/tmp/marketplace/rules/simplicity-bar/install.sh --format windsurf
/tmp/marketplace/rules/simplicity-bar/install.sh --format cursor
/tmp/marketplace/rules/simplicity-bar/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat simplicity-bar/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp simplicity-bar/formats/windsurf.md .windsurf/rules/simplicity-bar.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp simplicity-bar/formats/cursor.md .cursor/rules/simplicity-bar.md
```

## What it enforces

- Weigh complexity cost against improvement magnitude before keeping any change
- Prefer code deletion over code addition when results are preserved
- Reject marginal improvements that add disproportionate complexity
- Treat every added line as a maintenance liability that must earn its place

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/simplicity-bar.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/simplicity-bar.md` | `alwaysApply: true` |
