# readable-docs

An always-on rule that enforces human-friendly documentation practices: concise READMEs, step-by-step guides for newcomers, consistent terminology, and documentation that stays in sync with code.

Complements [document-lifecycle](../document-lifecycle/) (which covers agent-facing docs like AGENTS.md and HANDOFF.md) by focusing on project documentation that humans read — READMEs, getting-started guides, architecture overviews, and how-to docs.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/readable-docs/rule.md" .claude/rules/readable-docs.md   # symlink (live updates)
# or:
cp rules/readable-docs/rule.md .claude/rules/readable-docs.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-readable-docs` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- **TL;DR README** — one screen, not a manual. Links to detailed docs.
- **Guides in `docs/`** — one topic per file, named by subject.
- **Hand-holding** — step-by-step for newcomers, with prerequisites and expected output.
- **Consistent terminology** — define terms once, use them uniformly.
- **Docs track code** — update docs in the same commit as behavior changes.
- **Mirror code structure** — docs explain each module/subsystem.
- **No orphaned docs** — every document is linked from somewhere.
- **Consistency** — uniform formatting, heading style, and command syntax.

## Companion skill

Use with [code-health-audit](../../skills/code-health-audit/) to scan for documentation problems — missing docs, orphaned files, stale content.

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/readable-docs.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/readable-docs.md` | `alwaysApply: true` |
