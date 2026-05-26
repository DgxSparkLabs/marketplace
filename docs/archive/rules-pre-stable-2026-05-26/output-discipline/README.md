# output-discipline

An always-on rule that enforces context hygiene -- redirect verbose command output to files and extract only what you need with targeted reads.

Inspired by the output management strategy in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/output-discipline/rule.md" .claude/rules/output-discipline.md   # symlink (live updates)
# or:
cp rules/output-discipline/rule.md .claude/rules/output-discipline.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-output-discipline` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- Redirect verbose commands to log files instead of flooding agent context
- Use targeted extraction (grep, tail, head) to read only what's needed
- Diagnose failures from the end of logs, not the beginning
- Clean up temporary output files after use

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/output-discipline.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/output-discipline.md` | `alwaysApply: true` |
