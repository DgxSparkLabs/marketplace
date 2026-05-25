# verification-ladder

Five-layer automated testing: compile, unit, integration, perf, e2e

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/verification-ladder/rule.md" .claude/rules/verification-ladder.md   # symlink (live updates)
# or:
cp rules/verification-ladder/rule.md .claude/rules/verification-ladder.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-verification-ladder` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it does

Establishes a five-layer automated verification strategy — from compile-time warnings through end-to-end smoke tests — ensuring test infrastructure is built before feature code.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
