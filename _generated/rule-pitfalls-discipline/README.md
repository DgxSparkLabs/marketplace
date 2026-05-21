# pitfalls-discipline

An always-on rule that enforces a read/write loop for `PITFALLS.md`. Before complex work, check for known pitfalls. After fixing bugs, record them.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-pitfalls-discipline@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-pitfalls-discipline/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- **Read before work:** Check PITFALLS.md and git log for related issues before implementing
- **Write after bugs:** Record symptom, cause, fix, and commit reference
- **Promote patterns:** Move recurring pitfalls to global rules or add structural guardrails

## Related

- [session-resilience](../session-resilience/) — the mindset rule that drives continuous state persistence
- [task-formation](../task-formation/) — includes "search pitfalls" in the Before Starting checklist
- [pitfall-check](../../skills/pitfall-check/) — skill that automates the search step
