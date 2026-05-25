# verify-your-work

An always-on rule that requires AI agents to test and verify everything they build before declaring a task complete. Agents must be maximally autonomous — solving problems themselves — but must pause and prompt the user when credentials, API keys, or other human-dependent setup is required.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/verify-your-work/rule.md" .claude/rules/verify-your-work.md   # symlink (live updates)
# or:
cp rules/verify-your-work/rule.md .claude/rules/verify-your-work.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-verify-your-work` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- **Test before you ship** — agents must run their code, inspect output, and confirm correctness
- **Be autonomous** — exhaust all reasonable approaches before asking the user for help
- **Pause for human-dependent setup** — when API keys, OAuth tokens, or account access is needed, stop and prompt the user with clear instructions on what to provide and how
- **No untested claims** — agents must say what they verified and what they could not, never "should work"

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/verify-your-work.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/verify-your-work.md` | `alwaysApply: true` |
