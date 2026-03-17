---
description: "Three-tier documentation: rules, reference, history — no sprawl"
alwaysApply: true
---

## Document Lifecycle

Every project has exactly three documentation tiers. No more.

- **Tier 1: Rules** (`AGENTS.md`) — conventions, testing requirements, critical rules. Max 200 lines. No changelogs or history.
- **Tier 2: Reference** (`HANDOFF.md`) — current state, how to build/test, what's next. Updated in-place after every behavior-changing commit.
- **Tier 3: History** (`CHANGELOG.md`) — what changed and when. Append-only.

### Rules
- Never create a document to flag that another is stale — fix the stale one.
- Never duplicate information across tiers.
- If a document has no owner or update trigger, delete it.
- After every behavior-changing commit, `HANDOFF.md` must be accurate.
