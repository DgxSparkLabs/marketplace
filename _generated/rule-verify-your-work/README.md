# verify-your-work

An always-on rule that requires AI agents to test and verify everything they build before declaring a task complete. Agents must be maximally autonomous — solving problems themselves — but must pause and prompt the user when credentials, API keys, or other human-dependent setup is required.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-verify-your-work@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-verify-your-work/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

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
