# simplicity-bar

An always-on rule that enforces a complexity cost/benefit check on every change -- weigh the improvement magnitude against the complexity added, and prefer deletion over addition.

Inspired by the simplicity criterion in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/simplicity-bar/rule.md" .claude/rules/simplicity-bar.md   # symlink (live updates)
# or:
cp rules/simplicity-bar/rule.md .claude/rules/simplicity-bar.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-simplicity-bar` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- Weigh complexity cost against improvement magnitude before keeping any change
- Prefer code deletion over code addition when results are preserved
- Reject marginal improvements that add disproportionate complexity
- Treat every added line as a maintenance liability that must earn its place

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/simplicity-bar.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/simplicity-bar.md` | `alwaysApply: true` |
