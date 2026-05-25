# session-resilience

An always-on rule that enforces continuous state persistence. Agents don't have memory between sessions — this rule makes them write to HANDOFF.md, PITFALLS.md, and CHANGELOG.md so the next agent can pick up where they left off.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/session-resilience/rule.md" .claude/rules/session-resilience.md   # symlink (live updates)
# or:
cp rules/session-resilience/rule.md .claude/rules/session-resilience.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-session-resilience` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


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
