---
name: telegram-notify
description: Send a Telegram notification with a task summary
argument-hint: "[message]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
    - Exec(echo)
triggers:
  - user
  - model
---

# Telegram Notify

Send a Telegram message to the user summarizing what was accomplished.

## First-time setup

Before sending any notification, you MUST verify the skill is ready. Check both env vars:

```
echo "$TELEGRAM_BOT_TOKEN" "$TELEGRAM_CHAT_ID"
```

If **either is empty or unset**, the skill is not configured yet. Do NOT try to send a message — it will fail. Instead:

1. Tell the user Telegram notifications aren't set up yet and you need to walk them through it.
2. Run the interactive setup script. It is an interactive script — **run it in an interactive shell** and let the user respond to each prompt:
   ```
   uv run telegram-notify/scripts/setup.py
   ```
3. The setup script handles everything step by step:
   - Asks the user to create a bot via @BotFather on Telegram and paste the token
   - Validates the token against the Telegram API
   - Asks the user to message the bot, then auto-detects their chat ID
   - Sends a test message so the user can confirm it arrived
   - Offers to save credentials to their shell profile
4. After setup completes, verify the env vars are now set before proceeding.

If both env vars **are set**, send a quick test message to make sure the connection still works before relying on it:

```
uv run telegram-notify/scripts/send_telegram.py -m "telegram-notify is connected"
```

If the test fails (expired token, bot deleted, etc.), re-run the setup script.

## Sending a notification

```
uv run telegram-notify/scripts/send_telegram.py --message "Your message here"
```

### Options

- `--message` / `-m` — message text (required)
- `--parse-mode` — `Markdown`, `MarkdownV2`, or `HTML` (optional, default: plain text)
- `--chat-id` — override the env var for this call
- `--token` — override the env var for this call

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

When you need a response from the user and they may not be watching the terminal,
send a prompt via Telegram and wait for their reply:

```
uv run telegram-notify/scripts/wait_for_input.py --prompt "What should I do next?" --timeout 300
```

The script sends the prompt, long-polls for a reply, and prints the user's
message to stdout. Use `--json` for structured output.

### Options

- `--prompt` / `-p` — message to send before waiting (optional)
- `--timeout` / `-t` — max seconds to wait (default: 300 = 5 minutes)
- `--json` — output as JSON (`{"received": true, "text": "...", "timeout": false}`)
- `--chat-id` — override the env var for this call
- `--token` — override the env var for this call

Exit codes: 0 = message received, 2 = timeout.

### When to use this

- You are blocked and need a decision from the user
- You need credentials, a URL, or other info only the user can provide
- You finished a task and want to ask what to do next
- The user might be away from the terminal but reachable on their phone

## Instructions

Compose an appropriate notification message based on the task context, then run the script. If the user provided a specific message via arguments, send that directly.

User arguments: $ARGUMENTS
