# pitfalls-discipline

An always-on rule that enforces a read/write loop for `PITFALLS.md`. Before complex work, check for known pitfalls. After fixing bugs, record them.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/pitfalls-discipline/rule.md" .claude/rules/pitfalls-discipline.md   # symlink (live updates)
# or:
cp rules/pitfalls-discipline/rule.md .claude/rules/pitfalls-discipline.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-pitfalls-discipline` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- **Read before work:** Check PITFALLS.md and git log for related issues before implementing
- **Write after bugs:** Record symptom, cause, fix, and commit reference
- **Promote patterns:** Move recurring pitfalls to global rules or add structural guardrails

## Related

- [session-resilience](../session-resilience/) — the mindset rule that drives continuous state persistence
- [task-formation](../task-formation/) — includes "search pitfalls" in the Before Starting checklist
- [pitfall-check](../../skills/pitfall-check/) — skill that automates the search step
