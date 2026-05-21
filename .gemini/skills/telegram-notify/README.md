# telegram-notify

Send Telegram notifications from an AI agent session using the [Telegram Bot API](https://core.telegram.org/bots/api).

Useful as a "ping me when you're done" skill — the agent sends a concise task summary to your Telegram when it finishes working.

This is a markdown-only skill — no scripts or dependencies. The agent calls the Telegram Bot API directly via `curl`.

## Setup

### 1. Create a bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`
2. Choose a display name and username (must end in `bot`)
3. Copy the bot token BotFather gives you

### 2. Get your chat ID

1. Message your new bot (just say "hi")
2. Run:
   ```bash
   curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates" | python3 -m json.tool
   ```
3. Look for `"chat": {"id": 12345678, ...}` in the response

### 3. Export credentials

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
export TELEGRAM_CHAT_ID="12345678"
```

Add these to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) for persistence.

## Usage

### Send a message

```bash
curl -sf -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "'"$TELEGRAM_CHAT_ID"'", "text": "Hello from the terminal!"}'
```

### Validate your token

```bash
curl -sf "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | python3 -m json.tool
```

## As an Agent Skill

Copy the `telegram-notify/` directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r telegram-notify/ ~/.config/devin/skills/telegram-notify/
# or: cp -r telegram-notify/ ~/.windsurf/skills/telegram-notify/

# Project-specific
cp -r telegram-notify/ /path/to/project/.devin/skills/telegram-notify/
# or: cp -r telegram-notify/ /path/to/project/.windsurf/skills/telegram-notify/
```

Then invoke with `/telegram-notify` in a session, or let the agent call it autonomously when it finishes a task.
