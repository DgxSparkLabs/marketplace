# gemini-chat

Interactive multi-turn chat with Google Gemini using the official `google-genai` SDK.

## Features

- **Interactive REPL** — back-and-forth conversation with streaming output
- **Multi-turn memory** — Gemini remembers the full conversation context
- **System prompts** — set the tone or persona for the conversation
- **Conversation history** — save and resume conversations from JSON files
- **Single-message mode** — quick one-off questions with optional JSON output
- **Google Search grounding** — enable `--search` for real-time web-grounded answers (like AI Mode)
- **Model selection** — use any Gemini model (flash, pro, etc.)

## Quick Start

```bash
# Get a free API key
# Visit https://aistudio.google.com/apikey

export GEMINI_API_KEY='your-key'

# Start chatting
uv run gemini-chat/scripts/chat.py

# Single question
uv run gemini-chat/scripts/chat.py -m "what's new in Python 3.13?"

# With system prompt
uv run gemini-chat/scripts/chat.py --system "You are a database expert"

# Save and resume conversations
uv run gemini-chat/scripts/chat.py --history conversation.json

# Search-grounded chat (like Google AI Mode)
uv run gemini-chat/scripts/chat.py --search
```

## Requirements

- Python 3.11+
- `GEMINI_API_KEY` environment variable ([get one free](https://aistudio.google.com/apikey))

## Options

| Flag | Required | Description |
|------|----------|-------------|
| `-m`, `--message` | No | Single message (non-interactive mode) |
| `--model` | No | Model name (default: `gemini-2.5-flash`) |
| `-s`, `--system` | No | System instruction for the conversation |
| `--history` | No | JSON file to load/save conversation history |
| `--no-stream` | No | Disable streaming output |
| `--search` | No | Enable Google Search grounding (like AI Mode) |
| `--json` | No | Output as JSON (single-message mode only) |
| `--check` | No | Validate `GEMINI_API_KEY` and exit |

## As an Agent Skill

Copy the `gemini-chat/` directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r gemini-chat/ ~/.config/devin/skills/gemini-chat/
# or: cp -r gemini-chat/ ~/.windsurf/skills/gemini-chat/

# Project-specific
cp -r gemini-chat/ /path/to/project/.devin/skills/gemini-chat/
# or: cp -r gemini-chat/ /path/to/project/.windsurf/skills/gemini-chat/
```

Then invoke with `/gemini-chat` in a session, or let the agent call it autonomously.

## Prior Art

- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) — Google's official Node.js CLI
- [simonw/llm](https://github.com/simonw/llm) + [llm-gemini](https://github.com/simonw/llm-gemini) — multi-model CLI with Gemini plugin
- [googleapis/python-genai](https://github.com/googleapis/python-genai) — official Python SDK (used by this skill)

This skill uses the official `google-genai` SDK directly for a lightweight, zero-config experience focused on interactive conversation.
