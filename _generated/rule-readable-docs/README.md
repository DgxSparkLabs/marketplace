# readable-docs

An always-on rule that enforces human-friendly documentation practices: concise READMEs, step-by-step guides for newcomers, consistent terminology, and documentation that stays in sync with code.

Complements [document-lifecycle](../document-lifecycle/) (which covers agent-facing docs like AGENTS.md and HANDOFF.md) by focusing on project documentation that humans read — READMEs, getting-started guides, architecture overviews, and how-to docs.

## Quick Install

```bash
git clone https://github.com/DgxSparkLabs/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/readable-docs/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/readable-docs/install.sh --global

# Install for a specific tool only
/tmp/marketplace/rules/readable-docs/install.sh --format windsurf
/tmp/marketplace/rules/readable-docs/install.sh --format cursor
/tmp/marketplace/rules/readable-docs/install.sh --format agents
```

## Manual Install

### AGENTS.md (universal)

```bash
cat rules/readable-docs/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp rules/readable-docs/formats/windsurf.md .windsurf/rules/readable-docs.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp rules/readable-docs/formats/cursor.md .cursor/rules/readable-docs.md
```

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
