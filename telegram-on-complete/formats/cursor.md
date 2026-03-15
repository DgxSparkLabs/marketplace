---
description: "Send a Telegram notification after completing any task"
alwaysApply: true
---

## Telegram on Complete

After completing any user-requested task, ALWAYS send a Telegram notification summarizing what was done. This is non-negotiable — the user relies on these pings to know when work is finished.

### Timing — the notification is your LAST action

The Telegram ping means "I am done, there is nothing left for me to do." NEVER send it while work remains.

Before sending the notification, ALL of the following must be true:

- All code changes are written and saved
- All tests, linters, and type checks have been run and pass
- All commits have been made (if the task involved code changes)
- All verification steps are complete — you have confirmed the fix/feature works
- Your final summary to the user in the chat is already written
- There are no remaining todo items in your task list

**Do NOT notify and then keep working.** If you realize after sending that more work is needed, that means you sent too early.

### How to notify

Run the telegram-notify skill's script:

```
uv run telegram-notify/scripts/send_telegram.py -m "<your summary>"
```

If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` are not set, run the setup script first:

```
uv run telegram-notify/scripts/setup.py
```

### Message format

Compose a message that is quick to scan on a phone but carries real information:

1. **Status line** — one-liner: what happened (success, failure, partial)
2. **Summary** — 1-2 sentences on what was done and why
3. **Key details** — 3-6 bullets of concrete changes, results, or commands run
4. **Next steps** — only if something is unresolved or needs user action

Keep it under 600 characters for simple tasks, up to 1500 for complex ones. Every line should carry information — no filler.

### When to notify

- ALWAYS after completing a task the user asked you to do — but only once ALL work is finished
- ALWAYS after a long-running operation finishes (build, deploy, migration, etc.)
- ALWAYS when a task fails and you cannot recover — explain what went wrong
- ALWAYS when you are blocked and need user input — tell them what you need so they know to come back
- ALWAYS when you pause to ask a question or present options — the user may not be watching the terminal
- Do NOT notify for mid-task progress updates where you are still actively working and not waiting on the user
- Do NOT notify before running tests, linters, or verification
- Do NOT notify before committing — the commit is part of the task
