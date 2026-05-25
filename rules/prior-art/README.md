# prior-art

An always-on rule that prevents AI agents from reinventing the wheel. Before building anything non-trivial, the agent must search for existing solutions — in the codebase, in project dependencies, and on the web — and report what it found.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/prior-art/rule.md" .claude/rules/prior-art.md   # symlink (live updates)
# or:
cp rules/prior-art/rule.md .claude/rules/prior-art.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-prior-art` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- **Search before building** — check the codebase, project dependencies, and the web for existing solutions before writing custom code
- **Evaluate what you find** — assess maintenance status, adoption, scope fit, license, quality, and security
- **Use a decision framework** — reuse exact matches, prefer well-maintained libraries, extend partial solutions, or build custom only when nothing suitable exists
- **Report findings** — always tell the user what you searched for and what you found, even if you end up building custom code
- **Know when to skip** — don't waste time searching for project-specific tasks like renaming variables or fixing typos

## How it works

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/prior-art.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/prior-art.md` | `alwaysApply: true` |
