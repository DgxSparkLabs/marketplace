# pitfalls-discipline

An always-on rule that enforces a read/write loop for `PITFALLS.md`. Before complex work, check for known pitfalls. After fixing bugs, record them.

## Quick Install

```bash
git clone https://github.com/yourusername/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/pitfalls-discipline/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/pitfalls-discipline/install.sh --global

# Install for a specific tool
/tmp/marketplace/rules/pitfalls-discipline/install.sh --format windsurf
/tmp/marketplace/rules/pitfalls-discipline/install.sh --format cursor
```

## What it enforces

- **Read before work:** Check PITFALLS.md and git log for related issues before implementing
- **Write after bugs:** Record symptom, cause, fix, and commit reference
- **Promote patterns:** Move recurring pitfalls to global rules or add structural guardrails

## Related

- [session-resilience](../session-resilience/) — the mindset rule that drives continuous state persistence
- [task-formation](../task-formation/) — includes "search pitfalls" in the Before Starting checklist
- [pitfall-check](../../skills/pitfall-check/) — skill that automates the search step
