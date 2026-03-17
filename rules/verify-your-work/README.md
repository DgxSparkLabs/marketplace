# verify-your-work

An always-on rule that requires AI agents to test and verify everything they build before declaring a task complete. Agents must be maximally autonomous — solving problems themselves — but must pause and prompt the user when credentials, API keys, or other human-dependent setup is required.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/verify-your-work/install.sh

# Install globally (all projects)
/tmp/marketplace/verify-your-work/install.sh --global

# Install for a specific tool only
/tmp/marketplace/verify-your-work/install.sh --format windsurf
/tmp/marketplace/verify-your-work/install.sh --format cursor
/tmp/marketplace/verify-your-work/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat verify-your-work/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp verify-your-work/formats/windsurf.md .windsurf/rules/verify-your-work.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp verify-your-work/formats/cursor.md .cursor/rules/verify-your-work.md
```
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
