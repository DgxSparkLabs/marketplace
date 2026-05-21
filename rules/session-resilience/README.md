# session-resilience

An always-on rule that enforces continuous state persistence. Agents don't have memory between sessions — this rule makes them write to HANDOFF.md, PITFALLS.md, and CHANGELOG.md so the next agent can pick up where they left off.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-session-resilience@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-session-resilience/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Write state to disk continuously, not just at session end
- Update HANDOFF.md after every meaningful change
- Log pitfalls (symptom, cause, fix) to PITFALLS.md
- Use the todo list as the structural plan
- Write for the next agent, not yourself

## Related

- [document-lifecycle](../document-lifecycle/) — the three-tier doc structure this rule writes to
- [document-progress](../document-progress/) — step-by-step progress tracking
- [pitfalls-discipline](../pitfalls-discipline/) — full read/write loop for PITFALLS.md
- [project-bootstrap](../../skills/project-bootstrap/) — create the doc structure this rule depends on
