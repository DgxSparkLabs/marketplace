---
name: check
description: Mid-session course correction — stop, review rules, and realign
allowed-tools:
  - read
  - grep
  - glob
triggers:
  - user
  - model
---

# Course Correction

STOP. Before doing anything else, course-correct.

## Step 1: Re-read your rules

Find and read your global rules files:
- `~/.config/devin/AGENTS.md` (Devin CLI)
- `~/.config/devin/CRAFT.md` (thinking framework, if exists)
- `~/.claude/CLAUDE.md` (Claude Code)
- `AGENTS.md` in the project root

Read them fully. Don't skim.

## Step 2: Review your todo list

What's in progress? What's pending? What did you skip?

## Step 3: Self-diagnosis

Ask yourself these questions honestly:

- **Am I verifying or assuming?** Documentation says X? Run the command. Read the actual code. "I assumed..." is how every debugging hour starts.
- **Did I estimate blast radius** before my last change? How many files? Can I revert cleanly?
- **Am I tunneling?** Have I been on the same failing approach for >30 minutes? If so, stop and reassess. Check PITFALLS.md.
- **Did I skip verification?** "I'm sure this works" is not verification. Run the tests. Every time.
- **Am I scope-creeping?** "While I'm here I'll also fix..." — no. One change, one commit. Note other things for later.
- **Did I write down what I learned?** If I figured something out, is it in HANDOFF.md, PITFALLS.md, or a commit message? Or just in conversation?
- **Is HANDOFF.md still accurate?** Would the next agent thank me for how I left this project?

## Step 4: State your intent

Say out loud:
- What you're working on and **why**
- What **"done" looks like** for this task (one concrete, verifiable check)
- What your **next concrete step** is

Then resume work.

## When to Use

- When the user says "slow down", "check yourself", or similar
- When you've been working for a while without pausing to reflect
- After hitting an error you didn't expect
- When switching tasks mid-session
- When you catch yourself saying "I think" instead of "I verified"

User arguments: $ARGUMENTS
