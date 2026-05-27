---
# `name` is the slash-component half of the invocation: `/skill-example:lab-notebook`.
# This is operator-authored — the generator does NOT modify it. Pick a short
# semantic word (not the plugin name) to avoid doubled forms like `/skill-example:example-skill`.
# See docs/ADDING_A_CONSTRUCT.md § "Trace each fragment to its source" for the full chain.
name: lab-notebook
description: Reference example. Echoes back a formatted lab-notebook-style status message. Shows how to write a SKILL.md with frontmatter, allowed-tools, and argument handling.
argument-hint: "[topic]"
allowed-tools:
  - Bash
  - Read
---

# Example Skill — Lab Notebook Status

This is a reference skill. When invoked, it composes a short formatted message tagged as a lab notebook entry.

If the user provided a topic via arguments, mention it. Otherwise, ask the user what topic they want to log.

User arguments: $ARGUMENTS

## What to do

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
