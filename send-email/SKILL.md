---
name: send-email
description: Send an email to someone using the Resend API
argument-hint: "[recipient] [subject]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Send Email

Send an email using the Resend API via a self-contained Python script.

## Prerequisites

The `RESEND_API_KEY` environment variable must be set. If it is not set, tell the user to:
1. Sign up at https://resend.com
2. Get an API key from https://resend.com/api-keys
3. Export it: `export RESEND_API_KEY="re_..."`

The script requires `uv` to be installed. If not available, tell the user to install it:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Sending an Email

Run the script from the skill directory:

```
uv run send-email/scripts/send_email.py --to "recipient@example.com" --subject "Subject line" --body "Email body text"
```

### Options

- `--to` — one or more recipient emails (required)
- `--subject` — email subject line (required)
- `--body` — plain text email body (required)
- `--html` — HTML email body (optional, overrides --body)
- `--from` — sender address (default: onboarding@resend.dev)

### Multiple recipients

```
uv run send-email/scripts/send_email.py --to "a@example.com" "b@example.com" --subject "Hello" --body "Hi everyone!"
```

## Instructions

Parse the user's request to extract the recipient, subject, and body. If any are missing, compose reasonable defaults or ask the user. Then run the script with the appropriate arguments.

User arguments: $ARGUMENTS
