# check

Mid-session course correction — stop, review rules, and realign. A lightweight reset when work quality drifts.

## Setup

No external dependencies or API keys needed.

## Usage

```
/check
```

The skill forces a pause: re-read rules, review the todo list, run a self-diagnosis checklist, and state intent before resuming.

### What It Checks

| Question | Failure Mode |
|----------|-------------|
| Am I verifying or assuming? | Guessing instead of tracing |
| Did I estimate blast radius? | Large risky changes without planning |
| Am I tunneling? | >30 min on a failing approach |
| Did I skip verification? | "I'm sure this works" without running tests |
| Am I scope-creeping? | "While I'm here I'll also fix..." |
| Did I write down what I learned? | Context hoarding — knowledge stuck in conversation |
| Is HANDOFF.md still accurate? | Stale docs for the next agent |

### When to Use

- When the user says **"slow down"** or **"check yourself"**
- After a **long stretch** of work without reflecting
- After hitting an **unexpected error**
- When **switching tasks** mid-session
- When catching yourself saying **"I think"** instead of **"I verified"**

## As an Agent Skill

```bash
cp -r check/ ~/.config/devin/skills/check/
```

The skill is both user-triggered (`/check`) and model-triggered. The agent can invoke it autonomously when it detects drift.
