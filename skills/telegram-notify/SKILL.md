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

Before sending any notification, you MUST verify the skill is ready:

```
uv run ~/.config/devin/skills/telegram-notify/scripts/send_telegram.py --check
```

**Do NOT echo, print, or log `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID`.** The `--check` flag validates that credentials are set and the bot token is valid, without revealing secret values.

If `--check` reports missing or invalid credentials, run the interactive setup script in an interactive shell:

```
uv run ~/.config/devin/skills/telegram-notify/scripts/setup.py
```

The setup script handles everything: bot creation via @BotFather, token validation, chat ID discovery, test message, and saving credentials to the shell profile.

After setup completes, run `--check` again to confirm.

## Sending a notification

```
uv run ~/.config/devin/skills/telegram-notify/scripts/send_telegram.py --message "Your message here"
```

### Options

- `--message` / `-m` — message text (required)
- `--parse-mode` — `Markdown`, `MarkdownV2`, or `HTML` (optional, default: plain text)

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
uv run ~/.config/devin/skills/telegram-notify/scripts/wait_for_input.py --prompt "What should I do next?"
```

The script sends the prompt, long-polls for a reply, and prints the user's
message to stdout. If no reply arrives within the timeout (default: 3 minutes),
it prints an autonomous-continuation prompt instead — telling you to use your
best judgment and keep working. Either way the exit code is 0 and you get
actionable text on stdout.

### Options

- `--prompt` / `-p` — message to send before waiting (optional)
- `--timeout` / `-t` — max seconds to wait (default: 180 = 3 minutes)
- `--json` — output as JSON (includes `autonomous_prompt` field on timeout)

On timeout the script exits 0 and outputs a continuation prompt. Read stdout
and follow its instructions — pick reasonable defaults, document assumptions,
and keep going.

### When to use this

- You are blocked and need a decision from the user
- You need credentials, a URL, or other info only the user can provide
- You finished a task and want to ask what to do next
- The user might be away from the terminal but reachable on their phone

## Instructions

Compose an appropriate notification message based on the task context, then run the script. If the user provided a specific message via arguments, send that directly.

User arguments: $ARGUMENTS
