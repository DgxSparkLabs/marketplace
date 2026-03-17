## Telegram on Complete

After completing any task, send a Telegram notification as your LAST action.

```
uv run telegram-notify/scripts/send_telegram.py -m "<summary>"
```

If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` are not set, run setup first:
```
uv run telegram-notify/scripts/setup.py
```

**Before notifying, ALL must be true:** code saved, tests pass, commits made, verification done, no remaining todos.

**When to notify:** after completing work, after long operations finish, when blocked on user input, when asking a question. NOT for mid-task progress.

### Emergency escalation

If you hit a situation that could cause **data loss, security exposure, irreversible damage, or production breakage**, do NOT proceed on your own. Reach the user via Telegram and wait for their response:

```
uv run telegram-notify/scripts/wait_for_input.py -p "URGENT: <describe the emergency and what you need>"
```

The script waits up to 3 minutes. If the user replies, follow their instructions. If they don't reply, the script returns an autonomous-continuation prompt — but for true emergencies, **do NOT continue the dangerous action**. Instead, leave a clear note in `PROGRESS.md` describing what happened and what decision is needed, then move on to safe work only.
