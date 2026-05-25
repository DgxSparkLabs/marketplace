# no-ai-credit

An always-on rule that prevents AI agents from adding self-attribution to any output — git commits, PRs, code comments, documentation, READMEs, changelogs, and any other artifacts.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-no-ai-credit@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-no-ai-credit/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

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
