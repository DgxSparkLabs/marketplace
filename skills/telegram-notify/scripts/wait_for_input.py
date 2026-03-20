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
from pathlib import Path

# Hard limits — never wait forever, never skip the wait entirely.
MIN_TIMEOUT = 10
MAX_TIMEOUT = 600  # 10 minutes

SETUP_HINT = (
    "Run the setup script: uv run "
    + str(Path(__file__).resolve().parent / "setup.py")
)


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
        default=180,
        help="Max seconds to wait (default: 180, range: 10–600)",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args()

    # Clamp timeout to safe bounds — never wait forever.
    timeout = max(MIN_TIMEOUT, min(args.timeout, MAX_TIMEOUT))
    if timeout != args.timeout:
        print(
            f"Timeout clamped to {timeout}s (requested {args.timeout}s, "
            f"allowed range: {MIN_TIMEOUT}–{MAX_TIMEOUT}s)",
            file=sys.stderr,
        )

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

    if args.prompt:
        try:
            send_message(token, chat_id, args.prompt)
            print(f"Sent prompt: {args.prompt}", file=sys.stderr)
        except Exception as e:
            print(f"Failed to send prompt: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Waiting for reply (timeout: {timeout}s)...", file=sys.stderr)

    text = wait_for_message(token, chat_id, timeout)

    AUTONOMOUS_PROMPT = (
        "No reply received — the user is likely away. Continue autonomously.\n"
        "\n"
        "1. Re-read what you were working on and what you asked the user.\n"
        "2. If you asked a decision question, pick the best-judgment default and proceed.\n"
        "3. If you need credentials or something only the user can provide, set that aside "
        "and work on everything else you can.\n"
        "4. Document any assumptions you made so the user can review later.\n"
        "5. Keep going until you're truly blocked or the task is done."
    )

    if text is None:
        if args.as_json:
            print(json.dumps({
                "received": False,
                "text": None,
                "timeout": True,
                "autonomous_prompt": AUTONOMOUS_PROMPT,
            }))
        else:
            print(AUTONOMOUS_PROMPT)
        sys.exit(0)

    if args.as_json:
        print(json.dumps({"received": True, "text": text, "timeout": False}))
    else:
        print(text)


if __name__ == "__main__":
    main()
