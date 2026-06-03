---
name: notebook
description: Echoes back a formatted lab-notebook-style status message. Shows how to write a SKILL.md with frontmatter, allowed-tools, and argument handling.
argument-hint: "[topic]"
allowed-tools:
  - Bash
  - Read
---

# Notebook — Lab Notebook Status

When invoked, compose a short markdown block tagged as a lab-notebook entry.

If the user provided a topic via arguments, mention it. Otherwise, ask the user what topic they want to log.

User arguments: $ARGUMENTS

## What to do

First print this debug line exactly — it surfaces the raw arguments this skill received (empty if none): `[skill:notebook] args=[$ARGUMENTS]`. Then:

1. Compose a markdown block in this exact shape, substituting `$ARGUMENTS` for the topic:

```
[Lab Notebook] Status update on "$ARGUMENTS"
- Time: <current ISO timestamp via `date -u +%FT%TZ`>
- Status: in-progress
- Next checkpoint: <suggest one>
```

2. Print it to the user.
3. Stop. Do not invoke other tools beyond `Bash` for the timestamp.

That is the entire skill — small on purpose, so it is easy to read end to end.
