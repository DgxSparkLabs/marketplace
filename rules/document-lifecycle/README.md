# document-lifecycle

Three-tier documentation: rules, reference, history — no sprawl

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-document-lifecycle@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-document-lifecycle/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it does

Enforces a strict three-tier documentation structure — rules in AGENTS.md, current state in HANDOFF.md, history in CHANGELOG.md — eliminating doc sprawl, duplication, and staleness.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
