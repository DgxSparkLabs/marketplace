---
status: live
purpose: knowledge-base-of-bugs-and-fixes
---

# Pitfalls

Knowledge base of bugs that occurred in this project and how they were fixed. Per `AGENTS.md`, after fixing any bug worth remembering, add an entry here so the next agent can avoid the same trap.

Pre-1.0 entries (Textual TUI installer era — installer crashes, banner glyphs, secret-leak skill setup, dangling-symlink bootstrap) are preserved at [`docs/archive/pre-1.0-pitfalls.md`](docs/archive/pre-1.0-pitfalls.md). They reference code paths that no longer exist after the v1.0.0 plugin-compliance migration and Phase 4 DI refactor.

## Format

Each entry uses this template:

```markdown
## <Short symptom title>

- **Symptom:** What you observed (the visible failure mode).
- **Cause:** Root cause — the actual reason it broke.
- **Fix:** What resolved it.
- **Commit:** `<short-sha>` (optional but preferred).
```

Keep entries 2-4 lines per field. Link to the commit so the next agent can read the diff. If a pitfall is structural (would have been caught by a test or hook), add the guardrail too and note it in the entry.

## Entries

_No active post-1.0 entries yet. Add the first one here when the next bug is fixed._
