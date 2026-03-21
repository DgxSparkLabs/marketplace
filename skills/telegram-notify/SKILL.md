---
name: telegram-notify
description: Send a Telegram notification with a task summary
argument-hint: "[message]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(curl)
    - Exec(echo)
triggers:
  - user
  - model
---

# Telegram Notify

Send a Telegram message to the user summarizing what was accomplished.

## First-time setup

Check that both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set:

```
echo "TOKEN=${TELEGRAM_BOT_TOKEN:+set}" && echo "CHAT_ID=${TELEGRAM_CHAT_ID:+set}"
```

**Do NOT echo, print, or log the actual values of `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID`.**

If either is missing, tell the user:

1. Message [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`, and copy the token.
2. Message the new bot, then find the chat ID:
   ```
   curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin),indent=2))"
   ```
   Look for `"chat": {"id": NUMBER}` in the response.
3. Export both values:
   ```
   export TELEGRAM_BOT_TOKEN="<token>"
   export TELEGRAM_CHAT_ID="<chat_id>"
   ```
4. Add the exports to their shell profile for persistence.

To validate the token works:

```
curl -sf "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Bot: @{d[\"result\"][\"username\"]}')"
```

## Sending a notification

```
curl -sf -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"$TELEGRAM_CHAT_ID\", \"text\": \"YOUR_MESSAGE_HERE\"}"
```

To use Markdown formatting, add `"parse_mode": "Markdown"` to the JSON body.

**Important:** Escape any double quotes or special JSON characters in the message text. For multi-line messages, use `\n` for newlines in the JSON string.

## Composing the message

When notifying the user about a completed task, compose a message that is **both quick to scan and substantive**. Follow this structure:

1. **Status line** — one-liner with the outcome (use a checkmark or X prefix)
2. **Summary** — 1-2 sentences explaining what was done and why
3. **Key details** — bullet list of concrete changes, commands run, or results (3-6 bullets)
4. **Next steps** — only if there are unresolved items or follow-ups the user should know about

Example:

```
Task complete: refactored auth middleware

Extracted token validation into a shared utility and updated all three route files to use it. Tests pass, no behavior change.

- Created src/utils/validate-token.ts with JWT verification logic
- Updated src/routes/api.ts, src/routes/admin.ts, src/routes/webhooks.ts
- Removed 47 lines of duplicated validation code
- All 23 existing tests pass, added 4 new unit tests for validate-token
```

Keep it **under 600 characters** when possible so it reads well on a phone. If the task is complex, go up to ~1500 characters but no more. Omit fluff — every line should carry information.

Do NOT use Markdown parse mode unless the message contains code blocks or formatting that genuinely helps readability. Plain text is preferred for most notifications.

## Waiting for user input

When you need a response from the user and they may not be watching the terminal, send a prompt via Telegram and poll for their reply.

### Send the prompt

```
curl -sf -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"$TELEGRAM_CHAT_ID\", \"text\": \"YOUR_QUESTION_HERE\"}"
```

### Drain old updates then poll for a reply

First, drain pending updates to get the latest offset:

```
curl -sf "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | python3 -c "
import sys, json
data = json.load(sys.stdin)
updates = data.get('result', [])
if updates:
    print(updates[-1]['update_id'] + 1)
else:
    print(0)
"
```

Then poll with that offset (replace `OFFSET` with the value from above). Repeat up to 6 times (30s each = ~3 minutes total):

```
curl -sf "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?timeout=30&offset=OFFSET" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('result', []):
    msg = u.get('message', {})
    if str(msg.get('chat', {}).get('id', '')) == '$TELEGRAM_CHAT_ID' and msg.get('text'):
        print(msg['text'])
        sys.exit(0)
print('')
"
```

If no reply arrives after ~3 minutes, continue autonomously: pick reasonable defaults, document assumptions, and keep working. For true emergencies (data loss, security), do NOT continue the dangerous action — leave a note in `HANDOFF.md` instead.

## Instructions

Compose an appropriate notification message based on the task context, then send it using `curl`. If the user provided a specific message via arguments, send that directly.

User arguments: $ARGUMENTS
