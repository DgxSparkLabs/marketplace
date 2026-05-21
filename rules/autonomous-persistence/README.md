# autonomous-persistence

An always-on rule that prevents agents from pausing to ask unnecessary questions -- keep working autonomously until the task is done or you are explicitly stopped.

Inspired by the autonomous experimentation loop in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/DgxSparkLabs/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/autonomous-persistence/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/autonomous-persistence/install.sh --global

# Install for a specific tool only
/tmp/marketplace/rules/autonomous-persistence/install.sh --format windsurf
/tmp/marketplace/rules/autonomous-persistence/install.sh --format cursor
/tmp/marketplace/rules/autonomous-persistence/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat autonomous-persistence/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp autonomous-persistence/formats/windsurf.md .windsurf/rules/autonomous-persistence.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp autonomous-persistence/formats/cursor.md .cursor/rules/autonomous-persistence.md
```

## What it enforces

- Never ask "should I keep going?" or "is this a good stopping point?"
- Only pause for things the human must genuinely provide (credentials, policy decisions)
- When stuck, think harder -- re-read code, search, try combinations, try radical approaches
- Exhaust all tools and approaches before asking the human for help

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/autonomous-persistence.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/autonomous-persistence.md` | `alwaysApply: true` |
