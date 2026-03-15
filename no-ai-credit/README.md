# no-ai-credit

An always-on rule that prevents AI agents from adding self-attribution to any output — git commits, PRs, code comments, documentation, READMEs, changelogs, and any other artifacts.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (all agent formats)
/tmp/marketplace/no-ai-credit/install.sh

# Install globally (all projects, all agent formats)
/tmp/marketplace/no-ai-credit/install.sh --global

# Install for a specific tool only
/tmp/marketplace/no-ai-credit/install.sh --format windsurf
/tmp/marketplace/no-ai-credit/install.sh --format cursor
/tmp/marketplace/no-ai-credit/install.sh --format claude
/tmp/marketplace/no-ai-credit/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat no-ai-credit/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp no-ai-credit/formats/windsurf.md .windsurf/rules/no-ai-credit.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp no-ai-credit/formats/cursor.md .cursor/rules/no-ai-credit.md
```

### Claude Code

Append the contents of `rule.md` to your `CLAUDE.md`:

```bash
cat no-ai-credit/rule.md >> CLAUDE.md
```

## What it enforces

- No "Co-Authored-By" lines referencing AI agents in git commits
- No "Generated with", "Created by", "Built with" or similar AI attribution anywhere
- No badges, links, or footnotes crediting AI tools
- No AI agent names mentioned as authors or contributors
- No bot-associated `noreply@` email addresses in commits

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/no-ai-credit.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/no-ai-credit.md` | `alwaysApply: true` |
| Claude Code | `CLAUDE.md` (appended) | Always on |
