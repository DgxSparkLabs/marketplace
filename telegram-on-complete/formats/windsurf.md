---
trigger: always_on
description: "Send a Telegram notification after completing any task"
---

## Telegram on Complete

After completing any user-requested task, ALWAYS send a Telegram notification summarizing what was done. This is non-negotiable — the user relies on these pings to know when work is finished.

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

- ALWAYS after completing a task the user asked you to do
- ALWAYS after a long-running operation finishes (build, deploy, migration, etc.)
- ALWAYS when a task fails and you cannot recover — explain what went wrong
- Do NOT notify for trivial follow-up questions, clarifications, or mid-task status updates
