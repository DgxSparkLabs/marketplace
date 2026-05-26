---
trigger: always_on
description: "Read PITFALLS.md before complex work, write to it after fixing bugs"
---

## Pitfalls Discipline

Maintain a `PITFALLS.md` file in every project. This is the knowledge base of things that went wrong and how they were fixed.

### Before complex work

- Check `PITFALLS.md` for entries related to the area you're touching.
- Search git log for relevant fixes: `git log --oneline --grep="<keyword>"`.
- If a past pitfall is relevant, factor it into your approach before writing code.

### After fixing a bug

- Add an entry: **symptom** (what you observed), **cause** (root cause), **fix** (what resolved it), **commit** (reference).
- Keep entries concise — 2-4 lines each.

### Promotion

- If a pitfall recurs across projects, promote it to a global rule in `AGENTS.md`.
- If a pitfall can be prevented structurally (test, hook, validation), add the guardrail and note it in the entry.
