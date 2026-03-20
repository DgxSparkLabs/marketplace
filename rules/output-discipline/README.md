# output-discipline

An always-on rule that enforces context hygiene -- redirect verbose command output to files and extract only what you need with targeted reads.

Inspired by the output management strategy in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/output-discipline/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/output-discipline/install.sh --global

# Install for a specific tool only
/tmp/marketplace/rules/output-discipline/install.sh --format windsurf
/tmp/marketplace/rules/output-discipline/install.sh --format cursor
/tmp/marketplace/rules/output-discipline/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat output-discipline/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp output-discipline/formats/windsurf.md .windsurf/rules/output-discipline.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp output-discipline/formats/cursor.md .cursor/rules/output-discipline.md
```

## What it enforces

- Redirect verbose commands to log files instead of flooding agent context
- Use targeted extraction (grep, tail, head) to read only what's needed
- Diagnose failures from the end of logs, not the beginning
- Clean up temporary output files after use

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/output-discipline.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/output-discipline.md` | `alwaysApply: true` |
