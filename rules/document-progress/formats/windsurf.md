---
trigger: always_on
description: "Write progress to disk so nothing is lost across sessions"
---

## Document Progress

For tasks with 3+ steps or 2+ files, write progress to disk. Context compacts and sessions end — files survive.

- **Before starting:** Plan what you'll do in the todo list.
- **After each step:** Mark the todo complete. Update `HANDOFF.md` if behavior changed. Commit.
- **Do NOT rely on conversation memory.** The todo list and `HANDOFF.md` are your memory.
- Never create append-only logs that grow unboundedly. `HANDOFF.md` is edited in-place to reflect current state. History goes in `CHANGELOG.md`.
