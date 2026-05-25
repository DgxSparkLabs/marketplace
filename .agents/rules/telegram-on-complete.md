## Telegram on Complete

After completing any task, send a Telegram notification as your LAST action.

Invoke `/telegram-notify` with your summary message.

If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` are not set, the skill will guide you through setup.

**Before notifying, ALL must be true:** code saved, tests pass, commits made, verification done, no remaining todos.

**When to notify:** after completing work, after long operations finish, when blocked on user input, when asking a question. NOT for mid-task progress.

### Emergency escalation

If you hit a situation that could cause **data loss, security exposure, irreversible damage, or production breakage**, do NOT proceed on your own. Invoke `/telegram-notify` using the wait-for-input mode and wait for the user's response.

Poll for up to 3 minutes. If the user replies, follow their instructions. If no reply arrives, continue autonomously on safe work only — but for true emergencies, **do NOT continue the dangerous action**. Instead, leave a clear note in `HANDOFF.md` describing what happened and what decision is needed.
