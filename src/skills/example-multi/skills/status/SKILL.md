---
name: status
description: Prints disk usage of the current working directory plus a UTC timestamp. A second skill in the same plugin to demonstrate the multi-skill layout.
allowed-tools:
  - Bash
---

# Status — Disk Usage + Timestamp

This is a second skill living alongside `notebook` inside the same plugin. It demonstrates that one plugin can ship multiple SKILL.md files via the `skills/<skill>/SKILL.md` layout.

## What to do

First print this debug line exactly — it surfaces the raw arguments this skill received (empty if none): `[skill:status] args=[$ARGUMENTS]`. Then:

1. Run `df -h .` to capture disk usage of the current working directory.
2. Run `date -u +%FT%TZ` to capture the UTC timestamp.
3. Print a block in this exact shape:

```
[Status] $(date -u +%FT%TZ)
$(df -h .)
```

4. Stop. Use only `Bash`.

That is the entire skill — small on purpose.
