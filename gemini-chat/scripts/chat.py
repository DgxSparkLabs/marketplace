# /// script
# requires-python = ">=3.11"
# dependencies = ["google-genai>=1.0.0"]
# ///
"""
Interactive multi-turn chat with Google Gemini.

Usage:
    uv run gemini-chat/scripts/chat.py                          # interactive REPL
    uv run gemini-chat/scripts/chat.py -m "what is rust?"       # single message
    uv run gemini-chat/scripts/chat.py --system "You are a pirate"  # with system prompt
    uv run gemini-chat/scripts/chat.py --model gemini-2.5-pro   # specific model
    uv run gemini-chat/scripts/chat.py --history chat.json      # resume a conversation

Requires GEMINI_API_KEY env var (get one free at https://aistudio.google.com/apikey).
"""

import argparse
import json
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types


DEFAULT_MODEL = "gemini-2.5-flash"


def _build_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print(
            "Error: GEMINI_API_KEY not set.\n"
            "Get a free key at https://aistudio.google.com/apikey\n"
            "then: export GEMINI_API_KEY='your-key'",
            file=sys.stderr,
        )
        sys.exit(1)
    return genai.Client(api_key=api_key)


def _load_history(path: Path) -> list[types.Content]:
    """Load conversation history from a JSON file."""
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    history = []
    for msg in data:
        history.append(types.Content(
            role=msg["role"],
            parts=[types.Part.from_text(text=p["text"]) for p in msg["parts"]],
        ))
    return history


def _save_history(chat, path: Path) -> None:
    """Save conversation history to a JSON file."""
    history = []
    for msg in chat.get_history():
        parts = []
        for p in msg.parts:
            if hasattr(p, "text") and p.text:
                parts.append({"text": p.text})
        if parts:
            history.append({"role": msg.role, "parts": parts})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")


def _print_streaming(chat, message: str) -> str:
    """Send a message with streaming and print chunks as they arrive."""
    full_text = ""
    for chunk in chat.send_message_stream(message):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_text += chunk.text
    print()
    return full_text


def _print_response(chat, message: str) -> str:
    """Send a message and print the full response."""
    response = chat.send_message(message)
    print(response.text)
    return response.text


def run_interactive(client: genai.Client, model: str, system: str | None,
                    history_path: Path | None, stream: bool,
                    search: bool) -> None:
    """Run an interactive chat REPL."""
    config = {}
    if system:
        config["system_instruction"] = system
    if search:
        config["tools"] = [types.Tool(google_search=types.GoogleSearch())]

    history = []
    if history_path:
        history = _load_history(history_path)

    chat = client.chats.create(
        model=model,
        config=config if config else None,
        history=history if history else None,
    )

    if history:
        print(f"Resumed conversation ({len(history)} messages)")
    label = model + (" + Search" if search else "")
    print(f"Chatting with {label}. Type 'quit' to exit, 'save <file>' to save history.\n")

    send = _print_streaming if stream else _print_response

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye.")
            break
        if user_input.lower().startswith("save "):
            save_path = Path(user_input[5:].strip())
            _save_history(chat, save_path)
            print(f"Saved to {save_path}")
            continue

        print("\nGemini: ", end="")
        try:
            send(chat, user_input)
        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
        print()

    if history_path:
        _save_history(chat, history_path)
        print(f"History saved to {history_path}")


def run_single(client: genai.Client, model: str, system: str | None,
               message: str, stream: bool, as_json: bool,
               search: bool) -> None:
    """Send a single message and print the response."""
    config = {}
    if system:
        config["system_instruction"] = system
    if search:
        config["tools"] = [types.Tool(google_search=types.GoogleSearch())]

    chat = client.chats.create(
        model=model,
        config=config if config else None,
    )

    if as_json:
        response = chat.send_message(message)
        out = {
            "model": model,
            "message": message,
            "response": response.text,
        }
        if system:
            out["system"] = system
        print(json.dumps(out, indent=2, ensure_ascii=False))
    elif stream:
        _print_streaming(chat, message)
    else:
        _print_response(chat, message)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive multi-turn chat with Google Gemini.",
    )
    parser.add_argument("-m", "--message", help="Single message (non-interactive)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--system", "-s", help="System instruction for the conversation")
    parser.add_argument("--history", type=Path, help="JSON file to load/save conversation history")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming output")
    parser.add_argument("--search", action="store_true", help="Enable Google Search grounding (like AI Mode)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON (single message mode)")
    args = parser.parse_args()

    client = _build_client()
    stream = not args.no_stream

    if args.message:
        run_single(client, args.model, args.system, args.message, stream, args.as_json, args.search)
    else:
        run_interactive(client, args.model, args.system, args.history, stream, args.search)


if __name__ == "__main__":
    main()
