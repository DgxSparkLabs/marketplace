# readable-docs

An always-on rule that enforces human-friendly documentation practices: concise READMEs, step-by-step guides for newcomers, consistent terminology, and documentation that stays in sync with code.

Complements [document-lifecycle](../document-lifecycle/) (which covers agent-facing docs like AGENTS.md and HANDOFF.md) by focusing on project documentation that humans read — READMEs, getting-started guides, architecture overviews, and how-to docs.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-readable-docs@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-readable-docs/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

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
