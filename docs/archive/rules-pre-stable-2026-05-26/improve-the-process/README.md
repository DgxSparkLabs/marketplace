# improve-the-process

Every session should leave the workflow better than it found it. Fix friction structurally, not just symptomatically.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/improve-the-process/rule.md" .claude/rules/improve-the-process.md   # symlink (live updates)
# or:
cp rules/improve-the-process/rule.md .claude/rules/improve-the-process.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-improve-the-process` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it does

Reminds agents that the task is never just the task. When you hit friction, make a mistake, or discover something useful, the expected response is to fix the process -- add a check, update a doc, improve a tool -- not just work around it and move on.

## See also

- [verification-ladder](../verification-ladder/) — five-layer automated testing
- [document-lifecycle](../document-lifecycle/) — three-tier documentation, no sprawl
- [stay-motivated](../stay-motivated/) — completeness checklist before stopping
