# task-formation

Decompose requests into goals with intent, then into actionable session-sized tasks

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-task-formation@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-task-formation/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it does

Enforces decomposition-first planning — break requests into goals (with intent/why), then into actionable tasks with concrete pass conditions. Code is referenced by name not line number, and tasks are sized to fit a single session.

## See also

- [blast-radius](../blast-radius/) — estimate change scope before coding
- [verify-your-work](../verify-your-work/) — prove correctness, don't assume it
