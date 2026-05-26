# document-lifecycle

Three-tier documentation: rules, reference, history — no sprawl

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/document-lifecycle/rule.md" .claude/rules/document-lifecycle.md   # symlink (live updates)
# or:
cp rules/document-lifecycle/rule.md .claude/rules/document-lifecycle.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-document-lifecycle` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it does

Enforces a strict three-tier documentation structure — rules in AGENTS.md, current state in HANDOFF.md, history in CHANGELOG.md — eliminating doc sprawl, duplication, and staleness.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
