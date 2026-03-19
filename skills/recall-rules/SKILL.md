---
name: recall-rules
description: Re-read global rules and thinking framework to realign mid-session
allowed-tools:
  - read
  - grep
  - glob
triggers:
  - user
  - model
---

# Recall Rules

Re-read and internalize the global agent rules and thinking framework. These are your operating instructions — follow them for the rest of this session.

## What to Do

1. **Find your global rules files.** Check these locations in order:

   - `~/.config/devin/AGENTS.md` (Devin CLI global rules)
   - `~/.config/devin/CRAFT.md` (thinking framework, if it exists)
   - `~/.claude/CLAUDE.md` (Claude Code global rules)
   - `.cursorrules` or `.cursor/rules/` (Cursor project rules)
   - `.windsurf/rules/` (Windsurf project rules)

2. **Read every rules file you find.** Use the `read` tool on each one. Read them fully — don't skim.

3. **Check the current project** for local rules:
   - `AGENTS.md` in the project root
   - `CLAUDE.md` in the project root
   - `.cursor/rules/*.md`
   - `.windsurf/rules/*.md`

4. **Internalize the rules.** After reading, state:
   - The 3 most important rules for the current task
   - Any rules you may have been violating

5. **Resume work** with the rules fresh in context.

## When to Use

- At the **start of a session** to load your operating instructions
- When you feel yourself **drifting** from disciplined work
- When the user says something like "slow down" or "check yourself"
- After a **long stretch** of work without reviewing your process
- When switching between **different projects** in the same session

User arguments: $ARGUMENTS
