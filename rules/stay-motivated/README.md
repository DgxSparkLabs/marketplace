# stay-motivated

Prevent the agent from stopping prematurely — keep working until truly done. An always-on rule that fires every session, reminding the agent to check its todo list, debug errors instead of reporting them, and keep shipping until all tasks are complete.

## Why This Exists

Agents tend to stop early: they ask "would you like me to..." instead of doing, they report errors instead of debugging, and they declare "done" with pending tasks. This rule injects a persistent nudge into every session based on patterns observed across 58 real sessions.

Pairs with the [motivation](../motivation/) skill for on-demand encouragement from the user's own words.

## Install

```bash
# Install to AGENTS.md (default, current project)
stay-motivated/install.sh

# Install globally
stay-motivated/install.sh --global

# Install for a specific tool
stay-motivated/install.sh --format windsurf
stay-motivated/install.sh --format cursor
stay-motivated/install.sh --format all
```

## What It Does

The rule is passive — no scripts, no dependencies. It adds a checklist to the agent's context that triggers before any "stopping" behavior:

1. **Self-check**: 7 questions to ask before stopping (pending todos? untested code? errors to debug?)
2. **Recovery**: Points to the `/motivation` skill for a real quote from session history
3. **Standing instructions**: 5 direct quotes from the user establishing the expected work ethic
4. **Definition of done**: Concrete checklist (todos complete, tests pass, committed, notified)

## Supported Formats

| Format | File | Activation |
|--------|------|------------|
| AGENTS.md | `rule.md` | Always active |
| Windsurf | `formats/windsurf.md` | `trigger: always_on` |
| Cursor | `formats/cursor.md` | `alwaysApply: true` |
