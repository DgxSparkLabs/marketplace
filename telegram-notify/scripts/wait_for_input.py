# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Wait for a text message from the user via Telegram.

Sends an optional prompt, then long-polls the Telegram Bot API
until a message arrives from the configured chat. Returns the
message text to stdout for the agent to consume.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error


def get_updates(token: str, offset: int | None = None, timeout: int = 30) -> dict:
    """Long-poll the Telegram Bot API for new messages."""
    url = f"https://api.telegram.org/bot{token}/getUpdates?timeout={timeout}"
    if offset is not None:
        url += f"&offset={offset}"
    url += "&allowed_updates=[\"message\"]"

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout + 10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram API error {e.code}: {body}") from e
    except (urllib.error.URLError, TimeoutError):
        return {"ok": True, "result": []}


def send_message(token: str, chat_id: str, text: str) -> dict:
    """Send a message to the user."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def drain_pending(token: str) -> int | None:
    """Consume all pending updates so we only get fresh messages."""
    offset = None
    while True:
        result = get_updates(token, offset=offset, timeout=0)
        updates = result.get("result", [])
        if not updates:
            break
        offset = updates[-1]["update_id"] + 1
    return offset


def wait_for_message(
    token: str, chat_id: str, timeout_seconds: int, poll_interval: int = 30
) -> str | None:
    """Block until a message arrives from the target chat, or timeout."""
    offset = drain_pending(token)
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        remaining = int(deadline - time.time())
        if remaining <= 0:
            break
        poll_time = min(poll_interval, remaining)

        result = get_updates(token, offset=offset, timeout=poll_time)
        updates = result.get("result", [])

        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            msg_chat_id = str(msg.get("chat", {}).get("id", ""))
            text = msg.get("text", "")

            if msg_chat_id == chat_id and text:
                # Drain this update so it doesn't replay
                drain_pending(token)
                return text

    return None


def main():
    parser = argparse.ArgumentParser(description="Wait for Telegram input from the user")
    parser.add_argument(
        "--prompt", "-p",
        help="Message to send before waiting (e.g. 'What should I do next?')",
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Max seconds to wait (default: 300 = 5 minutes)",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    parser.add_argument("--chat-id", help="Override TELEGRAM_CHAT_ID env var")
    parser.add_argument("--token", help="Override TELEGRAM_BOT_TOKEN env var")
    args = parser.parse_args()

    token = args.token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not set.", file=sys.stderr)
        sys.exit(1)

    chat_id = args.chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        print("Error: TELEGRAM_CHAT_ID not set.", file=sys.stderr)
        sys.exit(1)

    if args.prompt:
        try:
            send_message(token, chat_id, args.prompt)
            print(f"Sent prompt: {args.prompt}", file=sys.stderr)
        except Exception as e:
            print(f"Failed to send prompt: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Waiting for reply (timeout: {args.timeout}s)...", file=sys.stderr)

    text = wait_for_message(token, chat_id, args.timeout)

    if text is None:
        if args.as_json:
            print(json.dumps({"received": False, "text": None, "timeout": True}))
        else:
            print("TIMEOUT: No message received.", file=sys.stderr)
        sys.exit(2)

    if args.as_json:
        print(json.dumps({"received": True, "text": text, "timeout": False}))
    else:
        print(text)


if __name__ == "__main__":
    main()
