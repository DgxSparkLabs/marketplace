# prior-art

An always-on rule that prevents AI agents from reinventing the wheel. Before building anything non-trivial, the agent must search for existing solutions — in the codebase, in project dependencies, and on the web — and report what it found.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-prior-art@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-prior-art/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

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
