# task-formation

Decompose requests into goals with intent, then into actionable session-sized tasks

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/task-formation/rule.md" .claude/rules/task-formation.md   # symlink (live updates)
# or:
cp rules/task-formation/rule.md .claude/rules/task-formation.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-task-formation` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it does

Enforces decomposition-first planning — break requests into goals (with intent/why), then into actionable tasks with concrete pass conditions. Code is referenced by name not line number, and tasks are sized to fit a single session.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
