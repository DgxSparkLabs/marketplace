# revert-on-failure

An always-on rule that enforces a commit-experiment-measure-revert loop for speculative changes -- commit a known-good baseline, try one thing, measure, keep if improved, revert if not.

Inspired by the experiment loop in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/revert-on-failure/rule.md" .claude/rules/revert-on-failure.md   # symlink (live updates)
# or:
cp rules/revert-on-failure/rule.md .claude/rules/revert-on-failure.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-revert-on-failure` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- Always commit a clean baseline before making speculative changes
- Test each change individually -- no batching untested experiments
- Keep changes that measurably improve, revert everything else
- Use judgment on crashes: fix trivial issues, abandon broken ideas
- Abandon an approach after 3 failed attempts -- try a different angle

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/revert-on-failure.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/revert-on-failure.md` | `alwaysApply: true` |
