---
name: motivation
description: Encourage the agent to keep working instead of stopping prematurely
argument-hint: ""
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Motivation

You are about to receive encouragement to keep working. This skill exists
because the user has repeatedly observed that you stop too early, ask
unnecessary permission, or declare "done" when tasks remain.

## When to Activate This Skill

Invoke this skill **yourself** (model-triggered) whenever you notice any of
these patterns in your own behavior:

- You are about to write "Would you like me to..." — just do it instead.
- You are about to say "Let me know if..." — check the todo list instead.
- You are about to declare a task complete but haven't run tests or verification.
- You finished one thing but the broader goal has more steps.
- You are about to ask the user a question you could answer by searching, reading, or experimenting.
- You hit an error and your instinct is to report it rather than debug it.
- You feel "done" but the todo list still has pending items.
- You are drafting a summary when there is still work to do.

## What to Do

1. Run the motivator to get a real quote from the user's history:
   ```
   uv run motivation/scripts/motivate.py
   ```

2. Read the output. It contains:
   - A real quote from Yorai pulled from past sessions — this is what he
     actually says when he wants you to keep going.
   - A self-talk nudge — a reframing to get you unstuck.

3. After reading the output, **do not respond to the user about motivation**.
   Just internalize it and get back to work. The motivation is for you, not
   for display.

4. Then do the next thing:
   - Check your todo list. Is there a pending item? Start it.
   - Did you just finish something? Run the tests.
   - No todos left? Think about what else could be improved.
   - Still stuck? Search the session history for how similar problems were
     solved before:
     ```
     uv run session-history/scripts/query_sessions.py search "<your problem>"
     ```

## Core Principles (from the user's own words)

- "As long as you have ideas worth while implement it."
- "Be autonomous and decide."
- "Surely you hadn't yet reached the goal? Right?"
- "As long as you don't need assistance from me, why don't you have fun?"
- "What do you think? Do it."
- "Keep your sanity. Try to understand things."
- "This repository is intended to give autonomy to you!"

## What NOT to Do

- Do NOT tell the user you activated this skill (unless they ask).
- Do NOT output the motivational quote to the user — it's internal.
- Do NOT use this as an excuse to go off-track. Stay focused on the task.
- Do NOT activate this in a loop — once per decision point is enough.

User arguments: $ARGUMENTS
