# verification-ladder

Five-layer automated testing: compile, unit, integration, perf, e2e

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-verification-ladder@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-verification-ladder/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it does

Establishes a five-layer automated verification strategy — from compile-time warnings through end-to-end smoke tests — ensuring test infrastructure is built before feature code.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
