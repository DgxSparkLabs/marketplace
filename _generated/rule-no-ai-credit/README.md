# no-ai-credit

An always-on rule that prevents AI agents from adding self-attribution to any output — git commits, PRs, code comments, documentation, READMEs, changelogs, and any other artifacts.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/no-ai-credit/rule.md" .claude/rules/no-ai-credit.md   # symlink (live updates)
# or:
cp rules/no-ai-credit/rule.md .claude/rules/no-ai-credit.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-no-ai-credit` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


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
