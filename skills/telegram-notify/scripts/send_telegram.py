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

MAX_MESSAGE_LENGTH = 4096


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


def main():
    parser = argparse.ArgumentParser(description="Send a Telegram message via the Bot API")
    parser.add_argument("--message", "-m", required=True, help="Message text to send")
    parser.add_argument(
        "--parse-mode",
        choices=["Markdown", "MarkdownV2", "HTML"],
        default=None,
        help="Message formatting mode (default: plain text)",
    )
    parser.add_argument("--chat-id", help="Override TELEGRAM_CHAT_ID env var")
    parser.add_argument("--token", help="Override TELEGRAM_BOT_TOKEN env var")
    args = parser.parse_args()

    token = args.token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.", file=sys.stderr)
        print("Create a bot via @BotFather on Telegram to get a token.", file=sys.stderr)
        sys.exit(1)

    chat_id = args.chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        print("Error: TELEGRAM_CHAT_ID environment variable is not set.", file=sys.stderr)
        print("Message your bot, then visit:", file=sys.stderr)
        print(f"  https://api.telegram.org/bot{token}/getUpdates", file=sys.stderr)
        print("Find your chat.id in the response.", file=sys.stderr)
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
