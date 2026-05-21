# session-resilience

An always-on rule that enforces continuous state persistence. Agents don't have memory between sessions — this rule makes them write to HANDOFF.md, PITFALLS.md, and CHANGELOG.md so the next agent can pick up where they left off.

## Quick Install

```bash
git clone https://github.com/yourusername/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/session-resilience/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/session-resilience/install.sh --global

# Install for a specific tool
/tmp/marketplace/rules/session-resilience/install.sh --format windsurf
/tmp/marketplace/rules/session-resilience/install.sh --format cursor
```

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
