# send-email

Send emails from the command line or an AI agent session using the [Resend](https://resend.com) API.

## Setup

1. Sign up at [resend.com](https://resend.com) and get an API key.
2. Export it:
   ```bash
   export RESEND_API_KEY="re_..."
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## Usage

The script is self-contained with inline dependencies (PEP 723). No install step needed:

```bash
uv run scripts/send_email.py --to "recipient@example.com" --subject "Hello" --body "Hi there!"
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--to` | Yes | One or more recipient email addresses |
| `--subject` | Yes | Email subject line |
| `--body` | Yes | Plain text email body |
| `--html` | No | HTML email body (overrides `--body`) |
| `--from` | No | Sender address (default: `onboarding@resend.dev`) |

### Examples

```bash
# Multiple recipients
uv run scripts/send_email.py --to "a@example.com" "b@example.com" --subject "Hello" --body "Hi all!"

# HTML email
uv run scripts/send_email.py --to "a@example.com" --subject "Hello" --body "fallback" --html "<h1>Hello!</h1>"
```

## As an Agent Skill

Copy the `send-email/` directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r send-email/ ~/.config/cognition/skills/send-email/
# or: cp -r send-email/ ~/.windsurf/skills/send-email/

# Project-specific
cp -r send-email/ /path/to/project/.cognition/skills/send-email/
# or: cp -r send-email/ /path/to/project/.windsurf/skills/send-email/
```

Then invoke with `/send-email` in a session.
