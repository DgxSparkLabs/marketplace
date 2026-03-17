---
description: "Concrete pass conditions, code references by name, session-sized tasks"
alwaysApply: true
---

## Task Formation

- **Define "done"** as one concrete command with one observable outcome before writing any code.
- **Reference code by name, not line number.** "After the declaration of `g_handle_map`" not "after line ~2113."
- **Every task has a pass condition** written before work starts — a specific, verifiable check.
- **Dependency graphs are explicit.** If B depends on A, draw it.
- **Tasks are sized for one session.** If it can't be completed, tested, and committed in one sitting, break it down.

### The Commit Loop
1. State what you're changing in one sentence
2. Write or update the test
3. Make the change
4. Run the test — if it fails, go back to 3
5. Run the full fast suite
6. Update `HANDOFF.md` if behavior changed
7. Commit
