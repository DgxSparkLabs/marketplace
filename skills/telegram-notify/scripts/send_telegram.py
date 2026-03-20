# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Send a Telegram message via the Bot API (zero dependencies)."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

MAX_MESSAGE_LENGTH = 4096

SETUP_HINT = (
    "Run the setup script: uv run "
    + str(Path(__file__).resolve().parent / "setup.py")
)


def send_message(token: str, chat_id: str, text: str, parse_mode: str | None = None) -> dict:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload: dict = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(body).get("description", body)
        except json.JSONDecodeError:
            detail = body
        raise RuntimeError(f"Telegram API error {e.code}: {detail}") from e


def check_config() -> None:
    """Verify env vars are set and the bot token is valid, without printing secrets."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token and not chat_id:
        print("TELEGRAM_BOT_TOKEN: not set", file=sys.stderr)
        print("TELEGRAM_CHAT_ID: not set", file=sys.stderr)
        print(SETUP_HINT, file=sys.stderr)
        sys.exit(1)
    if not token:
        print("TELEGRAM_BOT_TOKEN: not set", file=sys.stderr)
        print("TELEGRAM_CHAT_ID: set", file=sys.stderr)
        print(SETUP_HINT, file=sys.stderr)
        sys.exit(1)
    if not chat_id:
        print("TELEGRAM_BOT_TOKEN: set", file=sys.stderr)
        print("TELEGRAM_CHAT_ID: not set", file=sys.stderr)
        print(SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    # Validate the token against the Telegram API
    url = f"https://api.telegram.org/bot{token}/getMe"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            bot_name = data.get("result", {}).get("username", "unknown")
            print(f"TELEGRAM_BOT_TOKEN: valid (bot: @{bot_name})")
            print("TELEGRAM_CHAT_ID: set")
    except urllib.error.HTTPError:
        print("TELEGRAM_BOT_TOKEN: set but INVALID (API rejected it)", file=sys.stderr)
        print("TELEGRAM_CHAT_ID: set", file=sys.stderr)
        print(SETUP_HINT, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"TELEGRAM_BOT_TOKEN: set but could not validate ({e})", file=sys.stderr)
        print("TELEGRAM_CHAT_ID: set", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Send a Telegram message via the Bot API")
    parser.add_argument("--message", "-m", help="Message text to send")
    parser.add_argument(
        "--parse-mode",
        choices=["Markdown", "MarkdownV2", "HTML"],
        default=None,
        help="Message formatting mode (default: plain text)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that credentials are configured and valid, then exit",
    )
    args = parser.parse_args()

    if args.check:
        check_config()
        sys.exit(0)

    if not args.message:
        parser.error("--message is required (unless using --check)")

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN is not set.", file=sys.stderr)
        print(SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        print("Error: TELEGRAM_CHAT_ID is not set.", file=sys.stderr)
        print(SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    message = args.message
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[: MAX_MESSAGE_LENGTH - 20] + "\n\n... [truncated]"

    try:
        result = send_message(token, chat_id, message, args.parse_mode)
        msg_id = result.get("result", {}).get("message_id", "unknown")
        print(f"Message sent (id: {msg_id})")
    except RuntimeError as e:
        print(f"Failed to send message: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
