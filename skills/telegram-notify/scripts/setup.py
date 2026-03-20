# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Interactive setup for telegram-notify. Guides the user through bot creation,
chat ID discovery, test message, and shell profile configuration."""

import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

TELEGRAM_API = "https://api.telegram.org/bot{token}"


def api_call(token: str, method: str, payload: dict | None = None) -> dict:
    url = f"{TELEGRAM_API.format(token=token)}/{method}"
    if payload:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def prompt(msg: str, *, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{msg}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nSetup cancelled.")
        sys.exit(1)
    return value or default


def prompt_yes_no(msg: str, *, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    try:
        value = input(f"{msg} ({hint}): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nSetup cancelled.")
        sys.exit(1)
    if not value:
        return default
    return value in ("y", "yes")


def step(n: int, title: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"  Step {n}: {title}")
    print(f"{'=' * 50}\n")


def detect_shell_profile() -> pathlib.Path | None:
    shell = os.environ.get("SHELL", "")
    home = pathlib.Path.home()
    candidates: list[pathlib.Path] = []

    if "zsh" in shell:
        candidates = [home / ".zshrc", home / ".zprofile"]
    elif "bash" in shell:
        candidates = [home / ".bashrc", home / ".bash_profile", home / ".profile"]
    else:
        candidates = [home / ".profile", home / ".bashrc"]

    for c in candidates:
        if c.exists():
            return c
    return candidates[0] if candidates else None


def main() -> None:
    print()
    print("  Telegram Notify — Setup")
    print("  " + "-" * 30)
    print()
    print("  This will walk you through:")
    print("  1. Creating a Telegram bot (via @BotFather)")
    print("  2. Getting your chat ID")
    print("  3. Sending a test message")
    print("  4. Saving credentials to your shell profile")
    print()

    existing_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    existing_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if existing_token and existing_chat_id:
        print("  Found existing config:")
        print(f"    TELEGRAM_BOT_TOKEN = {existing_token[:12]}...")
        print(f"    TELEGRAM_CHAT_ID   = {existing_chat_id}")
        if not prompt_yes_no("\n  Reconfigure from scratch?", default=False):
            print("\n  Keeping existing config. Sending a test message...\n")
            _send_test(existing_token, existing_chat_id)
            return

    # ----- Step 1: Get bot token -----

    step(1, "Create a Telegram Bot")

    if existing_token:
        print(f"  Current TELEGRAM_BOT_TOKEN: {existing_token[:12]}...")
        if prompt_yes_no("  Use existing token?"):
            token = existing_token
        else:
            token = ""
    else:
        token = ""

    if not token:
        print("  Open Telegram and search for @BotFather, then:")
        print()
        print("    1. Send /newbot")
        print("    2. Choose a display name (e.g. 'Task Notifier')")
        print("    3. Choose a username (must end in 'bot', e.g. 'my_task_notify_bot')")
        print("    4. BotFather will reply with your bot token")
        print()
        token = prompt("  Paste your bot token here")

    if not token:
        print("\n  Error: No token provided. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Validate token
    print("\n  Validating token...", end=" ", flush=True)
    try:
        me = api_call(token, "getMe")
        bot_name = me["result"]["first_name"]
        bot_username = me["result"].get("username", "unknown")
        print("OK")
        print(f"  Bot: {bot_name} (@{bot_username})")
    except Exception as e:
        print("FAILED")
        print(f"\n  Could not validate token: {e}", file=sys.stderr)
        print("  Double-check the token from @BotFather and try again.", file=sys.stderr)
        sys.exit(1)

    # ----- Step 2: Get chat ID -----

    step(2, "Get Your Chat ID")

    if existing_chat_id:
        print(f"  Current TELEGRAM_CHAT_ID: {existing_chat_id}")
        if prompt_yes_no("  Use existing chat ID?"):
            chat_id = existing_chat_id
        else:
            chat_id = ""
    else:
        chat_id = ""

    if not chat_id:
        # Clear any old updates so we only see fresh ones
        try:
            old = api_call(token, "getUpdates")
            old_updates = old.get("result", [])
            if old_updates:
                last_id = old_updates[-1]["update_id"]
                api_call(token, "getUpdates", {"offset": last_id + 1})
        except Exception:
            pass

        print(f"  Open Telegram and send any message to @{bot_username}.")
        print("  (Just say 'hi' — we need this to detect your chat ID.)")
        print()
        input("  Press Enter once you've sent the message...")
        print()
        print("  Polling for your message", end="", flush=True)

        chat_id = ""
        for attempt in range(15):
            try:
                updates = api_call(token, "getUpdates")
                results = updates.get("result", [])
                for u in results:
                    msg = u.get("message", {})
                    chat = msg.get("chat", {})
                    cid = chat.get("id")
                    if cid:
                        chat_id = str(cid)
                        chat_name = (
                            chat.get("first_name", "")
                            + " "
                            + chat.get("last_name", "")
                        ).strip() or chat.get("title", "unknown")
                        break
                if chat_id:
                    break
            except Exception:
                pass
            print(".", end="", flush=True)
            time.sleep(2)

        print()

        if not chat_id:
            print("\n  Could not detect a chat ID automatically.")
            print("  You can find it manually by visiting:")
            print("    https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates")
            print("  (Replace <YOUR_TOKEN> with your bot token.)")
            print("  Look for \"chat\":{\"id\": NUMBER} in the response.\n")
            chat_id = prompt("  Enter your chat ID manually")

        if not chat_id:
            print("\n  Error: No chat ID provided. Exiting.", file=sys.stderr)
            sys.exit(1)

        print(f"\n  Found chat: {chat_name} (ID: {chat_id})")

    # ----- Step 3: Test message -----

    step(3, "Send a Test Message")
    _send_test(token, chat_id)

    # ----- Step 4: Save to shell profile -----

    step(4, "Save Configuration")

    profile = detect_shell_profile()
    export_lines = (
        f'\nexport TELEGRAM_BOT_TOKEN="{token}"\n'
        f'export TELEGRAM_CHAT_ID="{chat_id}"\n'
    )

    print("  To persist these credentials, add to your shell profile:\n")
    print(f'    export TELEGRAM_BOT_TOKEN="{token[:12]}..."')
    print(f'    export TELEGRAM_CHAT_ID="{chat_id}"')

    if profile:
        print(f"\n  Detected shell profile: {profile}")
        if prompt_yes_no(f"  Append to {profile.name}?"):
            try:
                with open(profile, "a") as f:
                    f.write("\n# telegram-notify\n")
                    f.write(export_lines)
                print(f"\n  Written to {profile}.")
                print(f"  Run: source {profile}")
            except OSError as e:
                print(f"\n  Could not write to {profile}: {e}", file=sys.stderr)
                print("  Add the export lines manually.", file=sys.stderr)
        else:
            print("\n  Skipped. Add the lines manually when ready.")
    else:
        print("\n  Could not detect shell profile. Add the lines manually.")

    print()
    print("  " + "-" * 30)
    print("  Setup complete!")
    print()
    print("  The agent will now ping you on Telegram when tasks finish.")
    print("  You can also invoke it manually: /telegram-notify")
    print()


def _send_test(token: str, chat_id: str) -> None:
    print("  Sending test message...", end=" ", flush=True)
    try:
        result = api_call(token, "sendMessage", {
            "chat_id": chat_id,
            "text": "telegram-notify is set up and working. You'll receive task summaries here.",
        })
        if result.get("ok"):
            print("OK")
            print("  Check your Telegram — you should see the test message.")
        else:
            desc = result.get("description", "unknown error")
            print(f"FAILED: {desc}")
            sys.exit(1)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            desc = json.loads(body).get("description", body)
        except json.JSONDecodeError:
            desc = body
        print("FAILED")
        print(f"\n  API error: {desc}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("FAILED")
        print(f"\n  Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
